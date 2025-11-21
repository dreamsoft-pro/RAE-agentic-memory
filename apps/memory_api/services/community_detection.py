"""
Community Detection and Summarization - Pillar 2: Wisdom.

Implements:
- Community Detection (Leiden/Louvain via networkx/community)
- Community Summarization (LLM)
- Super-Node Creation
"""

import structlog
from typing import List, Dict, Any, Optional
import networkx as nx
import community.community_louvain as community_louvain
import asyncpg
from pydantic import BaseModel, Field

from apps.memory_api.config import settings
from apps.memory_api.services.llm import get_llm_provider

logger = structlog.get_logger(__name__)

class CommunitySummary(BaseModel):
    summary: str = Field(..., description="A high-level synthesis of the information contained in the community.")
    themes: List[str] = Field(..., description="Key themes or topics in this community.")
    title: str = Field(..., description="A short title for this community/cluster.")

class CommunityDetectionService:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool
        self.llm_provider = get_llm_provider()

    async def run_community_detection_and_summarization(self, project_id: str, tenant_id: str):
        """
        1. Load Graph from DB.
        2. Run Community Detection (Louvain).
        3. For each community, generate summary.
        4. Store summary as 'Super-Node'.
        """
        logger.info("starting_community_detection", project_id=project_id, tenant_id=tenant_id)

        # 1. Load Graph
        graph = await self._load_graph_from_db(project_id, tenant_id)
        if len(graph.nodes) < 5:
            logger.info("graph_too_small_for_communities", node_count=len(graph.nodes))
            return

        # 2. Detect Communities
        # Using Louvain algorithm for community detection
        # Partition is a dict: {node: community_id}
        partition = community_louvain.best_partition(graph)

        # Group nodes by community
        communities = {}
        for node, community_id in partition.items():
            if community_id not in communities:
                communities[community_id] = []
            communities[community_id].append(node)

        logger.info("communities_detected", count=len(communities))

        # 3. & 4. Summarize and Store
        for community_id, node_ids in communities.items():
            # Only process communities of a certain size
            if len(node_ids) < 3:
                continue

            await self._process_community(community_id, node_ids, graph, project_id, tenant_id)

    async def _process_community(self, community_id: int, node_ids: List[str], graph: nx.Graph, project_id: str, tenant_id: str):
        # Gather information about the community
        # Nodes and their immediate edges/relationships within the community
        nodes_info = []
        for node_id in node_ids:
            # We used internal DB IDs for graph nodes, but we need labels for LLM
            # Let's assume graph nodes are keyed by 'label' or we have a mapping.
            # In _load_graph_from_db, I will set node 'label' attribute.
            label = graph.nodes[node_id].get('label', str(node_id))
            nodes_info.append(label)

        # Get edges inside the community
        edges_info = []
        subgraph = graph.subgraph(node_ids)
        for u, v, data in subgraph.edges(data=True):
            u_label = graph.nodes[u].get('label', str(u))
            v_label = graph.nodes[v].get('label', str(v))
            relation = data.get('relation', 'RELATED_TO')
            edges_info.append(f"{u_label} --[{relation}]--> {v_label}")

        description = f"Nodes: {', '.join(nodes_info)}\nRelationships:\n{chr(10).join(edges_info[:50])}" # Limit edges to fit context

        # Generate Summary
        summary = await self._generate_summary(description)

        # Store as Super-Node
        await self._store_super_node(community_id, summary, node_ids, project_id, tenant_id)

    async def _generate_summary(self, description: str) -> CommunitySummary:
        prompt = f"""
        Analyze the following community of entities and relationships from a knowledge graph:

        {description}

        Synthesize this information into a high-level summary.
        Instead of listing facts, generalize them.
        Example: Instead of "User likes sushi", "User likes ramen", say "User prefers Japanese cuisine".

        Provide a Title, a Summary, and a list of Key Themes.
        """

        try:
            # Use the "Sage" model (Synthesis Model)
            result = await self.llm_provider.generate_structured(
                system="You are a Wisdom Engine responsible for synthesizing knowledge.",
                prompt=prompt,
                model=settings.SYNTHESIS_MODEL,
                response_model=CommunitySummary
            )
            return result
        except Exception as e:
            logger.error("community_summarization_failed", error=str(e))
            return CommunitySummary(summary="Extraction failed", themes=[], title="Unknown Community")

    async def _store_super_node(self, community_id: int, summary: CommunitySummary, member_node_ids: List[int], project_id: str, tenant_id: str):
        """
        Store the summary as a special node in the graph (e.g. type='Community').
        And link it to member nodes (or just keep it separate).
        For now, let's store it in `knowledge_graph_nodes` with a special label format or property.
        """

        node_label = f"Community: {summary.title}"
        properties = {
            "type": "community",
            "summary": summary.summary,
            "themes": summary.themes,
            "community_id": community_id,
            "member_count": len(member_node_ids)
        }

        async with self.pool.acquire() as conn:
            # Create Super Node
            # We need a unique ID for it. Let's use negative IDs or a UUID string if the column allows.
            # The schema says `node_id` is a string (label/unique identifier).
            # The `id` column is serial int.

            # Let's make a unique node_id
            super_node_id = f"community_{project_id}_{community_id}"

            await conn.execute(
                """
                INSERT INTO knowledge_graph_nodes (tenant_id, project_id, node_id, label, properties)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (tenant_id, project_id, node_id)
                DO UPDATE SET label = $4, properties = $5
                """,
                tenant_id, project_id, super_node_id, node_label, properties
            )

            # We could link this super node to all members, but that might clutter the graph.
            # "Hybrid Search" implies we search these nodes first.
            # So just having them is enough for now.

    async def _load_graph_from_db(self, project_id: str, tenant_id: str) -> nx.Graph:
        G = nx.Graph()

        async with self.pool.acquire() as conn:
            # Load Nodes
            nodes = await conn.fetch(
                "SELECT id, label FROM knowledge_graph_nodes WHERE tenant_id = $1 AND project_id = $2",
                tenant_id, project_id
            )
            for n in nodes:
                G.add_node(n['id'], label=n['label'])

            # Load Edges
            edges = await conn.fetch(
                """
                SELECT source_node_id, target_node_id, relation
                FROM knowledge_graph_edges
                WHERE tenant_id = $1 AND project_id = $2
                """,
                tenant_id, project_id
            )
            for e in edges:
                if G.has_node(e['source_node_id']) and G.has_node(e['target_node_id']):
                    G.add_edge(e['source_node_id'], e['target_node_id'], relation=e['relation'])

        return G
