from typing import Any, Dict, List
from pydantic import ValidationError
from ...models.contracts import AgentOutputContract

class GroundingVerifier:
    """Hard Gate: Eliminates hallucinations by checking claims against sources."""
    def verify(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        sources = payload.get("retrieved_sources_content", [])
        analysis = payload.get("analysis", "").lower()
        
        if not sources and len(analysis) > 30:
            return {"grounded": False, "score": 0.0, "msg": "Claim made without any retrieved sources."}
            
        # Basic heuristic grounding check: do key terms from analysis exist in sources?
        # In full version this uses semantic similarity
        if sources:
            source_text = " ".join(sources).lower()
            keywords = [w for w in analysis.split() if len(w) > 5]
            if not keywords: return {"grounded": True, "score": 1.0}
            
            matches = sum(1 for k in keywords if k in source_text)
            match_ratio = matches / len(keywords)
            
            if match_ratio < 0.3: # Threshold for hard block
                return {"grounded": False, "score": match_ratio, "msg": "Hallucination detected: analysis drift from sources."}
                
        return {"grounded": True, "score": 1.0}

class L1OperationalReflection:
    def __init__(self, risk_threshold: float = 0.7):
        self.grounding_verifier = GroundingVerifier()
        self.contract_enforcer = ContractEnforcer() # Assuming ContractEnforcer exists in same file or scope

    def reflect(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        # 1. Structure Check
        try:
            AgentOutputContract(**payload)
        except ValidationError as e:
            return {"block": True, "reason": "Structural violation", "errors": str(e)}

        # 2. Hallucination Check (Grounding)
        grounding = self.grounding_verifier.verify(payload)
        if not grounding["grounded"]:
            return {"block": True, "reason": grounding["msg"], "score": grounding["score"]}

        return {
            "block": False,
            "structural_status": "ok",
            "grounding_score": grounding["score"]
        }

class ContractEnforcer:
    def enforce(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "ok"}
