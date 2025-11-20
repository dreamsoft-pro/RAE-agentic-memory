"""
Graph API endpoints for knowledge graph operations.

This module provides endpoints for:
- Extracting knowledge graphs from episodic memories
- Querying graph structures
- Retrieving graph statistics
- Managing graph nodes and edges
"""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Request, HTTPException, Query, Depends
from pydantic import BaseModel, Field

from apps.memory_api.dependencies import get_api_key
from apps.memory_api.services.graph_extraction import GraphExtractionResult, GraphTriple
from apps.memory_api.services.reflection_engine import ReflectionEngine
from apps.memory_api.services.hybrid_search import HybridSearchService, HybridSearchResult, TraversalStrategy
from apps.memory_api.metrics import memory_query_counter
import structlog

logger = structlog.get_logger(__name__)

router = APIRouter(
    prefix="/graph",
    tags=["knowledge-graph"],
    dependencies=[Depends(get_api_key)]
)


class GraphExtractionRequest(BaseModel):
    """Request model for graph extraction."""

    project_id: str = Field(..., description="Project identifier")
    limit: int = Field(default=50, ge=1, le=1000, description="Max memories to process")
    min_confidence: float = Field(default=0.5, ge=0.0, le=1.0, description="Minimum confidence threshold")
    auto_store: bool = Field(default=True, description="Automatically store extracted triples")


class HierarchicalReflectionRequest(BaseModel):
    """Request model for hierarchical reflection generation."""

    project_id: str = Field(..., description="Project identifier")
    bucket_size: int = Field(default=10, ge=2, le=100, description="Bucket size for hierarchical processing")
    max_episodes: Optional[int] = Field(default=None, description="Max episodes to process")


class HierarchicalReflectionResponse(BaseModel):
    """Response model for hierarchical reflection."""

    project_id: str
    summary: str
    episodes_processed: int


class GraphStatsResponse(BaseModel):
    """Response model for graph statistics."""

    project_id: str
    tenant_id: str
    total_nodes: int
    total_edges: int
    unique_relations: List[str]
    statistics: Dict[str, Any]


class GraphNodeResponse(BaseModel):
    """Response model for a single graph node."""

    id: str
    node_id: str
    label: str
    properties: Optional[Dict[str, Any]]
    created_at: str


class GraphEdgeResponse(BaseModel):
    """Response model for a single graph edge."""

    id: str
    source_node_id: str
    target_node_id: str
    relation: str
    properties: Optional[Dict[str, Any]]
    created_at: str


class GraphQueryResponse(BaseModel):
    """Response model for graph queries."""

    nodes: List[GraphNodeResponse]
    edges: List[GraphEdgeResponse]
    statistics: Dict[str, Any]


class GraphSearchRequest(BaseModel):
    """Request model for advanced graph search."""

    query: str = Field(..., description="Search query", min_length=1, max_length=1024)
    project_id: str = Field(..., description="Project identifier")
    top_k_vector: int = Field(default=5, ge=1, le=50, description="Number of vector search results")
    graph_depth: int = Field(default=2, ge=1, le=5, description="Maximum graph traversal depth")
    traversal_strategy: str = Field(
        default="bfs",
        description="Graph traversal strategy: 'bfs' or 'dfs'"
    )
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Optional search filters")


@router.post("/extract", response_model=GraphExtractionResult)
async def extract_knowledge_graph(
    req: GraphExtractionRequest,
    request: Request
):
    """
    Extract knowledge graph from episodic memories.

    This endpoint analyzes recent episodic memories and extracts:
    - Entities (nodes)
    - Relationships (edges)
    - Confidence scores
    - Metadata

    The extracted graph can be automatically stored in the database
    or returned for further processing.

    Args:
        req: Graph extraction request parameters
        request: FastAPI request object (for tenant context)

    Returns:
        GraphExtractionResult with triples, entities, and statistics

    Raises:
        HTTPException: If tenant header is missing or extraction fails
    """
    tenant_id = request.headers.get("X-Tenant-Id")
    if not tenant_id:
        raise HTTPException(status_code=400, detail="X-Tenant-Id header is required.")

    logger.info(
        "graph_extraction_requested",
        tenant_id=tenant_id,
        project_id=req.project_id,
        limit=req.limit
    )

    try:
        # Initialize reflection engine
        reflection_engine = ReflectionEngine(request.app.state.pool)

        # Perform enhanced graph extraction
        result = await reflection_engine.extract_knowledge_graph_enhanced(
            project=req.project_id,
            tenant_id=tenant_id,
            limit=req.limit,
            min_confidence=req.min_confidence,
            auto_store=req.auto_store
        )

        logger.info(
            "graph_extraction_completed",
            tenant_id=tenant_id,
            project_id=req.project_id,
            triples_count=len(result.triples)
        )

        return result

    except Exception as e:
        logger.exception(
            "graph_extraction_failed",
            tenant_id=tenant_id,
            project_id=req.project_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=500,
            detail=f"Graph extraction failed: {str(e)}"
        )


