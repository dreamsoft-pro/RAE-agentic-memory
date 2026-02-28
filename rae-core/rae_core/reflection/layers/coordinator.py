from typing import Any, Dict, List, Optional
from .l1_operational import L1OperationalReflection
from .l2_structural import L2StructuralReflection
from .l3_meta import L3MetaFieldReflection
from ...interfaces.storage import IMemoryStorage

class ReflectionCoordinator:
    def __init__(self, mode: str = "standard", enforce_hard_frames: bool = True, storage: IMemoryStorage | None = None):
        self.mode = mode.lower()
        self.enforce_hard_frames = enforce_hard_frames
        self.storage = storage
        self.l1 = L1OperationalReflection()
        self.l2 = L2StructuralReflection(storage=storage)
        self.l3 = L3MetaFieldReflection(storage=storage)

    async def run_reflections(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        results = {"l1_operational": {}, "l2_structural": {}, "l3_meta_field": {}, "final_decision": "pass", "block_reasons": []}
        
        # L1 is sync for now
        l1_res = self.l1.reflect(payload)
        results["l1_operational"] = l1_res
        if l1_res.get("block"):
            results["final_decision"] = "blocked"
            results["block_reasons"].append(f"L1: {l1_res.get('reason', 'Violation')}")
            if self.enforce_hard_frames: return results
            
        if self.mode in ["standard", "advanced"]:
            l2_res = await self.l2.reflect(payload)
            results["l2_structural"] = l2_res
            if not l2_res.get("is_semantically_sound"):
                if self.mode == "advanced":
                    results["final_decision"] = "blocked"
                    results["block_reasons"].extend(l2_res.get("semantic_violations", []))
                    if self.enforce_hard_frames: return results

        if self.mode == "advanced":
            l3_res = await self.l3.reflect(payload, results)
            results["l3_meta_field"] = l3_res
            if l3_res.get("block"):
                results["final_decision"] = "blocked"
                for a in l3_res.get("epistemic_anomalies", []):
                    results["block_reasons"].append(f"L3 Anomaly: {a['msg']}")
                    
        return results
