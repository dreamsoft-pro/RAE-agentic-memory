"""
Hybrid Search Service - Enterprise-grade search combining vector similarity and graph traversal.

This module implements advanced hybrid search capabilities that merge:
- Vector similarity search (semantic search)
- Knowledge graph traversal (relationship-based discovery)
- Context synthesis (merging results into coherent context)
- Relevance reranking (scoring combined results)

This approach provides richer, more contextual search results by leveraging
both the semantic similarity of content and the structural relationships
between entities in the knowledge graph.
"""

from typing import List, Dict, Any, Optional, Set, Tuple
from pydantic import BaseModel, Field
import asyncpg
import structlog

from apps.memory_api.services.vector_store import get_vector_store
from apps.memory_api.services.embedding import get_embedding_service
from apps.memory_api.models import ScoredMemoryRecord
from apps.memory_api.models.graph import GraphNode, GraphEdge, TraversalStrategy
from apps.memory_api.repositories.graph_repository import GraphRepository

logger = structlog.get_logger(__name__)


class HybridSearchResult(BaseModel):
    """Complete result from hybrid search operation."""

    vector_matches: List[ScoredMemoryRecord] = Field(
        default_factory=list,
        description="Results from vector similarity search"
    )
    graph_nodes: List[GraphNode] = Field(
        default_factory=list,
        description="Nodes discovered via graph traversal"
    )
    graph_edges: List[GraphEdge] = Field(
        default_factory=list,
        description="Edges discovered via graph traversal"
    )
    synthesized_context: str = Field(
        default="",
        description="Merged context from all sources"
    )
    graph_enabled: bool = Field(
        default=False,
        description="Whether graph traversal was enabled for this search"
    )
    statistics: Dict[str, Any] = Field(
        default_factory=dict,
        description="Search statistics"
    )


