"""
Hybrid Search Service - Multi-Strategy Search with Dynamic Weighting

This service orchestrates multiple search strategies and combines results:
- Vector similarity search
- Semantic node search
- Graph traversal search
- Full-text search
- LLM re-ranking

Includes:
- Query analysis for intent classification
- Dynamic weight calculation
- Result fusion and normalization
- LLM-based re-ranking
"""

from datetime import datetime
from typing import Any, Dict, List

import asyncpg
import structlog

from apps.memory_api.models.hybrid_search_models import (
    HybridSearchResult,
    QueryAnalysis,
    RerankingModel,
    SearchResultItem,
    SearchStrategy,
)
from apps.memory_api.repositories.token_savings_repository import TokenSavingsRepository
from apps.memory_api.services.hybrid_cache import get_hybrid_cache
from apps.memory_api.services.llm import get_llm_provider
from apps.memory_api.services.ml_service_client import MLServiceClient
from apps.memory_api.services.query_analyzer import QueryAnalyzer
from apps.memory_api.services.token_savings_service import TokenSavingsService

logger = structlog.get_logger(__name__)


# ============================================================================
# LLM Re-ranking Prompt
# ============================================================================

RERANKING_PROMPT = """You are a search result re-ranking expert. Re-rank the following search results based on relevance to the query.

Query: "{query}"

Results:
{results}

Your task:
1. Evaluate each result's relevance to the query
2. Assign a relevance score from 0.0 to 1.0 (higher = more relevant)
3. Consider:
   - Semantic relevance
   - Contextual fit
   - Completeness of information
   - Recency if applicable

Return a JSON array with scores:
[
  {{"index": 0, "score": 0.95, "reason": "Directly answers the query"}},
  {{"index": 1, "score": 0.75, "reason": "Partially relevant"}},
  ...
]
"""


# ============================================================================
# Hybrid Search Service
# ============================================================================


