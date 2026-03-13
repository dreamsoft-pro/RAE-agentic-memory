from typing import Any, Dict, List, Optional
from ...interfaces.storage import IMemoryStorage

class InformationDensityGuard:
    """Agnostic check for memory structure and linkage."""
    def validate(self, payload: Dict[str, Any], contracts: List[Dict[str, Any]]) -> Dict[str, Any]:
        layer = payload.get("layer", "episodic")
        metadata = payload.get("metadata", {})
        
        # Linkage is universal: knowledge must be connected
        if layer in ["semantic", "longterm"]:
            has_links = metadata.get("related_to") or metadata.get("parent_id")
            if not has_links:
                return {"violation": "topological_orphan", "msg": "Information is isolated. Requires relationship links."}
        
        return {"density_status": "ok"}

class ModelEfficiencyGuard:
    """Enforces Model Economy based on task complexity."""
    def validate(self, payload: Dict[str, Any], contracts: List[Dict[str, Any]]) -> Dict[str, Any]:
        model_used = payload.get("metadata", {}).get("model", "unknown")
        content_length = len(payload.get("analysis", ""))
        
        economy_contract = next((c for c in contracts if c.get("metadata", {}).get("id") == "model_economy"), None)
        if economy_contract:
            # Universal complexity check: small tasks don't need SOTA
            if "pro" in model_used.lower() and content_length < 100:
                return {"violation": "model_waste", "suggestion": "Use lighter model for low-density information."}
        return {"economy_status": "ok"}

class L2StructuralReflection:
    def __init__(self, storage: Optional[IMemoryStorage] = None):
        self.storage = storage
        self.density_guard = InformationDensityGuard()
        self.efficiency_guard = ModelEfficiencyGuard()

    async def reflect(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        contracts = []
        if self.storage:
            contracts = await self.storage.list_memories(tenant_id=payload.get("tenant_id", "default"), layer="semantic", tags=["global_contract"])
        
        density = self.density_guard.validate(payload, contracts)
        efficiency = self.efficiency_guard.validate(payload, contracts)
        
        violations = []
        if "violation" in density: violations.append(density["violation"])
        if "violation" in efficiency: violations.append(efficiency["violation"])
        
        return {
            "semantic_violations": violations,
            "is_semantically_sound": len(violations) == 0,
            "density_msg": density.get("msg", "ok")
        }