@router.post("/reflection/hierarchical", response_model=HierarchicalReflectionResponse)
async def generate_hierarchical_reflection(
    req: HierarchicalReflectionRequest,
    request: Request
):
    """
    Generate hierarchical (map-reduce) reflection from large episode collections.

    This endpoint handles large numbers of episodic memories by:
    1. Splitting them into manageable buckets
    2. Summarizing each bucket (Map phase)
    3. Recursively summarizing summaries (Reduce phase)

    This approach scales to thousands of episodes without hitting context limits.

    Args:
        req: Hierarchical reflection request parameters
        request: FastAPI request object (for tenant context)

    Returns:
        HierarchicalReflectionResponse with summary and statistics

    Raises:
        HTTPException: If tenant header is missing or reflection fails
    """
    tenant_id = request.headers.get("X-Tenant-Id")
    if not tenant_id:
        raise HTTPException(status_code=400, detail="X-Tenant-Id header is required.")

    logger.info(
        "hierarchical_reflection_requested",
        tenant_id=tenant_id,
        project_id=req.project_id
    )

    try:
        # Initialize reflection engine
        reflection_engine = ReflectionEngine(request.app.state.pool)

        # Generate hierarchical reflection
        summary = await reflection_engine.generate_hierarchical_reflection(
            project=req.project_id,
            tenant_id=tenant_id,
            bucket_size=req.bucket_size,
            max_episodes=req.max_episodes
        )

        # Get episode count for response
        async with request.app.state.pool.acquire() as conn:
            episode_count = await conn.fetchval(
                """
                SELECT COUNT(*) FROM memories
                WHERE tenant_id = $1 AND project = $2 AND layer = 'em'
                """,
                tenant_id,
                req.project_id
            )

        logger.info(
            "hierarchical_reflection_completed",
            tenant_id=tenant_id,
            project_id=req.project_id,
            episodes_processed=episode_count
        )

        return HierarchicalReflectionResponse(
            project_id=req.project_id,
            summary=summary,
            episodes_processed=episode_count or 0
        )

    except Exception as e:
        logger.exception(
            "hierarchical_reflection_failed",
            tenant_id=tenant_id,
            project_id=req.project_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=500,
            detail=f"Hierarchical reflection failed: {str(e)}"
        )


@router.get("/stats", response_model=GraphStatsResponse)
async def get_graph_statistics(
    request: Request,
    project_id: str = Query(..., description="Project identifier")
):
    """
    Get statistics about the knowledge graph for a project.

    Returns counts of nodes, edges, unique relations, and other metrics.

    Args:
        request: FastAPI request object (for tenant context)
        project_id: Project identifier

    Returns:
        GraphStatsResponse with comprehensive graph statistics

    Raises:
        HTTPException: If tenant header is missing or query fails
    """
    tenant_id = request.headers.get("X-Tenant-Id")
    if not tenant_id:
        raise HTTPException(status_code=400, detail="X-Tenant-Id header is required.")

    try:
        async with request.app.state.pool.acquire() as conn:
            # Get node count
            node_count = await conn.fetchval(
                """
                SELECT COUNT(*) FROM knowledge_graph_nodes
                WHERE tenant_id = $1 AND project_id = $2
                """,
                tenant_id,
                project_id
            )

            # Get edge count
            edge_count = await conn.fetchval(
                """
                SELECT COUNT(*) FROM knowledge_graph_edges
                WHERE tenant_id = $1 AND project_id = $2
                """,
                tenant_id,
                project_id
            )

            # Get unique relations
            relations = await conn.fetch(
                """
                SELECT DISTINCT relation FROM knowledge_graph_edges
                WHERE tenant_id = $1 AND project_id = $2
                ORDER BY relation
                """,
                tenant_id,
                project_id
            )

            unique_relations = [r['relation'] for r in relations]

            # Additional statistics
            statistics = {
                "avg_edges_per_node": round(edge_count / node_count, 2) if node_count > 0 else 0,
                "total_relation_types": len(unique_relations)
            }

            return GraphStatsResponse(
                project_id=project_id,
                tenant_id=tenant_id,
                total_nodes=node_count or 0,
                total_edges=edge_count or 0,
                unique_relations=unique_relations,
                statistics=statistics
            )

    except Exception as e:
        logger.exception(
            "graph_stats_failed",
            tenant_id=tenant_id,
            project_id=project_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve graph statistics: {str(e)}"
        )


