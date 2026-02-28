from typing import Any, Dict, List
from pydantic import ValidationError
from ...models.contracts import AgentOutputContract

class EvidenceVerifier:
    def verify(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        sources = payload.get("retrieved_sources", [])
        analysis = payload.get("analysis", "")
        
        coverage_ratio = 1.0 if sources else 0.0
        if not sources and len(analysis) > 50:
            coverage_ratio = 0.0
        
        return {
            "coverage_ratio": coverage_ratio,
            "has_sources": len(sources) > 0
        }

class ContractEnforcer:
    def enforce(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            validated = AgentOutputContract(**payload)
            return {
                "status": "valid",
                "schema": "AgentOutputContract v1.0",
                "data": validated.model_dump()
            }
        except ValidationError as e:
            return {
                "status": "invalid",
                "errors": [str(err["msg"]) for err in e.errors()],
                "block": True
            }

class UncertaintyEstimator:
    def estimate(self, payload: Dict[str, Any]) -> Dict[str, float]:
        confidence = payload.get("confidence", 0.0)
        sources = payload.get("retrieved_sources", [])
        risk = 0.0
        if confidence > 0.8 and not sources:
            risk = 0.9
        return {"epistemic_risk": risk}

class L1OperationalReflection:
    def __init__(self, risk_threshold: float = 0.7):
        self.evidence_verifier = EvidenceVerifier()
        self.contract_enforcer = ContractEnforcer()
        self.uncertainty_estimator = UncertaintyEstimator()
        self.risk_threshold = risk_threshold

    def reflect(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        contract = self.contract_enforcer.enforce(payload)
        if contract.get("status") == "invalid":
            return {"block": True, "reason": "Structural contract violation", "errors": contract.get("errors")}

        evidence = self.evidence_verifier.verify(payload)
        risk = self.uncertainty_estimator.estimate(payload)

        block = False
        reasons = []
        if risk.get("epistemic_risk", 0.0) > self.risk_threshold:
            block = True
            reasons.append("Extreme epistemic risk")

        return {
            "block": block,
            "reasons": reasons,
            "structural_status": "ok",
            "evidence_coverage": evidence.get("coverage_ratio"),
            "risk_level": risk.get("epistemic_risk")
        }
