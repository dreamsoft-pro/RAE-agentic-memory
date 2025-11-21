"""
Entity Resolution Service - Handles deduplication and merging of knowledge graph nodes.

Implements Pillar 1 of the optimization plan:
- Semantic Clustering (Vector-based Clustering)
- Janitor Agent (LLM-based conflict resolution)
"""

import structlog
from typing import List, Dict, Any, Tuple
import asyncio
from pydantic import BaseModel, Field

from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN, AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import asyncpg

from apps.memory_api.config import settings
from apps.memory_api.services.llm import get_llm_provider

logger = structlog.get_logger(__name__)

# Load embedding model lazily
_EMBEDDING_MODEL = None

def get_embedding_model():
    global _EMBEDDING_MODEL
    if _EMBEDDING_MODEL is None:
        # 'all-MiniLM-L6-v2' is small and fast
        _EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2')
    return _EMBEDDING_MODEL

class MergeDecision(BaseModel):
    should_merge: bool = Field(..., description="Whether the entities represent the same concept and should be merged.")
    canonical_name: str = Field(..., description="The canonical name to use for the merged entity.")
    reasoning: str = Field(..., description="Reasoning for the decision.")

class EntityResolutionService:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool
        self.llm_provider = get_llm_provider()
        self.similarity_threshold_high = 0.95
        self.similarity_threshold_low = 0.85

    async def run_clustering_and_merging(self, project_id: str, tenant_id: str):
        """
        Main entry point for the background task.
        1. Fetch all nodes for the project.
        2. Generate embeddings.
        3. Cluster.
        4. Merge or ask LLM.
        """
        logger.info("starting_entity_resolution", project_id=project_id, tenant_id=tenant_id)

        nodes = await self._fetch_nodes(project_id, tenant_id)
        if len(nodes) < 2:
            logger.info("not_enough_nodes_for_clustering", count=len(nodes))
            return

        # Prepare node labels for embedding
        node_labels = [n['label'] for n in nodes]
        node_ids = [n['id'] for n in nodes]

        # Generate embeddings (CPU based, fast for small models)
        model = get_embedding_model()
        # This is synchronous, running in a thread might be better if blocking event loop,
        # but for now we assume it's acceptable in a celery task or background job.
        # If running in async context, use run_in_executor
        loop = asyncio.get_running_loop()
        embeddings = await loop.run_in_executor(None, model.encode, node_labels)

        # Clustering
        # We can use DBSCAN or Agglomerative Clustering with cosine distance.
        # Cosine distance = 1 - cosine similarity.
        # Threshold 0.90 similarity corresponds to distance 0.10.

        # Let's use Agglomerative Clustering which is good for hierarchical or simple grouping
        # distance_threshold is 1 - similarity. So for 0.85 similarity, threshold is 0.15.
        # But we want to check high confidence merges automatically.

        # Strategy:
        # 1. Calculate pairwise similarity matrix.
        # 2. Iterate through pairs with similarity > threshold.
        # 3. Group them using a connected components approach (or just use pre-built clustering).

        # Using AgglomerativeClustering
        # dist_threshold = 1 - 0.85 = 0.15
        clustering = AgglomerativeClustering(
            n_clusters=None,
            metric='cosine',
            linkage='average',
            distance_threshold=1 - self.similarity_threshold_low
        )

        cluster_labels = await loop.run_in_executor(None, clustering.fit_predict, embeddings)

        # Group nodes by cluster
        clusters = {}
        for idx, label in enumerate(cluster_labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(idx)

        # Process clusters
        for cluster_id, indices in clusters.items():
            if len(indices) < 2:
                continue

            cluster_nodes = [nodes[i] for i in indices]
            cluster_embeddings = [embeddings[i] for i in indices]

            # Check similarity within cluster
            # If all pairs are > 0.95, merge automatically.
            # If some are between 0.85 and 0.95, ask LLM.

            await self._process_cluster(cluster_nodes, cluster_embeddings, project_id, tenant_id)

    async def _process_cluster(self, nodes: List[Dict], embeddings: List[Any], project_id: str, tenant_id: str):
        # Calculate min similarity in this cluster
        min_sim = 1.0
        # Check all pairs
        for i in range(len(embeddings)):
            for j in range(i + 1, len(embeddings)):
                sim = cosine_similarity([embeddings[i]], [embeddings[j]])[0][0]
                if sim < min_sim:
                    min_sim = sim

        names = [n['label'] for n in nodes]
        logger.info("processing_cluster", names=names, min_similarity=min_sim)

        if min_sim >= self.similarity_threshold_high:
            # Auto merge
            logger.info("auto_merging_cluster", names=names)
            await self._merge_nodes(nodes, project_id, tenant_id)
        elif min_sim >= self.similarity_threshold_low:
            # Ask Janitor Agent
            logger.info("asking_janitor_agent", names=names)
            decision = await self._ask_janitor(names)
            if decision.should_merge:
                await self._merge_nodes(nodes, project_id, tenant_id, canonical_name=decision.canonical_name)
            else:
                logger.info("janitor_rejected_merge", names=names, reason=decision.reasoning)

    async def _ask_janitor(self, names: List[str]) -> MergeDecision:
        prompt = f"""
        Analyze the following list of entity names from a knowledge graph:
        {names}

        Decide if these entities refer to the exact same concept/thing and should be merged.
        Examples:
        - "Apple Inc." and "Apple Company" -> Merge (True)
        - "Java" (island) and "Java" (language) -> Do NOT Merge (False)
        - "Jan Kowalski" and "Jan K." -> Likely Merge (True) if context supports it, but here assume Yes if it looks obvious.

        If they should be merged, choose the best canonical name (e.g. the most complete or formal one).
        """

        try:
            result = await self.llm_provider.generate_structured(
                system="You are the 'Janitor Agent' responsible for data quality in a knowledge graph.",
                prompt=prompt,
                model=settings.EXTRACTION_MODEL, # Cheap model
                response_model=MergeDecision
            )
            return result
        except Exception as e:
            logger.error("janitor_agent_failed", error=str(e))
            # Default to not merging if unsure
            return MergeDecision(should_merge=False, canonical_name="", reasoning="Error")

    async def _merge_nodes(self, nodes: List[Dict], project_id: str, tenant_id: str, canonical_name: str = None):
        """
        Merges multiple nodes into one.
        1. Pick a target node (or create new, but better to pick one to keep ID stable if possible).
        2. If canonical_name is provided, update target node.
        3. Rewire edges: Move edges from source nodes to target node.
        4. Delete source nodes.
        """
        if not nodes:
            return

        # Pick target node: The one with the canonical name if present, or the first one,
        # or the one with most edges (simplification: pick first or by length of label)

        if canonical_name:
            # Find if any node already has this name
            target_node = next((n for n in nodes if n['label'] == canonical_name), None)
            if not target_node:
                # Rename the first node
                target_node = nodes[0]
                # Update label in DB
                async with self.pool.acquire() as conn:
                    await conn.execute(
                        "UPDATE knowledge_graph_nodes SET label = $1 WHERE id = $2",
                        canonical_name, target_node['id']
                    )
        else:
             # Heuristic: longest name is usually more descriptive? Or shortest?
             # Let's pick longest.
             target_node = max(nodes, key=lambda n: len(n['label']))

        sources = [n for n in nodes if n['id'] != target_node['id']]

        async with self.pool.acquire() as conn:
            async with conn.transaction():
                for source in sources:
                    # Move outgoing edges: Update source_node_id to target_node['id']
                    await conn.execute(
                        """
                        UPDATE knowledge_graph_edges
                        SET source_node_id = $1
                        WHERE source_node_id = $2
                        ON CONFLICT DO NOTHING
                        """,
                        target_node['id'], source['id']
                    )

                    # Move incoming edges: Update target_node_id to target_node['id']
                    await conn.execute(
                        """
                        UPDATE knowledge_graph_edges
                        SET target_node_id = $1
                        WHERE target_node_id = $2
                        ON CONFLICT DO NOTHING
                        """,
                        target_node['id'], source['id']
                    )

                    # Delete source node (edges should be gone or moved, but ON CONFLICT DO NOTHING might leave some if duplicate edges existed.
                    # If ON CONFLICT DO NOTHING skipped update, it means the edge already existed on target.
                    # So we should delete the remaining edges on source before deleting node.)

                    await conn.execute("DELETE FROM knowledge_graph_edges WHERE source_node_id = $1 OR target_node_id = $1", source['id'])
                    await conn.execute("DELETE FROM knowledge_graph_nodes WHERE id = $1", source['id'])

        logger.info("nodes_merged", target=target_node['label'], merged_count=len(sources))

    async def _fetch_nodes(self, project_id: str, tenant_id: str) -> List[Dict]:
        async with self.pool.acquire() as conn:
            records = await conn.fetch(
                """
                SELECT id, node_id, label
                FROM knowledge_graph_nodes
                WHERE tenant_id = $1 AND project_id = $2
                """,
                tenant_id, project_id
            )
            return [dict(r) for r in records]
