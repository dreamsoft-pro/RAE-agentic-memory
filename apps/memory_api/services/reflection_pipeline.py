"""
Reflection Pipeline - Enterprise Clustering & Generation System

This module implements the complete reflection generation pipeline with:
- Memory clustering using HDBSCAN and k-means
- Hierarchical reflection generation (insight → meta-insight)
- Automatic scoring and prioritization
- Embedding generation for reflections
- Cache-aware generation
- Full telemetry and cost tracking
"""

from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple
from uuid import UUID

import asyncpg
import numpy as np
import structlog

# Optional scikit-learn imports for clustering
try:  # pragma: no cover
    from sklearn.cluster import HDBSCAN, KMeans
    from sklearn.preprocessing import StandardScaler

    SKLEARN_AVAILABLE = True
except ImportError:  # pragma: no cover
    HDBSCAN = None  # type: ignore[assignment,misc]
    KMeans = None  # type: ignore[assignment,misc]
    StandardScaler = None  # type: ignore[assignment,misc]
    SKLEARN_AVAILABLE = False

if TYPE_CHECKING:
    from sklearn.cluster import HDBSCAN, KMeans  # noqa: F401
    from sklearn.preprocessing import StandardScaler  # noqa: F401

from apps.memory_api.config import settings
from apps.memory_api.models.reflection_models import (
    GenerateReflectionRequest,
    ReflectionScoring,
    ReflectionTelemetry,
    ReflectionType,
    ReflectionUnit,
)
from apps.memory_api.repositories import reflection_repository
from apps.memory_api.services.llm import get_llm_provider
from apps.memory_api.services.ml_service_client import MLServiceClient

logger = structlog.get_logger(__name__)


# ============================================================================
# Prompts
# ============================================================================

CLUSTER_INSIGHT_PROMPT = """
You are analyzing a cluster of related memories to extract key insights.

Memories in this cluster:
{memories}

Your task:
1. Identify the main theme or pattern connecting these memories
2. Extract the most important insight that can be learned
3. Be concise but comprehensive

Provide your insight as a clear, actionable statement.
"""

META_INSIGHT_PROMPT = """
You are analyzing a collection of insights to extract higher-level patterns.

Related insights:
{insights}

Your task:
1. Identify patterns across these insights
2. Extract meta-level understanding
3. Synthesize a broader principle or pattern

Provide your meta-insight as a clear, strategic observation.
"""

REFLECTION_SCORING_PROMPT = """
Evaluate this reflection on multiple dimensions:

Reflection: {reflection}

Score each dimension from 0.0 to 1.0:

1. Novelty: How unique or surprising is this insight?
2. Importance: How significant is this for decision-making?
3. Utility: How actionable or useful is this?
4. Confidence: How confident are you in this assessment?

Return scores as JSON:
{{
  "novelty": 0.0-1.0,
  "importance": 0.0-1.0,
  "utility": 0.0-1.0,
  "confidence": 0.0-1.0
}}
"""


# ============================================================================
# Reflection Pipeline
# ============================================================================


