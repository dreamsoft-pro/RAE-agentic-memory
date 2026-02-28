from typing import Any, Dict, List, Optional
from ...interfaces.storage import IMemoryStorage

class RetrievalAnalyzer:
    def analyze(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        sources = payload.get("retrieved_sources", [])
        quality = 1.0 if sources else 0.0
        return {"retrieval_quality": quality}

class SemanticConsistencyChecker:
    def check(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        decision = payload.get("decision", "")
        sources = payload.get("retrieved_sources", [])
        if not sources and decision not in ["insufficient_data", "retry"]:
            return {"violation": "grounding_error", "msg": "Decision requires evidence"}
        return {"consistency_status": "ok"}

class PatternDetector:
    def detect(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"insight_candidates": []}

class CostOptimizer:
    def optimize(self, payload: Dict[str, Any], contracts: List[Dict[str, Any]]) -> Dict[str, Any]:
        model_used = payload.get("metadata", {}).get("model", "unknown")
        analysis = payload.get("analysis", "")
        economy_contract = next((c for c in contracts if c.get("metadata", {}).get("id") == "model_economy"), None)
        if economy_contract:
            rules = economy_contract.get("metadata", {}).get("rules", [{}])[0]
            sota_models = rules.get("sota_models", [])
            is_heavy = any(m in model_used.lower() for m in sota_models)
            if is_heavy and len(analysis) < 50:
                return {"violation": "model_waste", "suggestion": "Use cheaper model"}
        return {"economy_status": "ok"}

class L2StructuralReflection:
    def __init__(self, storage: Optional[IMemoryStorage] = None):
        self.storage = storage
        self.retrieval_analyzer = RetrievalAnalyzer()
        self.consistency_checker = SemanticConsistencyChecker()
        self.pattern_detector = PatternDetector()
        self.cost_optimizer = CostOptimizer()

    async def reflect(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        contracts = []
        if self.storage:
            contracts = await self.storage.list_memories(
                tenant_id=payload.get("tenant_id", "default"),
                layer="semantic",
                tags=["global_contract"]
            )
        retrieval = self.retrieval_analyzer.analyze(payload)
        consistency = self.consistency_checker.check(payload)
        cost = self.cost_optimizer.optimize(payload, contracts)
        
        violations = []
        if "violation" in consistency: violations.append(consistency["violation"])
        if "violation" in cost: violations.append(cost["violation"])
        
        return {
            "semantic_violations": violations,
            "is_semantically_sound": len(violations) == 0,
            "consistency_msg": consistency.get("msg", "ok")
        }
