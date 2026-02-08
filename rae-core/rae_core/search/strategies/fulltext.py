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
                # Try common ID field names
                m_id = r.get('id') or r.get('memory_id') or r.get('uuid')
                if m_id:
                    output.append((UUID(str(m_id)), r.get('score', 1.0)))
            except Exception:
                continue
        return output
