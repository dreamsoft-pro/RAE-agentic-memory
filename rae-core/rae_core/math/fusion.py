"""
RAE Fusion Strategies (System 40.x).
Modular, atomic logic for combining search results.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple, Optional
from uuid import UUID
import math
import structlog

logger = structlog.get_logger(__name__)

class AbstractFusionStrategy(ABC):
    """Base class for all fusion strategies."""
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}

    @abstractmethod
    async def fuse(
        self,
        strategy_results: Dict[str, List],
        query: str,
        h_sys: float = 13.0,
        memory_contents: Optional[Dict[UUID, Dict]] = None,
        weights: Optional[Dict[str, float]] = None,
        **kwargs: Any,
    ) -> List[Tuple[UUID, float, float, Dict]]:
        pass

class Legacy416Strategy(AbstractFusionStrategy):
    """
    SYSTEM 4.16: High Precision RRF + Anchor Lock.
    """
    async def fuse(
        self,
        strategy_results: Dict[str, List],
        query: str,
        h_sys: float = 13.0,
        memory_contents: Optional[Dict[UUID, Dict]] = None,
        weights: Optional[Dict[str, float]] = None,
        **kwargs: Any,
    ) -> List[Tuple[UUID, float, float, Dict]]:
        cfg = self.config.get("strategies_config", {}).get("legacy_416", {})
        k = cfg.get("k_factor", 1.0)
        anchor_boost = cfg.get("anchor_lock_boost", 1000.0)
        partial_multiplier = cfg.get("partial_anchor_multiplier", 10.0)
        
        fused_scores: dict[UUID, float] = {}
        for strategy, results in strategy_results.items():
            if not results: continue
            for rank, item in enumerate(results):
                m_id = item[0] if isinstance(item, tuple) else (item.get("id") or item.get("memory_id"))
                if isinstance(m_id, str):
                    try: m_id = UUID(m_id)
                    except ValueError: pass 
                fused_scores[m_id] = fused_scores.get(m_id, 0.0) + (1.0 / (rank + k))

        processed = []
        q_lower = query.lower()
        symbols = [t for t in q_lower.split() if any(c.isdigit() for c in t) or any(c in t for c in "-_.:")]
        
        for m_id, rrf_score in fused_scores.items():
            mem_obj = (memory_contents or {}).get(m_id, {})
            content = mem_obj.get("content", "").lower()
            meta = mem_obj.get("metadata", {})
            
            if isinstance(meta, str):
                import json
                try: meta = json.loads(meta)
                except: meta = {}
            
            importance = float(meta.get("importance", 0.5))
            
            final_score = rrf_score
            audit = {"strategy": "Legacy416", "rrf": round(rrf_score, 4), "tier": 2}
            
            if symbols:
                matched = sum(1 for s in symbols if s in content)
                if matched == len(symbols):
                    final_score += anchor_boost
                    audit["anchor_lock"] = True
                    audit["tier"] = 0
                elif matched > 0:
                    final_score += (matched / len(symbols)) * partial_multiplier
                    audit["partial_anchor"] = round(matched / len(symbols), 2)
                    audit["tier"] = 1

            processed.append((m_id, final_score, importance, audit))
        
        return sorted(processed, key=lambda x: x[1], reverse=True)

class SiliconOracleStrategy(AbstractFusionStrategy):
    """
    SYSTEM 40.4: Pure Entropy-Based Resonance.
    """
    async def fuse(
        self,
        strategy_results: Dict[str, List],
        query: str,
        h_sys: float = 13.0,
        memory_contents: Optional[Dict[UUID, Dict]] = None,
        weights: Optional[Dict[str, float]] = None,
        **kwargs: Any,
    ) -> List[Tuple[UUID, float, float, Dict]]:
        cfg = self.config.get("strategies_config", {}).get("silicon_oracle", {})
        divisor = cfg.get("rank_sharpening_divisor", 3.0)
        
        fused_scores: dict[UUID, float] = {}
        actual_weights = weights or {}
        
        for strategy, results in strategy_results.items():
            w = actual_weights.get(strategy, 1.0)
            for rank, item in enumerate(results):
                m_id = item[0] if isinstance(item, tuple) else (item.get("id") or item.get("memory_id"))
                if isinstance(m_id, str):
                    try: m_id = UUID(m_id)
                    except ValueError: pass
                
                score = w * math.exp(-rank / divisor)
                fused_scores[m_id] = fused_scores.get(m_id, 0.0) + score

        processed = []
        for m_id, score in fused_scores.items():
            mem_obj = (memory_contents or {}).get(m_id, {})
            meta = mem_obj.get("metadata", {})
            importance = float(meta.get("importance", 0.5))
            audit = {"strategy": "SiliconOracle", "fused": round(score, 4)}
            processed.append((m_id, score, importance, audit))
            
        return sorted(processed, key=lambda x: x[1], reverse=True)

class FusionStrategy:
    """
    Gateway class for RAE fusion. 
    Implements positional arguments for backward compatibility with HybridSearchEngine.
    """
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        from rae_core.math.logic_gateway import LogicGateway
        self.gateway = LogicGateway(self.config)

    async def fuse(self, strategy_results=None, weights=None, query="", **kwargs):
        # Handle positional or keyword arguments
        return await self.gateway.fuse(
            strategy_results=strategy_results,
            weights=weights,
            query=query,
            **kwargs
        )