@router.get("/nodes", response_model=List[GraphNodeResponse])
async def get_graph_nodes(
    request: Request,
    project_id: str = Query(..., description="Project identifier"),
    limit: int = Query(default=100, ge=1, le=1000, description="Max nodes to return"),
    use_pagerank: bool = Query(
        default=False,
        description="Use PageRank to filter most important nodes (recommended for large graphs)"
    ),
    min_pagerank_score: float = Query(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Minimum PageRank score to include (only used with use_pagerank=true)"
    )
):
    """
    Retrieve graph nodes for a project.

    For large graphs (500+ nodes), use `use_pagerank=true` to filter
    by node importance. This prevents UI rendering issues by showing
    only the most important/central entities.

    Args:
        request: FastAPI request object (for tenant context)
        project_id: Project identifier
        limit: Maximum number of nodes to return
        use_pagerank: Enable PageRank filtering for large graphs
        min_pagerank_score: Minimum PageRank threshold

    Returns:
        List of GraphNodeResponse objects ordered by importance

    Raises:
        HTTPException: If tenant header is missing or query fails
    """
    tenant_id = request.headers.get("X-Tenant-Id")
    if not tenant_id:
        raise HTTPException(status_code=400, detail="X-Tenant-Id header is required.")

    try:
        if use_pagerank:
            # Import here to avoid circular dependency
            from apps.memory_api.services.graph_algorithms import GraphAlgorithmsService
            from uuid import UUID

            # Calculate PageRank scores
            graph_service = GraphAlgorithmsService(db=request.app.state.pool)
            pagerank_scores = await graph_service.pagerank(
                tenant_id=UUID(tenant_id) if isinstance(tenant_id, str) else tenant_id,
                project_id=project_id
            )

            if not pagerank_scores:
                logger.warning(
                    "pagerank_returned_empty",
                    tenant_id=tenant_id,
                    project_id=project_id
                )
                # Fall back to regular query
                use_pagerank = False

            else:
                # Filter nodes by PageRank score
                filtered_node_ids = [
                    node_id for node_id, score in pagerank_scores.items()
                    if score >= min_pagerank_score
                ]

                # Sort by PageRank score descending
                sorted_node_ids = sorted(
                    filtered_node_ids,
                    key=lambda nid: pagerank_scores[nid],
                    reverse=True
                )[:limit]

                logger.info(
                    "pagerank_filtering_applied",
                    tenant_id=tenant_id,
                    project_id=project_id,
                    total_nodes=len(pagerank_scores),
                    filtered_nodes=len(filtered_node_ids),
                    returned_nodes=len(sorted_node_ids)
                )

                # Fetch filtered nodes from database
                async with request.app.state.pool.acquire() as conn:
                    nodes = []
                    for node_id in sorted_node_ids:
                        node = await conn.fetchrow(
                            """
                            SELECT id, node_id, label, properties, created_at
                            FROM knowledge_graph_nodes
                            WHERE id = $1::uuid
                            """,
                            node_id
                        )
                        if node:
                            nodes.append(node)

                return [
                    GraphNodeResponse(
                        id=str(node['id']),
                        node_id=node['node_id'],
                        label=node['label'],
                        properties={
                            **(node['properties'] or {}),
                            "pagerank_score": round(pagerank_scores.get(str(node['id']), 0.0), 6)
                        },
                        created_at=str(node['created_at'])
                    )
                    for node in nodes
                ]

        # Regular query without PageRank filtering
        async with request.app.state.pool.acquire() as conn:
            nodes = await conn.fetch(
                """
                SELECT id, node_id, label, properties, created_at
                FROM knowledge_graph_nodes
                WHERE tenant_id = $1 AND project_id = $2
                ORDER BY created_at DESC
                LIMIT $3
                """,
                tenant_id,
                project_id,
                limit
            )

            return [
                GraphNodeResponse(
                    id=str(node['id']),
                    node_id=node['node_id'],
                    label=node['label'],
                    properties=node['properties'],
                    created_at=str(node['created_at'])
                )
                for node in nodes
            ]

    except Exception as e:
        logger.exception(
            "get_nodes_failed",
            tenant_id=tenant_id,
            project_id=project_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve graph nodes: {str(e)}"
        )