class HybridSearchService:
    """
    Enterprise-grade hybrid search service.

    Combines vector similarity search with knowledge graph traversal to provide
    comprehensive, context-rich search results.

    Features:
    - Configurable search strategies
    - Multiple traversal algorithms (BFS/DFS)
    - Context synthesis from multiple sources
    - Performance metrics and logging
    - Relevance scoring
    """

    def __init__(self, pool: asyncpg.Pool):
        """
        Initialize hybrid search service.

        Args:
            pool: AsyncPG connection pool for database operations
        """
        self.pool = pool
        self.embedding_service = get_embedding_service()
        self.graph_repository = GraphRepository(pool)

    async def search(
        self,
        query: str,
        tenant_id: str,
        project_id: str,
        top_k_vector: int = 5,
        graph_depth: int = 2,
        traversal_strategy: TraversalStrategy = TraversalStrategy.BFS,
        use_graph: bool = True,
        filters: Optional[Dict[str, Any]] = None
    ) -> HybridSearchResult:
        """
        Perform hybrid search combining vector similarity and graph traversal.

        Process:
        1. Vector search - find semantically similar memories
        2. Map memories to graph nodes
        3. Graph traversal - discover related entities
        4. Context synthesis - merge all information
        5. Relevance ranking - score and order results

        Args:
            query: Search query text
            tenant_id: Tenant identifier
            project_id: Project identifier
            top_k_vector: Number of vector search results (default: 5)
            graph_depth: Maximum graph traversal depth (default: 2)
            traversal_strategy: BFS or DFS traversal (default: BFS)
            use_graph: Enable graph traversal (default: True)
            filters: Optional filters for vector search

        Returns:
            HybridSearchResult with vector matches, graph data, and synthesized context

        Raises:
            RuntimeError: If search operation fails
        """
        logger.info(
            "hybrid_search_started",
            tenant_id=tenant_id,
            project_id=project_id,
            query_length=len(query),
            use_graph=use_graph
        )

        try:
            # Phase 1: Vector similarity search
            vector_results = await self._vector_search(
                query=query,
                tenant_id=tenant_id,
                project_id=project_id,
                top_k=top_k_vector,
                filters=filters
            )

            logger.info(
                "vector_search_completed",
                results_count=len(vector_results)
            )

            # If graph traversal disabled, return vector results only
            if not use_graph:
                synthesized = self._synthesize_vector_only(vector_results)
                return HybridSearchResult(
                    vector_matches=vector_results,
                    synthesized_context=synthesized,
                    graph_enabled=False,
                    statistics={
                        "vector_results": len(vector_results)
                    }
                )

            # Phase 2: Map vector results to graph nodes
            start_node_ids = await self._map_memories_to_nodes(
                memory_results=vector_results,
                tenant_id=tenant_id,
                project_id=project_id
            )

            logger.info(
                "mapped_to_graph_nodes",
                start_nodes_count=len(start_node_ids)
            )

            # If no graph nodes found, return vector results only
            if not start_node_ids:
                synthesized = self._synthesize_vector_only(vector_results)
                return HybridSearchResult(
                    vector_matches=vector_results,
                    synthesized_context=synthesized,
                    graph_enabled=True,
                    statistics={
                        "vector_results": len(vector_results),
                        "graph_nodes_found": 0
                    }
                )

            # Phase 3: Graph traversal
            graph_nodes, graph_edges = await self._traverse_graph(
                start_node_ids=start_node_ids,
                tenant_id=tenant_id,
                project_id=project_id,
                depth=graph_depth,
                strategy=traversal_strategy
            )

            logger.info(
                "graph_traversal_completed",
                nodes_discovered=len(graph_nodes),
                edges_discovered=len(graph_edges)
            )

            # Phase 4: Context synthesis
            synthesized_context = await self._synthesize_context(
                vector_results=vector_results,
                graph_nodes=graph_nodes,
                graph_edges=graph_edges,
                query=query
            )

            # Phase 5: Compile statistics
            statistics = {
                "vector_results": len(vector_results),
                "graph_nodes": len(graph_nodes),
                "graph_edges": len(graph_edges),
                "graph_depth": graph_depth,
                "traversal_strategy": traversal_strategy.value,
                "context_length": len(synthesized_context)
            }

            logger.info(
                "hybrid_search_completed",
                tenant_id=tenant_id,
                project_id=project_id,
                statistics=statistics
            )

            return HybridSearchResult(
                vector_matches=vector_results,
                graph_nodes=graph_nodes,
                graph_edges=graph_edges,
                synthesized_context=synthesized_context,
                graph_enabled=True,
                statistics=statistics
            )

        except Exception as e:
            logger.exception(
                "hybrid_search_failed",
                tenant_id=tenant_id,
                project_id=project_id,
                error=str(e)
            )
            raise RuntimeError(f"Hybrid search failed: {e}")

    async def _vector_search(
        self,
        query: str,
        tenant_id: str,
        project_id: str,
        top_k: int,
        filters: Optional[Dict[str, Any]]
    ) -> List[ScoredMemoryRecord]:
        """
        Perform vector similarity search.

        Args:
            query: Search query
            tenant_id: Tenant identifier
            project_id: Project identifier
            top_k: Number of results
            filters: Optional search filters

        Returns:
            List of scored memory records
        """
        # Generate query embedding
        query_embedding = self.embedding_service.generate_embeddings([query])[0]

        # Build filters
        query_filters = {
            "must": [
                {"key": "tenant_id", "match": {"value": tenant_id}},
                {"key": "project", "match": {"value": project_id}}
            ]
        }

        if filters:
            for key, value in filters.items():
                if key == "tags" and isinstance(value, list):
                    query_filters["must"].append({"key": "tags", "match": {"any": value}})

        # Query vector store
        vector_store = get_vector_store(pool=self.pool)
        results = await vector_store.query(
            query_embedding=query_embedding,
            top_k=top_k,
            filters=query_filters
        )

        # --- Pillar 2 Implementation: Hybrid Search with Super-Nodes ---
        # Search specifically for "community" nodes (Super-Nodes) in the graph
        # that might be relevant to the query.
        # This is a basic implementation that text-matches the query against super-node labels/summaries.
        # Ideally, Super-Nodes should also have vector embeddings in a separate collection or marked index.
        # For now, we search for them using SQL fuzzy match or just append them if found in the vector results
        # (if vector store indexes graph nodes too).

        # Assumption: "Super-Nodes" are stored in knowledge_graph_nodes with type='community'.
        # We perform a side-query to DB to find relevant communities.

        # Note: This is an additive search step.
        relevant_communities = await self._find_relevant_communities(query, tenant_id, project_id)

        # Create synthetic memory records for these communities so they are included in the synthesis
        for comm in relevant_communities:
            # Check if this community is already in results (unlikely if vector store doesn't index them)
            # Create a high-scoring record
            synthetic_record = ScoredMemoryRecord(
                id=str(comm['id']),
                content=f"COMMUNITY WISDOM: {comm['label']}. Summary: {comm['properties'].get('summary', '')}",
                score=0.95, # Give high priority to wisdom
                source="community_wisdom",
                tags=["wisdom", "community"],
                metadata=comm['properties']
            )
            # Prepend to results
            results.insert(0, synthetic_record)

        return results

    async def _find_relevant_communities(self, query: str, tenant_id: str, project_id: str) -> List[Dict]:
        """
        Find community nodes relevant to the query.

        Delegates to GraphRepository for database access.
        """
        return await self.graph_repository.find_relevant_communities(
            query=query,
            tenant_id=tenant_id,
            project_id=project_id,
            limit=3
        )

    async def _map_memories_to_nodes(
        self,
        memory_results: List[ScoredMemoryRecord],
        tenant_id: str,
        project_id: str
    ) -> List[str]:
        """
        Map memory content to knowledge graph nodes.

        This attempts to find graph nodes that correspond to the
        content of retrieved memories by matching entity names.

        Delegates to GraphRepository for database access.

        Args:
            memory_results: Vector search results
            tenant_id: Tenant identifier
            project_id: Project identifier

        Returns:
            List of node IDs to use as traversal starting points
        """
        if not memory_results:
            return []

        # Find nodes linked to these memories through content matching
        node_ids = []

        for memory in memory_results:
            # Look for nodes that match entities mentioned in the memory
            matched_nodes = await self.graph_repository.find_nodes_by_content_match(
                content=memory.content,
                tenant_id=tenant_id,
                project_id=project_id,
                limit=5
            )
            node_ids.extend(matched_nodes)

        # Return unique node IDs
        return list(set(node_ids))

    async def _traverse_graph(
        self,
        start_node_ids: List[str],
        tenant_id: str,
        project_id: str,
        depth: int,
        strategy: TraversalStrategy
    ) -> Tuple[List[GraphNode], List[GraphEdge]]:
        """
        Traverse the knowledge graph starting from given nodes.

        Delegates to GraphRepository for actual graph traversal operations.

        Args:
            start_node_ids: Starting node IDs
            tenant_id: Tenant identifier
            project_id: Project identifier
            depth: Maximum traversal depth
            strategy: Traversal strategy (BFS or DFS)

        Returns:
            Tuple of (discovered nodes, discovered edges)
        """
        if strategy == TraversalStrategy.BFS:
            return await self.graph_repository.traverse_graph_bfs(
                start_node_ids, tenant_id, project_id, depth
            )
        else:
            return await self.graph_repository.traverse_graph_dfs(
                start_node_ids, tenant_id, project_id, depth
            )

    async def _synthesize_context(
        self,
        vector_results: List[ScoredMemoryRecord],
        graph_nodes: List[GraphNode],
        graph_edges: List[GraphEdge],
        query: str
    ) -> str:
        """
        Synthesize unified context from vector and graph results.

        Args:
            vector_results: Vector search results
            graph_nodes: Discovered graph nodes
            graph_edges: Discovered graph edges
            query: Original search query

        Returns:
            Synthesized context string
        """
        context_parts = []

        # Section 1: Query context
        context_parts.append(f"# Search Query\n{query}\n")

        # Section 2: Vector search results
        if vector_results:
            context_parts.append("# Relevant Memories (Vector Search)\n")
            for i, result in enumerate(vector_results, 1):
                context_parts.append(
                    f"{i}. [Score: {result.score:.3f}] {result.content}\n"
                    f"   Source: {result.source} | Tags: {', '.join(result.tags or [])}\n"
                )

        # Section 3: Knowledge graph context
        if graph_nodes:
            context_parts.append("\n# Related Entities (Knowledge Graph)\n")

            # Group nodes by depth
            nodes_by_depth: Dict[int, List[GraphNode]] = {}
            for node in graph_nodes:
                depth = node.depth
                if depth not in nodes_by_depth:
                    nodes_by_depth[depth] = []
                nodes_by_depth[depth].append(node)

            for depth in sorted(nodes_by_depth.keys()):
                context_parts.append(f"\nDepth {depth}:\n")
                for node in nodes_by_depth[depth]:
                    context_parts.append(f"  - {node.label}\n")

        # Section 4: Relationships
        if graph_edges:
            context_parts.append("\n# Relationships\n")

            # Group edges by relation type
            edges_by_relation: Dict[str, List[GraphEdge]] = {}
            for edge in graph_edges:
                relation = edge.relation
                if relation not in edges_by_relation:
                    edges_by_relation[relation] = []
                edges_by_relation[relation].append(edge)

            for relation, edges in edges_by_relation.items():
                context_parts.append(f"\n{relation}:\n")
                for edge in edges[:10]:  # Limit to 10 per relation
                    # Find node labels
                    source_node = next(
                        (n for n in graph_nodes if n.id == edge.source_id),
                        None
                    )
                    target_node = next(
                        (n for n in graph_nodes if n.id == edge.target_id),
                        None
                    )

                    if source_node and target_node:
                        context_parts.append(
                            f"  {source_node.label} → {target_node.label}\n"
                        )

        return "\n".join(context_parts)

    def _synthesize_vector_only(
        self,
        vector_results: List[ScoredMemoryRecord]
    ) -> str:
        """
        Synthesize context from vector results only.

        Args:
            vector_results: Vector search results

        Returns:
            Synthesized context string
        """
        if not vector_results:
            return "No results found."

        context_parts = ["# Search Results\n"]

        for i, result in enumerate(vector_results, 1):
            context_parts.append(
                f"{i}. [Score: {result.score:.3f}] {result.content}\n"
                f"   Source: {result.source} | Tags: {', '.join(result.tags or [])}\n"
            )

        return "\n".join(context_parts)
