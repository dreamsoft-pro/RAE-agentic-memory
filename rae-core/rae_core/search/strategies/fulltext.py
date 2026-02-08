from typing import Any, Dict, List, Tuple
from uuid import UUID
import structlog
from rae_core.interfaces.storage import IMemoryStorage
from rae_core.search.strategies import SearchStrategy

logger = structlog.get_logger(__name__)

class FullTextStrategy(SearchStrategy):
    def __init__(self, memory_storage: IMemoryStorage):
        self.storage = memory_storage

    def get_strategy_name(self) -> str:
        return "fulltext"

    def get_strategy_weight(self) -> float:
        return 1.0

    async def search(self, query: str, tenant_id: str, filters: Dict[str, Any] | None = None, limit: int = 10, **kwargs: Any) -> List[Tuple[UUID, float]]:
        agent_id = kwargs.get('agent_id') or (filters or {}).get('agent_id')
        layer = kwargs.get('layer') or (filters or {}).get('layer')
        
        results = await self.storage.search_memories(
            query=query,
            tenant_id=tenant_id,
            limit=limit,
            filters=filters,
            agent_id=agent_id,
            layer=layer
        )
        
        output = []
        for r in results:
            try:
                # Handle SQLite style: {"memory": {...}, "score": ...}
                if isinstance(r, dict) and "memory" in r:
                    m_data = r["memory"]
                    m_id = m_data.get('id') or m_data.get('memory_id') or m_data.get('uuid')
                    score = r.get('score', 1.0)
                else:
                    # Flat style (Postgres)
                    m_id = r.get('id') or r.get('memory_id') or r.get('uuid')
                    score = r.get('score', 1.0)
                
                if m_id:
                    output.append((UUID(str(m_id)), float(score)))
            except Exception as e:
                logger.error("fulltext_result_parsing_failed", error=str(e), result=r)
                continue
        return output