@router.get("/edges", response_model=List[GraphEdgeResponse])
async def get_graph_edges(
    request: Request,
    project_id: str = Query(..., description="Project identifier"),
    limit: int = Query(default=100, ge=1, le=1000, description="Max edges to return"),
    relation: Optional[str] = Query(default=None, description="Filter by relation type")
):
    """
    Retrieve graph edges for a project.

    Args:
        request: FastAPI request object (for tenant context)
        project_id: Project identifier
        limit: Maximum number of edges to return
        relation: Optional filter by relation type

    Returns:
        List of GraphEdgeResponse objects

    Raises:
        HTTPException: If tenant header is missing or query fails
    """
    tenant_id = request.headers.get("X-Tenant-Id")
    if not tenant_id:
        raise HTTPException(status_code=400, detail="X-Tenant-Id header is required.")

    try:
        async with request.app.state.pool.acquire() as conn:
            if relation:
                edges = await conn.fetch(
                    """
                    SELECT id, source_node_id, target_node_id, relation, properties, created_at
                    FROM knowledge_graph_edges
                    WHERE tenant_id = $1 AND project_id = $2 AND relation = $3
                    ORDER BY created_at DESC
                    LIMIT $4
                    """,
                    tenant_id,
                    project_id,
                    relation,
                    limit
                )
            else:
                edges = await conn.fetch(
                    """
                    SELECT id, source_node_id, target_node_id, relation, properties, created_at
                    FROM knowledge_graph_edges
                    WHERE tenant_id = $1 AND project_id = $2
                    ORDER BY created_at DESC
                    LIMIT $3
                    """,
                    tenant_id,
                    project_id,
                    limit
                )

            return [
                GraphEdgeResponse(
                    id=str(edge['id']),
                    source_node_id=str(edge['source_node_id']),
                    target_node_id=str(edge['target_node_id']),
                    relation=edge['relation'],
                    properties=edge['properties'],
                    created_at=str(edge['created_at'])
                )
                for edge in edges
            ]

    except Exception as e:
        logger.exception(
            "get_edges_failed",
            tenant_id=tenant_id,
            project_id=project_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve graph edges: {str(e)}"
        )


@router.post("/query", response_model=HybridSearchResult)
async def query_knowledge_graph(
    req: GraphSearchRequest,
    request: Request
):
    """
    Advanced knowledge graph search with hybrid retrieval.

    This endpoint provides the most comprehensive search capabilities by:
    1. Performing semantic vector search to find relevant memories
    2. Mapping results to knowledge graph entities
    3. Traversing the graph to discover related entities and relationships
    4. Synthesizing all information into coherent context

    This is ideal for:
    - Exploring complex relationships between entities
    - Discovering indirect connections
    - Building comprehensive context for AI agents
    - Understanding project structure and dependencies

    Args:
        req: Graph search request parameters
        request: FastAPI request object (for tenant context)

    Returns:
        HybridSearchResult with vector matches, graph data, and synthesized context

    Raises:
        HTTPException: If tenant header is missing or search fails
    """
    tenant_id = request.headers.get("X-Tenant-Id")
    if not tenant_id:
        raise HTTPException(status_code=400, detail="X-Tenant-Id header is required.")

    # Validate traversal strategy
    try:
        strategy = TraversalStrategy(req.traversal_strategy.lower())
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid traversal_strategy. Must be 'bfs' or 'dfs', got '{req.traversal_strategy}'"
        )

    logger.info(
        "graph_query_requested",
        tenant_id=tenant_id,
        project_id=req.project_id,
        query=req.query,
        graph_depth=req.graph_depth,
        strategy=strategy.value
    )

    try:
        # Initialize hybrid search service
        hybrid_search = HybridSearchService(request.app.state.pool)

        # Perform comprehensive hybrid search
        result = await hybrid_search.search(
            query=req.query,
            tenant_id=tenant_id,
            project_id=req.project_id,
            top_k_vector=req.top_k_vector,
            graph_depth=req.graph_depth,
            traversal_strategy=strategy,
            use_graph=True,
            filters=req.filters
        )

        logger.info(
            "graph_query_completed",
            tenant_id=tenant_id,
            project_id=req.project_id,
            vector_results=len(result.vector_matches),
            graph_nodes=len(result.graph_nodes),
            graph_edges=len(result.graph_edges)
        )

        # Update metrics
        memory_query_counter.labels(tenant_id=tenant_id).inc()

        return result

    except Exception as e:
        logger.exception(
            "graph_query_failed",
            tenant_id=tenant_id,
            project_id=req.project_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=500,
            detail=f"Graph query failed: {str(e)}"
        )