class HybridSearchService:
    """
    Enterprise hybrid search combining multiple strategies.

    Features:
    - Multi-strategy search (vector, semantic, graph, fulltext)
    - Query analysis and intent classification
    - Dynamic weight calculation
    - Result fusion with normalization
    - LLM re-ranking
    """

    def __init__(self, pool: asyncpg.Pool, enable_cache: bool = True):
        """
        Initialize hybrid search service.

        Args:
            pool: Database connection pool
            enable_cache: Enable result caching (default: True)
        """
        self.pool = pool
        self.query_analyzer = QueryAnalyzer()
        self.ml_client = MLServiceClient()
        self.llm_provider = get_llm_provider()
        self.enable_cache = enable_cache
        self.cache = get_hybrid_cache() if enable_cache else None
        self.savings_service = TokenSavingsService(TokenSavingsRepository(pool))

    async def search(
        self,
        tenant_id: str,
        project_id: str,
        query: str,
        k: int = 10,
        enable_vector: bool = True,
        enable_semantic: bool = True,
        enable_graph: bool = True,
        enable_fulltext: bool = True,
        enable_reranking: bool = True,
        reranking_model: RerankingModel = RerankingModel.CLAUDE_HAIKU,
        manual_weights: Dict[str, float] = None,
        temporal_filter: datetime = None,
        tag_filter: List[str] = None,
        min_importance: float = None,
        graph_max_depth: int = 3,
        conversation_history: List[str] = None,
        bypass_cache: bool = False,
    ) -> HybridSearchResult:
        """
        Execute hybrid multi-strategy search.

        Args:
            tenant_id: Tenant identifier
            project_id: Project identifier
            query: Search query
            k: Number of results
            enable_vector: Enable vector search
            enable_semantic: Enable semantic search
            enable_graph: Enable graph search
            enable_fulltext: Enable full-text search
            enable_reranking: Enable LLM re-ranking
            reranking_model: Model for re-ranking
            manual_weights: Manual weight override
            temporal_filter: Time-based filter
            tag_filter: Tag filter
            min_importance: Minimum importance score
            graph_max_depth: Max depth for graph traversal
            conversation_history: Conversation context
            bypass_cache: Bypass cache and force fresh search

        Returns:
            HybridSearchResult with combined results
        """
        import time

        start_time = time.time()

        logger.info("hybrid_search_started", tenant_id=tenant_id, query=query, k=k)

        # Check cache if enabled
        if self.enable_cache and not bypass_cache:
            cache_filters = {
                "k": k,
                "enable_vector": enable_vector,
                "enable_semantic": enable_semantic,
                "enable_graph": enable_graph,
                "enable_fulltext": enable_fulltext,
                "enable_reranking": enable_reranking,
                "temporal_filter": (
                    temporal_filter.isoformat() if temporal_filter else None
                ),
                "tag_filter": tag_filter,
                "min_importance": min_importance,
            }

            cached_result = await self.cache.get(
                query=query,
                tenant_id=tenant_id,
                project_id=project_id,
                filters=cache_filters,
            )

            if cached_result:
                logger.info("returning_cached_result", tenant_id=tenant_id)

                # Track token savings
                # Estimate: Query Analysis (~300) + Reranking (~k * 200 if enabled)
                predicted_tokens = 300
                if enable_reranking:
                    predicted_tokens += k * 200

                await self.savings_service.track_savings(
                    tenant_id=tenant_id,
                    project_id=project_id,
                    model="claude-3-haiku",
                    predicted_tokens=predicted_tokens,
                    real_tokens=0,
                    savings_type="cache",
                )

                return HybridSearchResult(**cached_result)

        # Stage 1: Query Analysis
        analysis_start = time.time()
        if manual_weights:
            # Skip analysis if manual weights provided
            query_analysis = QueryAnalysis(
                intent="exploratory",  # Default
                confidence=1.0,
                key_entities=[],
                key_concepts=[],
                temporal_markers=[],
                relation_types=[],
                recommended_strategies=[],
                strategy_weights=manual_weights,
                original_query=query,
            )
        else:
            query_analysis = await self.query_analyzer.analyze_query(
                query=query, context=conversation_history
            )

        analysis_time = int((time.time() - analysis_start) * 1000)

        # Stage 2: Calculate weights
        if manual_weights:
            weights = {SearchStrategy(k): v for k, v in manual_weights.items()}
        else:
            weights = await self.query_analyzer.calculate_dynamic_weights(
                query_analysis
            )

        logger.info(
            "weights_calculated", weights={k.value: v for k, v in weights.items()}
        )

        # Stage 3: Execute searches in parallel
        search_start = time.time()
        results_by_strategy = {}

        # Vector search
        if enable_vector and weights.get(SearchStrategy.VECTOR, 0) > 0:
            vector_results = await self._vector_search(
                tenant_id,
                project_id,
                query,
                k * 3,
                temporal_filter,
                tag_filter,
                min_importance,
            )
            results_by_strategy[SearchStrategy.VECTOR] = vector_results

        # Semantic search
        if enable_semantic and weights.get(SearchStrategy.SEMANTIC, 0) > 0:
            semantic_results = await self._semantic_search(
                tenant_id, project_id, query, k * 2, query_analysis.key_concepts
            )
            results_by_strategy[SearchStrategy.SEMANTIC] = semantic_results

        # Graph search
        if enable_graph and weights.get(SearchStrategy.GRAPH, 0) > 0:
            if query_analysis.requires_graph_traversal or enable_graph:
                graph_results = await self._graph_search(
                    tenant_id,
                    project_id,
                    query,
                    query_analysis.key_entities,
                    graph_max_depth,
                    k * 2,
                )
                results_by_strategy[SearchStrategy.GRAPH] = graph_results

        # Full-text search
        if enable_fulltext and weights.get(SearchStrategy.FULLTEXT, 0) > 0:
            fulltext_results = await self._fulltext_search(
                tenant_id, project_id, query, k * 2, temporal_filter, tag_filter
            )
            results_by_strategy[SearchStrategy.FULLTEXT] = fulltext_results

        search_time = int((time.time() - search_start) * 1000)

        # Stage 4: Fuse results
        fused_results = self._fuse_results(results_by_strategy, weights, k * 2)

        # Stage 5: LLM Re-ranking (optional)
        reranking_time = None
        if enable_reranking and len(fused_results) > 0:
            rerank_start = time.time()
            reranked_results = await self._rerank_results(
                query, fused_results[: k * 2], reranking_model
            )
            fused_results = reranked_results
            reranking_time = int((time.time() - rerank_start) * 1000)

        # Stage 6: Final ranking and truncation
        final_results = fused_results[:k]

        # Assign final ranks
        for idx, result in enumerate(final_results):
            result.rank = idx + 1

        total_time = int((time.time() - start_time) * 1000)

        logger.info(
            "hybrid_search_complete",
            results=len(final_results),
            total_time=total_time,
            analysis_time=analysis_time,
            search_time=search_time,
            reranking_time=reranking_time,
        )

        result = HybridSearchResult(
            results=final_results,
            total_results=len(final_results),
            query_analysis=query_analysis,
            vector_results_count=len(
                results_by_strategy.get(SearchStrategy.VECTOR, [])
            ),
            semantic_results_count=len(
                results_by_strategy.get(SearchStrategy.SEMANTIC, [])
            ),
            graph_results_count=len(results_by_strategy.get(SearchStrategy.GRAPH, [])),
            fulltext_results_count=len(
                results_by_strategy.get(SearchStrategy.FULLTEXT, [])
            ),
            total_time_ms=total_time,
            query_analysis_time_ms=analysis_time,
            search_time_ms=search_time,
            reranking_time_ms=reranking_time,
            applied_weights={k.value: v for k, v in weights.items()},
            reranking_used=enable_reranking,
            reranking_model=reranking_model if enable_reranking else None,
        )

        # Cache result if enabled
        if self.enable_cache and not bypass_cache:
            cache_filters = {
                "k": k,
                "enable_vector": enable_vector,
                "enable_semantic": enable_semantic,
                "enable_graph": enable_graph,
                "enable_fulltext": enable_fulltext,
                "enable_reranking": enable_reranking,
                "temporal_filter": (
                    temporal_filter.isoformat() if temporal_filter else None
                ),
                "tag_filter": tag_filter,
                "min_importance": min_importance,
            }

            await self.cache.set(
                query=query,
                tenant_id=tenant_id,
                project_id=project_id,
                result=result.dict(),
                filters=cache_filters,
            )

        return result

    # ========================================================================
    # Strategy Implementations
    # ========================================================================

    async def _vector_search(
        self,
        tenant_id: str,
        project_id: str,
        query: str,
        k: int,
        temporal_filter: datetime = None,
        tag_filter: List[str] = None,
        min_importance: float = None,
    ) -> List[Dict[str, Any]]:
        """Execute vector similarity search"""
        logger.info("executing_vector_search", k=k)

        try:
            # Generate query embedding
            query_embedding = await self.ml_client.get_embedding(query)

            # Build SQL query
            sql = """
                SELECT
                    id, content, tags, importance, metadata, created_at,
                    1 - (embedding <=> $3) as similarity
                FROM memories
                WHERE tenant_id = $1 AND project = $2
                    AND embedding IS NOT NULL
            """
            params = [tenant_id, project_id, query_embedding]
            param_idx = 4

            if temporal_filter:
                sql += f" AND created_at >= ${param_idx}"
                params.append(temporal_filter)
                param_idx += 1

            if tag_filter:
                sql += f" AND tags && ${param_idx}"
                params.append(tag_filter)
                param_idx += 1

            if min_importance:
                sql += f" AND importance >= ${param_idx}"
                params.append(min_importance)
                param_idx += 1

            sql += f" ORDER BY similarity DESC LIMIT ${param_idx}"
            params.append(k)

            records = await self.pool.fetch(sql, *params)

            results = [
                {
                    "memory_id": record["id"],
                    "content": record["content"],
                    "score": float(record["similarity"]),
                    "metadata": record.get("metadata", {}),
                    "created_at": record["created_at"],
                }
                for record in records
            ]

            logger.info("vector_search_complete", results=len(results))
            return results

        except Exception as e:
            logger.error("vector_search_failed", error=str(e))
            return []

    async def _semantic_search(
        self,
        tenant_id: str,
        project_id: str,
        query: str,
        k: int,
        key_concepts: List[str],
    ) -> List[Dict[str, Any]]:
        """Execute semantic node search"""
        logger.info("executing_semantic_search", k=k, concepts=len(key_concepts))

        try:
            # Search semantic nodes
            sql = """
                SELECT sn.id, sn.label, sn.canonical_form, sn.importance_score,
                       sn.source_memory_ids, sn.created_at
                FROM semantic_nodes sn
                WHERE sn.tenant_id = $1 AND sn.project_id = $2
                    AND (
                        sn.label ILIKE '%' || $3 || '%'
                        OR sn.canonical_form ILIKE '%' || $3 || '%'
                    )
                    AND sn.is_degraded = FALSE
                ORDER BY sn.importance_score DESC, sn.reinforcement_count DESC
                LIMIT $4
            """

            records = await self.pool.fetch(sql, tenant_id, project_id, query, k)

            # Expand to source memories
            results = []
            for record in records:
                memory_ids = record.get("source_memory_ids", [])
                if memory_ids:
                    # Fetch source memories
                    memories = await self.pool.fetch(
                        """
                        SELECT id, content, metadata, created_at
                        FROM memories
                        WHERE tenant_id = $1 AND project = $2 AND id = ANY($3)
                        LIMIT 5
                        """,
                        tenant_id,
                        project_id,
                        memory_ids,
                    )

                    for mem in memories:
                        results.append(
                            {
                                "memory_id": mem["id"],
                                "content": mem["content"],
                                "score": float(record["importance_score"]),
                                "metadata": mem.get("metadata", {}),
                                "created_at": mem["created_at"],
                                "semantic_node": str(record["id"]),
                            }
                        )

            logger.info("semantic_search_complete", results=len(results))
            return results[:k]

        except Exception as e:
            logger.error("semantic_search_failed", error=str(e))
            return []

    async def _graph_search(
        self,
        tenant_id: str,
        project_id: str,
        query: str,
        key_entities: List[str],
        max_depth: int,
        k: int,
    ) -> List[Dict[str, Any]]:
        """Execute graph traversal search with GraphRAG"""
        logger.info(
            "executing_graph_search", entities=len(key_entities), depth=max_depth
        )

        try:
            if not key_entities:
                return []

            # Find graph nodes matching entities
            node_records = await self.pool.fetch(
                """
                SELECT id, node_id, label, properties FROM knowledge_graph_nodes
                WHERE tenant_id = $1 AND project_id = $2
                    AND (
                        label ILIKE ANY($3)
                        OR node_id = ANY($3)
                    )
                LIMIT 10
                """,
                tenant_id,
                project_id,
                [f"%{entity}%" for entity in key_entities],
            )

            if not node_records:
                logger.info("no_graph_nodes_found", entities=key_entities)
                return []

            # Get start node IDs for traversal
            start_node_ids = [record["node_id"] for record in node_records]

            # Traverse graph using BFS to find connected nodes
            traversed_nodes = await self.pool.fetch(
                """
                WITH RECURSIVE graph_traverse AS (
                    -- Base case: start nodes
                    SELECT
                        n.id,
                        n.node_id,
                        n.label,
                        n.properties,
                        0 as depth
                    FROM knowledge_graph_nodes n
                    WHERE n.tenant_id = $1
                    AND n.project_id = $2
                    AND n.node_id = ANY($3)

                    UNION

                    -- Recursive case: traverse edges (both directions)
                    SELECT
                        n.id,
                        n.node_id,
                        n.label,
                        n.properties,
                        gt.depth + 1
                    FROM graph_traverse gt
                    JOIN knowledge_graph_edges e ON (
                        gt.id = e.source_node_id OR gt.id = e.target_node_id
                    )
                    JOIN knowledge_graph_nodes n ON (
                        (e.source_node_id = n.id AND e.source_node_id != gt.id) OR
                        (e.target_node_id = n.id AND e.target_node_id != gt.id)
                    )
                    WHERE gt.depth < $4
                    AND n.tenant_id = $1
                    AND n.project_id = $2
                )
                SELECT DISTINCT ON (id) id, node_id, label, properties, depth
                FROM graph_traverse
                ORDER BY id, depth
                LIMIT 50
                """,
                tenant_id,
                project_id,
                start_node_ids,
                max_depth,
            )

            # Extract memory IDs from graph node properties
            memory_ids = set()
            for node in traversed_nodes:
                properties = node.get("properties", {})
                if isinstance(properties, str):
                    import json

                    properties = json.loads(properties)

                # Check for source_memory_id in properties
                if "source_memory_id" in properties:
                    memory_ids.add(properties["source_memory_id"])

                # Check for memory_ids array
                if "memory_ids" in properties and isinstance(
                    properties["memory_ids"], list
                ):
                    memory_ids.update(properties["memory_ids"])

            if not memory_ids:
                logger.info("no_memories_linked_to_graph", nodes=len(traversed_nodes))
                return []

            # Fetch related memories
            memories = await self.pool.fetch(
                """
                SELECT id, content, metadata, created_at, importance
                FROM memories
                WHERE tenant_id = $1 AND project = $2 AND id = ANY($3)
                ORDER BY importance DESC
                LIMIT $4
                """,
                tenant_id,
                project_id,
                list(memory_ids),
                k,
            )

            results = []
            for mem in memories:
                results.append(
                    {
                        "memory_id": mem["id"],
                        "content": mem["content"],
                        "score": float(mem.get("importance", 0.5)),
                        "metadata": mem.get("metadata", {}),
                        "created_at": mem["created_at"],
                        "source": "graph_traversal",
                    }
                )

            logger.info(
                "graph_search_complete",
                nodes_traversed=len(traversed_nodes),
                memories_found=len(results),
            )
            return results

        except Exception as e:
            logger.error("graph_search_failed", error=str(e), exc_info=True)
            return []

    async def _fulltext_search(
        self,
        tenant_id: str,
        project_id: str,
        query: str,
        k: int,
        temporal_filter: datetime = None,
        tag_filter: List[str] = None,
    ) -> List[Dict[str, Any]]:
        """Execute full-text keyword search"""
        logger.info("executing_fulltext_search", k=k)

        try:
            sql = """
                SELECT id, content, tags, importance, metadata, created_at,
                       ts_rank(to_tsvector('english', content), plainto_tsquery('english', $3)) as rank
                FROM memories
                WHERE tenant_id = $1 AND project = $2
                    AND to_tsvector('english', content) @@ plainto_tsquery('english', $3)
            """
            params = [tenant_id, project_id, query]
            param_idx = 4

            if temporal_filter:
                sql += f" AND created_at >= ${param_idx}"
                params.append(temporal_filter)
                param_idx += 1

            if tag_filter:
                sql += f" AND tags && ${param_idx}"
                params.append(tag_filter)
                param_idx += 1

            sql += f" ORDER BY rank DESC LIMIT ${param_idx}"
            params.append(k)

            records = await self.pool.fetch(sql, *params)

            results = [
                {
                    "memory_id": record["id"],
                    "content": record["content"],
                    "score": float(record["rank"]),
                    "metadata": record.get("metadata", {}),
                    "created_at": record["created_at"],
                }
                for record in records
            ]

            logger.info("fulltext_search_complete", results=len(results))
            return results

        except Exception as e:
            logger.error("fulltext_search_failed", error=str(e))
            return []

    # ========================================================================
    # Result Fusion
    # ========================================================================

    def _fuse_results(
        self,
        results_by_strategy: Dict[SearchStrategy, List[Dict[str, Any]]],
        weights: Dict[SearchStrategy, float],
        k: int,
    ) -> List[SearchResultItem]:
        """
        Fuse results from multiple strategies using weighted scoring.

        Normalizes scores and combines using strategy weights.

        Args:
            results_by_strategy: Results from each strategy
            weights: Strategy weights
            k: Number of results to return

        Returns:
            Fused and ranked list of SearchResultItem
        """
        logger.info("fusing_results", strategies=len(results_by_strategy))

        # Collect all unique results
        result_map = {}  # memory_id -> result data

        for strategy, results in results_by_strategy.items():
            weight = weights.get(strategy, 0.0)

            if weight == 0:
                continue

            # Normalize scores within strategy (0-1 range)
            if not results:
                continue

            max_score = max(r["score"] for r in results) or 1.0

            for result in results:
                memory_id = result["memory_id"]
                normalized_score = result["score"] / max_score

                if memory_id not in result_map:
                    result_map[memory_id] = {
                        "memory_id": memory_id,
                        "content": result["content"],
                        "metadata": result.get("metadata", {}),
                        "created_at": result["created_at"],
                        "strategy_scores": {},
                        "strategies_used": [],
                    }

                # Add strategy score
                result_map[memory_id]["strategy_scores"][
                    strategy.value
                ] = normalized_score
                result_map[memory_id]["strategies_used"].append(strategy)

        # Calculate hybrid scores
        fused_results = []

        for memory_id, data in result_map.items():
            # Calculate weighted hybrid score
            hybrid_score = 0.0
            for strategy, score in data["strategy_scores"].items():
                strategy_enum = SearchStrategy(strategy)
                weight = weights.get(strategy_enum, 0.0)
                hybrid_score += score * weight

            # Create SearchResultItem
            item = SearchResultItem(
                memory_id=memory_id,
                content=data["content"],
                metadata=data["metadata"],
                vector_score=data["strategy_scores"].get("vector"),
                semantic_score=data["strategy_scores"].get("semantic"),
                graph_score=data["strategy_scores"].get("graph"),
                fulltext_score=data["strategy_scores"].get("fulltext"),
                hybrid_score=hybrid_score,
                final_score=hybrid_score,  # Will be updated if re-ranked
                rank=1,  # Will be assigned later, default to 1 for validation
                search_strategies_used=data["strategies_used"],
                created_at=data["created_at"],
            )

            fused_results.append(item)

        # Sort by hybrid score
        fused_results.sort(key=lambda x: x.hybrid_score, reverse=True)

        logger.info("fusion_complete", total_results=len(fused_results))

        return fused_results[:k]

    # ========================================================================
    # LLM Re-ranking
    # ========================================================================

    async def _rerank_results(
        self, query: str, results: List[SearchResultItem], model: RerankingModel
    ) -> List[SearchResultItem]:
        """
        Re-rank results using LLM for contextual relevance.

        Args:
            query: Original query
            results: Candidate results
            model: LLM model for re-ranking

        Returns:
            Re-ranked results
        """
        logger.info("reranking_results", count=len(results), model=model.value)

        if not results:
            return results

        try:
            # Format results for LLM
            results_formatted = []
            for idx, result in enumerate(results):
                snippet = (
                    result.content[:200] + "..."
                    if len(result.content) > 200
                    else result.content
                )
                results_formatted.append(f"{idx}. {snippet}")

            results_text = "\n\n".join(results_formatted)

            prompt = RERANKING_PROMPT.format(query=query, results=results_text)

            # Call LLM
            response = await self.llm_provider.generate(
                system="You are a search result re-ranking expert.",
                prompt=prompt,
                model=model.value,
            )

            # Parse scores (expect JSON array)
            import json

            scores_data = json.loads(response.text.strip())

            # Apply re-ranking scores
            for score_item in scores_data:
                idx = score_item["index"]
                score = score_item["score"]

                if 0 <= idx < len(results):
                    results[idx].rerank_score = score
                    # Combine with hybrid score (70% rerank, 30% hybrid)
                    results[idx].final_score = (
                        score * 0.7 + results[idx].hybrid_score * 0.3
                    )

            # Re-sort by final score
            results.sort(key=lambda x: x.final_score, reverse=True)

            logger.info("reranking_complete", reranked=len(results))

            return results

        except Exception as e:
            logger.error("reranking_failed", error=str(e))
            # Return original order if re-ranking fails
            return results
