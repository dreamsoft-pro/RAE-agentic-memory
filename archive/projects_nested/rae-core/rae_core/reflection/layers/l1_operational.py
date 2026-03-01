from typing import Any, Dict, List
from pydantic import ValidationError
from ...models.contracts import AgentOutputContract

class ContractEnforcer:
    def enforce(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            AgentOutputContract(**payload)
            return {"status": "ok"}
        except ValidationError as e:
            return {"status": "invalid", "errors": str(e), "block": True}

class UncertaintyEstimator:
    def estimate(self, payload: Dict[str, Any]) -> Dict[str, float]:
        confidence = payload.get("confidence", 0.0)
        risk = 0.9 if confidence > 0.8 and not payload.get("retrieved_sources") else 0.0
        return {"epistemic_risk": risk}

class L1OperationalReflection:
    def __init__(self, risk_threshold: float = 0.7):
        self.contract_enforcer = ContractEnforcer()
        self.uncertainty_estimator = UncertaintyEstimator()
        self.risk_threshold = risk_threshold

    def reflect(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        contract = self.contract_enforcer.enforce(payload)
        if contract.get("status") == "invalid":
            return {"block": True, "reason": "Structural contract violation", "errors": contract.get("errors")}

        risk = self.uncertainty_estimator.estimate(payload)
        block = risk.get("epistemic_risk", 0.0) > self.risk_threshold
        
        return {
            "block": block,
            "structural_status": "ok",
            "risk_level": risk.get("epistemic_risk")
        }