@router.get("/subgraph", response_model=GraphQueryResponse)
async def get_subgraph(
    request: Request,
    project_id: str = Query(..., description="Project identifier"),
    node_ids: str = Query(..., description="Comma-separated node IDs to start from"),
    depth: int = Query(default=1, ge=1, le=5, description="Traversal depth")
):
    """
    Retrieve a subgraph starting from specific nodes.

    This endpoint is useful for:
    - Visualizing local graph neighborhoods
    - Exploring entity relationships
    - Building graph visualizations

    Args:
        request: FastAPI request object (for tenant context)
        project_id: Project identifier
        node_ids: Comma-separated list of starting node IDs
        depth: Maximum traversal depth

    Returns:
        GraphQueryResponse with nodes and edges in the subgraph

    Raises:
        HTTPException: If tenant header is missing or query fails
    """
    tenant_id = request.headers.get("X-Tenant-Id")
    if not tenant_id:
        raise HTTPException(status_code=400, detail="X-Tenant-Id header is required.")

    # Parse node IDs
    start_nodes = [n.strip() for n in node_ids.split(",") if n.strip()]

    if not start_nodes:
        raise HTTPException(status_code=400, detail="At least one node_id is required")

    logger.info(
        "subgraph_requested",
        tenant_id=tenant_id,
        project_id=project_id,
        start_nodes=start_nodes,
        depth=depth
    )

    try:
        # Initialize hybrid search for graph traversal
        hybrid_search = HybridSearchService(request.app.state.pool)

        # Perform graph traversal
        nodes, edges = await hybrid_search._traverse_bfs(
            start_node_ids=start_nodes,
            tenant_id=tenant_id,
            project_id=project_id,
            max_depth=depth
        )

        # Convert to response format
        node_responses = []
        async with request.app.state.pool.acquire() as conn:
            for node in nodes:
                # Get full node data
                node_data = await conn.fetchrow(
                    """
                    SELECT id, node_id, label, properties, created_at
                    FROM knowledge_graph_nodes
                    WHERE id = $1::uuid
                    """,
                    node.id
                )

                if node_data:
                    node_responses.append(GraphNodeResponse(
                        id=str(node_data['id']),
                        node_id=node_data['node_id'],
                        label=node_data['label'],
                        properties=node_data['properties'],
                        created_at=str(node_data['created_at'])
                    ))

        edge_responses = []
        async with request.app.state.pool.acquire() as conn:
            for edge in edges:
                # Get full edge data
                edge_data = await conn.fetchrow(
                    """
                    SELECT id, source_node_id, target_node_id, relation, properties, created_at
                    FROM knowledge_graph_edges
                    WHERE source_node_id = $1::uuid AND target_node_id = $2::uuid
                    """,
                    edge.source_id,
                    edge.target_id
                )

                if edge_data:
                    edge_responses.append(GraphEdgeResponse(
                        id=str(edge_data['id']),
                        source_node_id=str(edge_data['source_node_id']),
                        target_node_id=str(edge_data['target_node_id']),
                        relation=edge_data['relation'],
                        properties=edge_data['properties'],
                        created_at=str(edge_data['created_at'])
                    ))

        statistics = {
            "start_nodes": len(start_nodes),
            "depth": depth,
            "nodes_found": len(node_responses),
            "edges_found": len(edge_responses)
        }

        logger.info(
            "subgraph_retrieved",
            tenant_id=tenant_id,
            project_id=project_id,
            statistics=statistics
        )

        return GraphQueryResponse(
            nodes=node_responses,
            edges=edge_responses,
            statistics=statistics
        )

    except Exception as e:
        logger.exception(
            "subgraph_failed",
            tenant_id=tenant_id,
            project_id=project_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve subgraph: {str(e)}"
        )
