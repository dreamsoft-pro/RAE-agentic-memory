import pytest
from uuid import UUID
from rae_core.search.strategies import SearchStrategy

class DummyStrategy(SearchStrategy):
    async def search(self, query, tenant_id, filters=None, limit=10):
        # Call super to cover the abstract method pass
        await super().search(query, tenant_id, filters, limit)
        return []
        
    def get_strategy_name(self):
        super().get_strategy_name()
        return "dummy"
        
    def get_strategy_weight(self):
        super().get_strategy_weight()
        return 0.5

@pytest.mark.asyncio
async def test_search_strategy_abstract_calls():
    strategy = DummyStrategy()
    await strategy.search("test", "tenant")
    assert strategy.get_strategy_name() == "dummy"
    assert strategy.get_strategy_weight() == 0.5
