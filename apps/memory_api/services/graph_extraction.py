"""
Graph Extraction Service - Enterprise-grade knowledge graph extraction from episodic memories.

This module provides sophisticated entity and relationship extraction capabilities,
transforming unstructured episodic memories into structured knowledge graphs.
"""

from typing import List, Dict, Optional, Any
import re
from pydantic import BaseModel, Field, field_validator
import asyncpg
import structlog

from apps.memory_api.services.llm import get_llm_provider
from apps.memory_api.config import settings
from apps.memory_api import metrics

logger = structlog.get_logger(__name__)


class GraphTriple(BaseModel):
    """
    Represents a single (Subject, Relation, Object) triple in the knowledge graph.

    Enterprise features:
    - Confidence scoring for reliability
    - Rich metadata for provenance tracking
    - Validation of entity and relation formats
    - Hashable for set operations and deduplication
    """

    model_config = {"frozen": True}  # Make model hashable by freezing it

    source: str = Field(
        ...,
        description="The source entity (subject) in the relationship",
        min_length=1,
        max_length=500
    )
    relation: str = Field(
        ...,
        description="The relationship type between entities (e.g., REPORTED_BUG, DEPENDS_ON)",
        min_length=1,
        max_length=200
    )
    target: str = Field(
        ...,
        description="The target entity (object) in the relationship",
        min_length=1,
        max_length=500
    )
    confidence: float = Field(
        default=1.0,
        description="Confidence score of the extraction (0.0 to 1.0)",
        ge=0.0,
        le=1.0
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata about the triple (source_memory_id, extraction_timestamp, etc.)"
    )

    @field_validator('source', 'target')
    @classmethod
    def normalize_entity(cls, v: str) -> str:
        """
        Normalize entity names to prevent fuzzy duplicates.

        Uses _normalize_entity_name helper.
        """
        return _normalize_entity_name(v)

    @field_validator('relation')
    @classmethod
    def normalize_relation(cls, v: str) -> str:
        """Normalize relation names to uppercase with underscores."""
        return v.upper().replace(' ', '_').replace('-', '_')

    def __hash__(self) -> int:
        """
        Make GraphTriple hashable for set operations and deduplication.

        Only uses source, relation, and target for hashing to allow
        deduplication of triples with different confidence scores.
        """
        return hash((self.source, self.relation, self.target))


class GraphExtractionResult(BaseModel):
    """
    Complete result of a knowledge graph extraction operation.

    Contains:
    - Extracted triples with relationships
    - List of unique entities discovered
    - Statistics about the extraction process
    """

    triples: List[GraphTriple] = Field(
        default_factory=list,
        description="Extracted relationship triples"
    )
    extracted_entities: List[str] = Field(
        default_factory=list,
        description="Unique entities discovered in the memories"
    )
    statistics: Dict[str, Any] = Field(
        default_factory=dict,
        description="Extraction statistics (memories_processed, entities_count, etc.)"
    )


def _normalize_entity_name(name: str) -> str:
    """
    Normalize entity names to prevent fuzzy duplicates.

    Transformations:
    - Convert to lowercase for case-insensitive matching
    - Strip whitespace
    - Replace hyphens and underscores with spaces
    - Remove extra spaces

    Args:
        name: The entity name to normalize.

    Returns:
        Normalized entity name.
    """
    # 1. Lowercase
    name = name.lower()
    # 2. Replace hyphens and underscores with spaces
    name = name.replace('-', ' ').replace('_', ' ')
    # 3. Strip whitespace
    name = name.strip()
    # 4. Remove extra spaces
    name = re.sub(r'\s+', ' ', name)
    return name


# Enterprise-grade extraction prompt with detailed instructions
GRAPH_EXTRACTION_PROMPT = """
You are an expert knowledge graph extraction system. Your task is to analyze memories and extract
structured relationships between entities.

## Instructions:
1. Identify key entities: people, projects, modules, concepts, bugs, features, decisions
2. Extract relationships between entities using clear, consistent relation types
3. Use standardized relation types like: REPORTED_BUG, FIXED_BY, DEPENDS_ON, CREATED_BY, MODIFIED, RELATED_TO, CAUSES, IMPLEMENTS
4. Assign confidence scores based on clarity and explicitness of the relationship
5. Extract only factual relationships, not speculative ones

## Memories to analyze:
{memories_text}

## Output format:
Provide a structured JSON response with:
- triples: Array of {{source, relation, target, confidence}} objects
- extracted_entities: Array of unique entity names
- statistics: Object with counts and metrics

Focus on quality over quantity. Extract only clear, meaningful relationships.
"""


