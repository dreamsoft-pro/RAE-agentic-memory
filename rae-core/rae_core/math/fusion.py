"""
Fusion Strategy - Adapter for LogicGateway.
"""

from typing import Dict, List, Tuple, Any
from uuid import UUID

from rae_core.math.logic_gateway import LogicGateway

class FusionStrategy:
    """
    Wrapper around LogicGateway to handle fusion logic.
    """

    def __init__(self):
        self.gateway = LogicGateway()

    def fuse(
        self, 
        strategy_results: Dict[str, List[Tuple[UUID, float]]], 
        weights: Dict[str, float] | None = None,
        query: str = "",
        config_override: Dict[str, float] | None = None
    ) -> List[Tuple[UUID, float]]:
        """
        Fuse results using LogicGateway routing.
        Passes config_override for System 7.2 Dynamic Thresholds.
        """
        # Route query to profile
        profile = self.gateway.route(query, strategy_results)
        
        # Execute fusion with optional config override
        return self.gateway.fuse(
            profile, 
            strategy_results, 
            weights=weights,
            query=query, 
            config_override=config_override
        )

# --- Legacy Support for MultiVectorStrategy ---

class RRFFusion:
    """Legacy RRF Fusion for internal MultiVector strategy usage."""
    
    def fuse(self, strategy_results: Dict[str, List[Tuple[UUID, float]]], weights: Dict[str, float] | None = None) -> List[Tuple[UUID, float]]:
        # Simple RRF implementation for internal vector fusion
        k = 60
        fused: Dict[UUID, float] = {}
        
        for res_list in strategy_results.values():
            for rank, (id, _) in enumerate(res_list):
                score = 1.0 / (rank + k)
                fused[id] = fused.get(id, 0.0) + score
                
        return sorted(fused.items(), key=lambda x: x[1], reverse=True)