class ReflectionPipeline:
    """
    Enterprise reflection generation pipeline with clustering and hierarchical insights.

    Features:
    - Automatic memory clustering (HDBSCAN or k-means)
    - Per-cluster insight generation
    - Hierarchical meta-insight generation
    - Automatic scoring (novelty, importance, utility, confidence)
    - Embedding generation for similarity search
    - Cache checking to avoid duplicate reflections
    - Full telemetry and cost tracking
    """

    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool
        self.llm_provider = get_llm_provider()
        self.ml_client = MLServiceClient()

    def _ensure_sklearn_available(self) -> None:
        """Ensure scikit-learn is available for clustering operations."""
        if not SKLEARN_AVAILABLE:
            raise RuntimeError(
                "Reflection clustering requires scikit-learn. "
                "Install ML extras: `pip install -r apps/memory_api/requirements-ml.txt` "
                "or run: `pip install scikit-learn`."
            )

    async def generate_reflections(
        self, request: GenerateReflectionRequest
    ) -> Tuple[List[ReflectionUnit], Dict[str, Any]]:
        """
        Generate reflections from memories using clustering pipeline.

        Args:
            request: Generation request with parameters

        Returns:
            Tuple of (generated_reflections, statistics)
        """
        logger.info(
            "reflection_pipeline_started",
            tenant_id=request.tenant_id,
            project=request.project,
            max_memories=request.max_memories,
        )

        start_time = datetime.now()
        statistics = {
            "memories_processed": 0,
            "clusters_found": 0,
            "insights_generated": 0,
            "meta_insights_generated": 0,
            "total_cost_usd": 0.0,
            "total_duration_ms": 0,
        }

        # Step 1: Fetch memories
        memories = await self._fetch_memories(
            request.tenant_id,
            request.project,
            request.max_memories,
            request.memory_filters,
            request.since,
        )

        if not memories:
            logger.info("no_memories_for_reflection", project=request.project)
            return [], statistics

        statistics["memories_processed"] = len(memories)
        logger.info("memories_fetched", count=len(memories))

        # Step 2: Cluster memories
        clusters = await self._cluster_memories(memories, request.min_cluster_size)
        statistics["clusters_found"] = len(clusters)
        logger.info("clustering_complete", clusters=len(clusters))

        if not clusters:
            logger.info("no_clusters_found", min_size=request.min_cluster_size)
            return [], statistics

        # Step 3: Generate insights for each cluster
        insights = []
        for cluster_id, cluster_memories in clusters.items():
            try:
                insight = await self._generate_cluster_insight(
                    tenant_id=request.tenant_id,
                    project_id=request.project,
                    cluster_id=cluster_id,
                    memories=cluster_memories,
                    parent_reflection_id=request.parent_reflection_id,
                )
                insights.append(insight)
                statistics["insights_generated"] += 1
                statistics["total_cost_usd"] += (
                    insight.telemetry.generation_cost_usd or 0.0
                )
            except Exception as e:
                logger.error(
                    "cluster_insight_failed", cluster_id=cluster_id, error=str(e)
                )

        logger.info("insights_generated", count=len(insights))

        # Step 4: Generate meta-insights if we have multiple insights
        all_reflections = insights.copy()

        if len(insights) >= 3 and not request.parent_reflection_id:
            try:
                meta_insight = await self._generate_meta_insight(
                    tenant_id=request.tenant_id,
                    project_id=request.project,
                    insights=insights,
                )
                all_reflections.append(meta_insight)
                statistics["meta_insights_generated"] += 1
                statistics["total_cost_usd"] += (
                    meta_insight.telemetry.generation_cost_usd or 0.0
                )
                logger.info("meta_insight_generated")
            except Exception as e:
                logger.error("meta_insight_failed", error=str(e))

        # Calculate total duration
        end_time = datetime.now()
        statistics["total_duration_ms"] = int(
            (end_time - start_time).total_seconds() * 1000
        )

        logger.info(
            "reflection_pipeline_complete",
            reflections=len(all_reflections),
            statistics=statistics,
        )

        return all_reflections, statistics

    async def _fetch_memories(
        self,
        tenant_id: str,
        project_id: str,
        limit: int,
        filters: Optional[Dict[str, Any]],
        since: Optional[datetime],
    ) -> List[Dict[str, Any]]:
        """Fetch memories for reflection generation"""
        conditions = ["tenant_id = $1", "project = $2"]
        params = [tenant_id, project_id]
        param_idx = 3

        # Add filters
        if since:
            conditions.append(f"created_at >= ${param_idx}")
            params.append(since)
            param_idx += 1

        if filters:
            if "layer" in filters:
                conditions.append(f"layer = ${param_idx}")
                params.append(filters["layer"])
                param_idx += 1

            if "tags" in filters:
                conditions.append(f"tags && ${param_idx}")
                params.append(filters["tags"])
                param_idx += 1

        where_clause = " AND ".join(conditions)
        query = f"""
            SELECT id, content, embedding, tags, importance, created_at
            FROM memories
            WHERE {where_clause}
            ORDER BY created_at DESC
            LIMIT ${param_idx}
        """
        params.append(limit)

        records = await self.pool.fetch(query, *params)
        return [dict(r) for r in records]

    async def _cluster_memories(
        self, memories: List[Dict[str, Any]], min_cluster_size: int
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Cluster memories using HDBSCAN or k-means.

        Args:
            memories: List of memory dictionaries with embeddings
            min_cluster_size: Minimum cluster size

        Returns:
            Dictionary mapping cluster_id to list of memories
        """
        # Ensure scikit-learn is available for clustering
        self._ensure_sklearn_available()

        logger.info(
            "clustering_memories", count=len(memories), min_size=min_cluster_size
        )

        # Extract embeddings
        embeddings = []
        valid_memories = []

        for memory in memories:
            if memory.get("embedding"):
                embeddings.append(memory["embedding"])
                valid_memories.append(memory)

        if len(embeddings) < min_cluster_size:
            logger.warning(
                "insufficient_memories_for_clustering", count=len(embeddings)
            )
            return {}

        embeddings_array = np.array(embeddings)

        # Standardize embeddings
        scaler = StandardScaler()
        embeddings_scaled = scaler.fit_transform(embeddings_array)

        # Try HDBSCAN first (density-based, automatic cluster detection)
        try:
            clusterer = HDBSCAN(
                min_cluster_size=min_cluster_size,
                min_samples=max(2, min_cluster_size // 2),
                metric="euclidean",
            )
            cluster_labels = clusterer.fit_predict(embeddings_scaled)

            # Check if we got meaningful clusters (not all noise)
            unique_labels = set(cluster_labels)
            unique_labels.discard(-1)  # Remove noise label

            if len(unique_labels) == 0:
                # Fall back to k-means
                logger.info("hdbscan_found_no_clusters_falling_back_to_kmeans")
                raise ValueError("No clusters found")

        except Exception as e:
            logger.info("using_kmeans_clustering", reason=str(e))
            # Fall back to k-means with heuristic for number of clusters
            n_clusters = max(2, min(len(embeddings) // min_cluster_size, 10))
            clusterer = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            cluster_labels = clusterer.fit_predict(embeddings_scaled)

        # Group memories by cluster
        clusters = {}
        for memory, label in zip(valid_memories, cluster_labels):
            if label == -1:  # Skip noise in HDBSCAN
                continue

            cluster_id = f"cluster_{label}"
            if cluster_id not in clusters:
                clusters[cluster_id] = []
            clusters[cluster_id].append(memory)

        # Filter out clusters below minimum size
        clusters = {
            cid: mems for cid, mems in clusters.items() if len(mems) >= min_cluster_size
        }

        logger.info(
            "clustering_complete",
            clusters_found=len(clusters),
            sizes=[len(mems) for mems in clusters.values()],
        )

        return clusters

    async def _generate_cluster_insight(
        self,
        tenant_id: str,
        project_id: str,
        cluster_id: str,
        memories: List[Dict[str, Any]],
        parent_reflection_id: Optional[UUID] = None,
    ) -> ReflectionUnit:
        """Generate insight for a single cluster of memories"""
        logger.info(
            "generating_cluster_insight", cluster_id=cluster_id, memories=len(memories)
        )

        generation_start = datetime.now()

        # Format memories for prompt
        memory_texts = [
            f"- [{m.get('created_at', 'unknown')}] {m.get('content', '')}"
            for m in memories[:20]  # Limit to 20 for context window
        ]
        memories_formatted = "\n".join(memory_texts)

        # Generate insight using LLM
        prompt = CLUSTER_INSIGHT_PROMPT.format(memories=memories_formatted)

        try:
            result = await self.llm_provider.generate(
                system="You are an expert at pattern recognition and insight extraction.",
                prompt=prompt,
                model=settings.RAE_LLM_MODEL_DEFAULT,
            )

            insight_text = result.text

            # Calculate generation metrics
            generation_duration = int(
                (datetime.now() - generation_start).total_seconds() * 1000
            )

            # Score the insight
            scoring = await self._score_reflection(insight_text)

            # Generate embedding for the insight
            embedding = await self._generate_embedding(insight_text)

            # Extract source memory IDs
            source_memory_ids = [UUID(m["id"]) for m in memories if m.get("id")]

            # Create telemetry
            telemetry = ReflectionTelemetry(
                generation_model=settings.RAE_LLM_MODEL_DEFAULT,
                generation_duration_ms=generation_duration,
                generation_tokens_used=(
                    result.usage.total_tokens if result.usage else None
                ),
                generation_cost_usd=(
                    result.cost_usd if hasattr(result, "cost_usd") else None
                ),
            )

            # Determine priority based on cluster size and importance
            priority = self._calculate_priority(len(memories), scoring)

            # Create reflection in database
            reflection = await reflection_repository.create_reflection(
                pool=self.pool,
                tenant_id=tenant_id,
                project_id=project_id,
                content=insight_text,
                reflection_type=ReflectionType.INSIGHT,
                priority=priority,
                scoring=scoring,
                parent_reflection_id=parent_reflection_id,
                source_memory_ids=source_memory_ids,
                embedding=embedding,
                cluster_id=cluster_id,
                tags=["cluster_insight", cluster_id],
                telemetry=telemetry,
            )

            logger.info(
                "cluster_insight_generated",
                reflection_id=str(reflection.id),
                score=reflection.score,
                priority=priority,
            )

            return reflection

        except Exception as e:
            logger.error("cluster_insight_generation_failed", error=str(e))
            raise

    async def _generate_meta_insight(
        self, tenant_id: str, project_id: str, insights: List[ReflectionUnit]
    ) -> ReflectionUnit:
        """Generate meta-insight from multiple insights"""
        logger.info("generating_meta_insight", insights=len(insights))

        generation_start = datetime.now()

        # Format insights for prompt
        insight_texts = [
            f"- {insight.content}"
            for insight in insights[:10]  # Limit to 10 for context window
        ]
        insights_formatted = "\n".join(insight_texts)

        # Generate meta-insight using LLM
        prompt = META_INSIGHT_PROMPT.format(insights=insights_formatted)

        try:
            result = await self.llm_provider.generate(
                system="You are an expert at synthesizing higher-level patterns from insights.",
                prompt=prompt,
                model=settings.RAE_LLM_MODEL_DEFAULT,
            )

            meta_insight_text = result.text

            # Calculate generation metrics
            generation_duration = int(
                (datetime.now() - generation_start).total_seconds() * 1000
            )

            # Score the meta-insight (typically higher scores for synthesis)
            scoring = await self._score_reflection(meta_insight_text)
            # Boost scores slightly for meta-insights
            scoring.importance_score = min(1.0, scoring.importance_score * 1.1)
            scoring.utility_score = min(1.0, scoring.utility_score * 1.1)

            # Generate embedding
            embedding = await self._generate_embedding(meta_insight_text)

            # Extract source reflection IDs
            source_reflection_ids = [insight.id for insight in insights]

            # Create telemetry
            telemetry = ReflectionTelemetry(
                generation_model=settings.RAE_LLM_MODEL_DEFAULT,
                generation_duration_ms=generation_duration,
                generation_tokens_used=(
                    result.usage.total_tokens if result.usage else None
                ),
                generation_cost_usd=(
                    result.cost_usd if hasattr(result, "cost_usd") else None
                ),
            )

            # Meta-insights get high priority
            priority = 5

            # Create meta-reflection in database
            reflection = await reflection_repository.create_reflection(
                pool=self.pool,
                tenant_id=tenant_id,
                project_id=project_id,
                content=meta_insight_text,
                reflection_type=ReflectionType.META,
                priority=priority,
                scoring=scoring,
                source_reflection_ids=source_reflection_ids,
                embedding=embedding,
                tags=["meta_insight", "synthesis"],
                telemetry=telemetry,
            )

            logger.info(
                "meta_insight_generated",
                reflection_id=str(reflection.id),
                score=reflection.score,
            )

            return reflection

        except Exception as e:
            logger.error("meta_insight_generation_failed", error=str(e))
            raise

    async def _score_reflection(self, reflection_text: str) -> ReflectionScoring:
        """
        Score a reflection on multiple dimensions using LLM.

        Args:
            reflection_text: The reflection content to score

        Returns:
            ReflectionScoring with component scores
        """
        try:
            prompt = REFLECTION_SCORING_PROMPT.format(reflection=reflection_text)

            # Use structured output for reliable parsing
            from pydantic import BaseModel, Field

            class ScoreResponse(BaseModel):
                novelty: float = Field(..., ge=0.0, le=1.0)
                importance: float = Field(..., ge=0.0, le=1.0)
                utility: float = Field(..., ge=0.0, le=1.0)
                confidence: float = Field(..., ge=0.0, le=1.0)

            result = await self.llm_provider.generate_structured(
                system="You are an expert evaluator of insights and reflections.",
                prompt=prompt,
                model=settings.RAE_LLM_MODEL_DEFAULT,
                response_model=ScoreResponse,
            )

            return ReflectionScoring(
                novelty_score=result.novelty,
                importance_score=result.importance,
                utility_score=result.utility,
                confidence_score=result.confidence,
            )

        except Exception as e:
            logger.warning("scoring_failed_using_defaults", error=str(e))
            # Return default middle scores
            return ReflectionScoring(
                novelty_score=0.5,
                importance_score=0.5,
                utility_score=0.5,
                confidence_score=0.5,
            )

    async def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for reflection text"""
        try:
            embedding = await self.ml_client.get_embedding(text)
            return embedding
        except Exception as e:
            logger.error("embedding_generation_failed", error=str(e))
            # Return zero vector as fallback
            return [0.0] * 1536

    def _calculate_priority(self, cluster_size: int, scoring: ReflectionScoring) -> int:
        """
        Calculate priority (1-5) based on cluster size and scores.

        Larger clusters and higher scores get higher priority.
        """
        # Base priority from composite score
        score_priority = scoring.composite_score * 5

        # Bonus for larger clusters (more evidence)
        size_bonus = min(1.0, cluster_size / 10)  # Max bonus at 10+ memories

        # Calculate final priority
        priority = int(round(score_priority + size_bonus))

        # Clamp to 1-5 range
        return max(1, min(5, priority))
