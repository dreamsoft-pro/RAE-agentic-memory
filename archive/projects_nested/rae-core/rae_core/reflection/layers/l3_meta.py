from typing import Any, Dict, List, Optional
from ...interfaces.storage import IMemoryStorage

class EpistemicProvenanceGuard:
    """Agnostic Level 3: Ensures all knowledge has verifiable origins."""
    def verify(self, payload: Dict[str, Any], previous_results: Dict[str, Any], contracts: List[Dict[str, Any]]) -> Dict[str, Any]:
        anomalies = []
        metadata = payload.get("metadata", {})
        layer = payload.get("layer", "episodic")
        
        # Rule: Persistent knowledge MUST have provenance (source)
        if layer in ["semantic", "longterm"]:
            if not metadata.get("source_id") and not metadata.get("retrieved_sources"):
                anomalies.append({
                    "type": "provenance_gap",
                    "severity": 0.8,
                    "msg": "Knowledge promotion without explicit evidence link."
                })

        # Rule: Conflict Detection (Episodic vs Semantic)
        # Placeholder for cross-layer contradiction check
        
        return {"epistemic_anomalies": anomalies, "field_stable": len(anomalies) == 0}

class L3MetaFieldReflection:
    def __init__(self, storage: Optional[IMemoryStorage] = None):
        self.storage = storage
        self.provenance_guard = EpistemicProvenanceGuard()

    async def reflect(self, payload: Dict[str, Any], previous_results: Dict[str, Any] = None) -> Dict[str, Any]:
        if not previous_results: return {"status": "skipped"}
        contracts = []
        if self.storage:
            contracts = await self.storage.list_memories(tenant_id=payload.get("tenant_id", "default"), layer="semantic", tags=["global_contract"])
        
        provenance = self.provenance_guard.verify(payload, previous_results, contracts)
        block = any(a["severity"] > 0.8 for a in provenance["epistemic_anomalies"])
        
        return {"block": block, "epistemic_anomalies": provenance["epistemic_anomalies"]}
