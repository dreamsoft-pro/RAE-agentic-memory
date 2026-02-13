"""
RAE Fusion Strategies - Modular Architecture (System 40.4)
No hardcoding. Pure Strategy Pattern.
"""

import math
from typing import Any, Dict, List, Tuple
from uuid import UUID
from abc import ABC, abstractmethod
import structlog

logger = structlog.get_logger(__name__)

class AbstractFusionStrategy(ABC):
    @abstractmethod
    async def fuse(
        self,
        strategy_results: Dict[str, List[Any]],
        query: str,
        h_sys: float,
        memory_contents: Dict[UUID, Dict[str, Any]],
        **kwargs
    ) -> List[Tuple[UUID, float, float, Dict]]:
        pass

# Backward Compatibility - This class is still used by engine.py
class FusionStrategy:
    """Delegator for backward compatibility."""
    def __init__(self, config: dict[str, Any] | None = None):
        # We import LogicGateway here to avoid circular imports
        from .logic_gateway import LogicGateway
        self.gateway = LogicGateway(config)

    async def fuse(
        self,
        strategy_results: Dict[str, List[Any]],
        weights: Dict[str, float] | None = None,
        query: str = "",
        config_override: Dict[str, Any] | None = None,
        memory_contents: Dict[UUID, Dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> List[Tuple[UUID, float, float, Dict]]:
        return await self.gateway.fuse(
            strategy_results=strategy_results,
            weights=weights,
            query=query,
            config_override=config_override,
            memory_contents=memory_contents,
            **kwargs
        )

class Legacy416Strategy(AbstractFusionStrategy):
    """
    SYSTEM 4.16: High Precision RRF + Anchor Lock.
    The most stable strategy for industrial IDs and codes.
    """
    async def fuse(
        self,
        strategy_results: Dict[str, List[Any]],
        query: str,
        h_sys: float,
        memory_contents: Dict[UUID, Dict[str, Any]],
        **kwargs
    ) -> List[Tuple[UUID, float, float, Dict]]:
        k = 1.0 
        fused_scores: dict[UUID, float] = {}
        
        for strategy, results in strategy_results.items():
            if not results: continue
            for rank, item in enumerate(results):
                m_id = item[0] if isinstance(item, tuple) else (item.get("id") or item.get("memory_id"))
                if isinstance(m_id, str):
                    try: m_id = UUID(m_id)
                    except ValueError: pass # Keep as string if not a valid UUID
                fused_scores[m_id] = fused_scores.get(m_id, 0.0) + (1.0 / (rank + k))

        processed = []
        q_lower = query.lower()
        symbols = [t for t in q_lower.split() if any(c.isdigit() for c in t) or any(c in t for c in "-_.:")]
        
        for m_id, rrf_score in fused_scores.items():
            mem_obj = memory_contents.get(m_id, {})
            content = mem_obj.get("content", "").lower()
            meta = mem_obj.get("metadata", {})
            
            # Defensive Metadata Parsing
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
                    final_score += 1000.0 
                    audit["anchor_lock"] = True
                    audit["tier"] = 0
                elif matched > 0:
                    final_score += (matched / len(symbols)) * 10.0
                    audit["partial_anchor"] = round(matched / len(symbols), 2)
                    audit["tier"] = 1

            processed.append((m_id, final_score, importance, audit))
        
        return sorted(processed, key=lambda x: x[1], reverse=True)

class SiliconOracleStrategy(AbstractFusionStrategy):
    """
    SYSTEM 40.4: Pure Entropy-Based Resonance.
    Fluid, self-tuning, no hardcoded anchors.
    """
    async def fuse(
        self,
        strategy_results: Dict[str, List[Any]],
        query: str,
        h_sys: float,
        memory_contents: Dict[UUID, Dict[str, Any]],
        **kwargs
    ) -> List[Tuple[UUID, float, float, Dict]]:
        logits_map: dict[UUID, float] = {}
        
        for strategy, results in strategy_results.items():
            if not results: continue
            for rank, item in enumerate(results):
                m_id = item[0] if isinstance(item, tuple) else (item.get("id") or item.get("memory_id"))
                if isinstance(m_id, str):
                    try: m_id = UUID(m_id)
                    except ValueError: pass # Keep as string if not a valid UUID
                p = math.exp(-rank / 3.0)
                logit = math.log(p / (1.0 - p + 1e-9))
                logits_map[m_id] = logits_map.get(m_id, 0.0) + logit

        processed = []
        q_lower = query.lower()
        q_tokens = q_lower.split()
        
        for m_id, combined_logit in logits_map.items():
            mem_obj = memory_contents.get(m_id, {})
            content = mem_obj.get("content", "").lower()
            meta = mem_obj.get("metadata", {})
            
            # Defensive Metadata Parsing
            if isinstance(meta, str):
                import json
                try: meta = json.loads(meta)
                except: meta = {}
                
            importance = float(meta.get("importance", 0.5))
            
            density = sum(content.count(t) for t in q_tokens if len(t) > 3)
            signal = math.log1p(density) * h_sys
            
            total_logit = combined_logit + signal
            audit = {"strategy": "SiliconOracle", "logit": round(total_logit, 2), "h_sys": round(h_sys, 2), "tier": 2}
            
            processed.append((m_id, total_logit, importance, audit))
            
        return sorted(processed, key=lambda x: x[1], reverse=True)
