from typing import Any, Dict, List
import uuid
from rae_core.reflection.layers.l1_operational import L1OperationalReflection
from rae_core.reflection.layers.l2_structural import L2StructuralReflection
from rae_core.reflection.layers.l3_meta import L3MetaFieldReflection
from rae_core.interfaces.storage import IMemoryStorage

class ReflectionCoordinator:
    """
    Coordinates L1, L2, L3 reflections based on mode and aggregates the output JSONs.
    Modes: "minimal" (mobile), "standard" (laptop), "advanced".
    """
    def __init__(
        self, 
        mode: str = "standard", 
        enforce_hard_frames: bool = True,
        storage: IMemoryStorage | None = None
    ):
        self.mode = mode.lower()
        self.enforce_hard_frames = enforce_hard_frames
        self.storage = storage
        
        self.l1 = L1OperationalReflection()
        self.l2 = L2StructuralReflection()
        self.l3 = L3MetaFieldReflection()

    def run_reflections(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synchronous run of all active layers.
        """
        result = {
            "l1_operational": {},
            "l2_structural": {},
            "l3_meta_field": {},
            "final_decision": "pass",
            "block_reasons": []
        }
        
        # L1 is active in all modes
        l1_res = self.l1.reflect(payload)
        result["l1_operational"] = l1_res
        
        if self.enforce_hard_frames and l1_res.get("block"):
            result["final_decision"] = "blocked"
            result["block_reasons"].append("L1 Operational constraints violated")

        # L2 is for "standard" and "advanced"
        if self.mode in ["standard", "advanced"]:
            l2_res = self.l2.reflect(payload)
            result["l2_structural"] = l2_res

        # L3 is for "advanced"
        if self.mode == "advanced":
            l3_res = self.l3.reflect(payload)
            result["l3_meta_field"] = l3_res
            
            if self.enforce_hard_frames and l3_res.get("block"):
                result["final_decision"] = "blocked"
                result["block_reasons"].append("L3 Meta-Field anomalies critical")

        return result

    async def run_and_store_reflections(
        self, 
        payload: Dict[str, Any], 
        tenant_id: str, 
        agent_id: str | None = None
    ) -> Dict[str, Any]:
        """
        Runs reflections and persists result to the audit table if storage is available.
        """
        result = self.run_reflections(payload)
        
        if self.storage:
            query_id = payload.get("query_id", str(uuid.uuid4()))
            fsi = result.get("l3_meta_field", {}).get("field_stability_index", 1.0)
            
            await self.storage.store_reflection_audit(
                query_id=query_id,
                tenant_id=tenant_id,
                agent_id=agent_id,
                fsi_score=fsi,
                final_decision=result["final_decision"],
                l1_report=result["l1_operational"],
                l2_report=result["l2_structural"],
                l3_report=result["l3_meta_field"],
                metadata=payload.get("metadata")
            )
            
        return result