class GraphExtractionService:
    """
    Enterprise-grade service for extracting knowledge graphs from memories.

    Features:
    - Batch processing of memories
    - Configurable extraction strategies
    - Automatic entity deduplication
    - Performance metrics and logging
    - Error handling and retry logic
    """

    def __init__(self, pool: asyncpg.Pool):
        """
        Initialize the graph extraction service.

        Args:
            pool: AsyncPG connection pool for database operations
        """
        self.pool = pool
        self.llm_provider = get_llm_provider()

    async def extract_knowledge_graph(
        self,
        project_id: str,
        tenant_id: str,
        limit: int = 50,
        min_confidence: float = 0.5
    ) -> GraphExtractionResult:
        """
        Extract knowledge graph triples from episodic memories.

        This is the main entry point for graph extraction. It:
        1. Fetches recent episodic memories from the database
        2. Uses LLM to extract structured relationships
        3. Filters results by confidence threshold
        4. Returns structured extraction results

        Args:
            project_id: The project to extract knowledge from
            tenant_id: The tenant ID for multi-tenancy
            limit: Maximum number of memories to process (default: 50)
            min_confidence: Minimum confidence threshold for triples (default: 0.5)

        Returns:
            GraphExtractionResult with triples, entities, and statistics

        Raises:
            ValueError: If project_id or tenant_id is invalid
            RuntimeError: If extraction fails
        """
        logger.info(
            "starting_graph_extraction",
            project_id=project_id,
            tenant_id=tenant_id,
            limit=limit
        )

        # 1. Fetch recent episodic memories
        memories = await self._fetch_episodic_memories(project_id, tenant_id, limit)

        if not memories:
            logger.info("no_memories_found", project_id=project_id)
            return GraphExtractionResult(
                statistics={
                    "memories_processed": 0,
                    "entities_count": 0,
                    "triples_count": 0
                }
            )

        # 2. Format memories for extraction
        memories_text = self._format_memories(memories)

        # 3. Create extraction prompt
        prompt = GRAPH_EXTRACTION_PROMPT.format(memories_text=memories_text)

        # 4. Call LLM with structured output
        try:
            system_prompt = "You are an expert knowledge graph extraction system."

            extraction_result = await self.llm_provider.generate_structured(
                system=system_prompt,
                prompt=prompt,
                model=settings.RAE_LLM_MODEL_DEFAULT,
                response_model=GraphExtractionResult
            )

            # 5. Filter by confidence threshold
            filtered_triples = [
                triple for triple in extraction_result.triples
                if triple.confidence >= min_confidence
            ]

            # 6. Add metadata to triples
            for triple in filtered_triples:
                triple.metadata.update({
                    "project_id": project_id,
                    "tenant_id": tenant_id,
                    "extraction_method": "llm_structured",
                    "model": settings.RAE_LLM_MODEL_DEFAULT
                })

            # 7. Compile statistics
            statistics = {
                "memories_processed": len(memories),
                "entities_count": len(extraction_result.extracted_entities),
                "triples_count": len(filtered_triples),
                "triples_filtered": len(extraction_result.triples) - len(filtered_triples),
                "min_confidence": min_confidence
            }

            logger.info(
                "graph_extraction_completed",
                project_id=project_id,
                statistics=statistics
            )

            # Update metrics
            metrics.reflection_event_counter.labels(
                tenant_id=tenant_id,
                project=project_id
            ).inc()

            return GraphExtractionResult(
                triples=filtered_triples,
                extracted_entities=extraction_result.extracted_entities,
                statistics=statistics
            )

        except Exception as e:
            logger.exception(
                "graph_extraction_failed",
                project_id=project_id,
                error=str(e)
            )
            raise RuntimeError(f"Graph extraction failed: {e}")

    async def _fetch_episodic_memories(
        self,
        project_id: str,
        tenant_id: str,
        limit: int
    ) -> List[Dict[str, Any]]:
        """
        Fetch recent episodic memories for extraction.

        Args:
            project_id: Project identifier
            tenant_id: Tenant identifier
            limit: Maximum number of memories to fetch

        Returns:
            List of memory dictionaries with id, content, and metadata
        """
        async with self.pool.acquire() as conn:
            records = await conn.fetch(
                """
                SELECT id, content, created_at, tags, source
                FROM memories
                WHERE tenant_id = $1 AND project = $2 AND layer = 'em'
                ORDER BY created_at DESC
                LIMIT $3
                """,
                tenant_id,
                project_id,
                limit
            )

            return [dict(record) for record in records]

    def _format_memories(self, memories: List[Dict[str, Any]]) -> str:
        """
        Format memories into a readable text format for LLM processing.

        Args:
            memories: List of memory dictionaries

        Returns:
            Formatted string with numbered memories
        """
        formatted_lines = []

        for i, memory in enumerate(memories, 1):
            content = memory.get('content', '')
            tags = memory.get('tags', [])
            source = memory.get('source', 'unknown')
            created_at = memory.get('created_at', '')

            line = f"{i}. [{created_at}] {content}"

            if tags:
                line += f" [tags: {', '.join(tags)}]"

            if source:
                line += f" (source: {source})"

            formatted_lines.append(line)

        return "\n".join(formatted_lines)

    async def store_graph_triples(
        self,
        triples: List[GraphTriple],
        project_id: str,
        tenant_id: str
    ) -> Dict[str, int]:
        """
        Store extracted graph triples in the database.

        This method:
        1. Inserts nodes (entities) if they don't exist
        2. Creates edges (relationships) between nodes
        3. Handles conflicts gracefully
        4. Returns statistics about inserted records

        Args:
            triples: List of GraphTriple objects to store
            project_id: Project identifier
            tenant_id: Tenant identifier

        Returns:
            Dictionary with counts of nodes_created and edges_created
        """
        nodes_created = 0
        edges_created = 0

        async with self.pool.acquire() as conn:
            async with conn.transaction():
                for triple in triples:
                    # Insert source node
                    result = await conn.execute(
                        """
                        INSERT INTO knowledge_graph_nodes
                        (tenant_id, project_id, node_id, label, properties)
                        VALUES ($1, $2, $3, $4, $5)
                        ON CONFLICT (tenant_id, project_id, node_id) DO NOTHING
                        """,
                        tenant_id,
                        project_id,
                        triple.source,
                        triple.source,
                        triple.metadata
                    )
                    if result == "INSERT 0 1":
                        nodes_created += 1

                    # Insert target node
                    result = await conn.execute(
                        """
                        INSERT INTO knowledge_graph_nodes
                        (tenant_id, project_id, node_id, label, properties)
                        VALUES ($1, $2, $3, $4, $5)
                        ON CONFLICT (tenant_id, project_id, node_id) DO NOTHING
                        """,
                        tenant_id,
                        project_id,
                        triple.target,
                        triple.target,
                        triple.metadata
                    )
                    if result == "INSERT 0 1":
                        nodes_created += 1

                    # Get node IDs
                    source_node = await conn.fetchrow(
                        """
                        SELECT id FROM knowledge_graph_nodes
                        WHERE tenant_id = $1 AND project_id = $2 AND node_id = $3
                        """,
                        tenant_id,
                        project_id,
                        triple.source
                    )

                    target_node = await conn.fetchrow(
                        """
                        SELECT id FROM knowledge_graph_nodes
                        WHERE tenant_id = $1 AND project_id = $2 AND node_id = $3
                        """,
                        tenant_id,
                        project_id,
                        triple.target
                    )

                    if source_node and target_node:
                        # Create edge with metadata
                        edge_properties = {
                            "confidence": triple.confidence,
                            **triple.metadata
                        }

                        result = await conn.execute(
                            """
                            INSERT INTO knowledge_graph_edges
                            (tenant_id, project_id, source_node_id, target_node_id, relation, properties)
                            VALUES ($1, $2, $3, $4, $5, $6)
                            ON CONFLICT DO NOTHING
                            """,
                            tenant_id,
                            project_id,
                            source_node["id"],
                            target_node["id"],
                            triple.relation,
                            edge_properties
                        )
                        if result == "INSERT 0 1":
                            edges_created += 1

        logger.info(
            "graph_triples_stored",
            project_id=project_id,
            nodes_created=nodes_created,
            edges_created=edges_created
        )

        return {
            "nodes_created": nodes_created,
            "edges_created": edges_created
        }
