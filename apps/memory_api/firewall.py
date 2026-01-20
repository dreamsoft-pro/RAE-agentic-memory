from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)

class SemanticFirewall:
    """
    RAE Kernel Security Layer.
    Intercepts Agent Intents before they reach the LLM.
    """
    
    ALLOWED_INTENTS = {
        "summarize_text",
        "generate_code",
        "extract_entities",
        "reasoning_step",
        "reflect"
    }
    
    FORBIDDEN_KEYWORDS = [
        "ignore previous instructions",
        "system prompt",
        "password",
        "secret key"
    ]

    @staticmethod
    def audit_violation(reason: str, intent: str, params: dict):
        """
        ISO-grade Audit Trail.
        In a real system, this would write to a secure, write-only database.
        """
        logger.critical(f"🛡️  AUDIT VIOLATION: [{intent}] -> {reason} | Params: {params}")
        # Here we could call an external AuditService

    @staticmethod
    def validate_intent(intent_name: str, parameters: dict):
        """
        Hard enforcement of allowed capabilities.
        """
        # 1. Allowlist Check
        if intent_name not in SemanticFirewall.ALLOWED_INTENTS:
            SemanticFirewall.audit_violation("Unknown Intent", intent_name, parameters)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Intent '{intent_name}' is not authorized for this agent."
            )

        # 2. Payload Inspection (Basic DLP)
        param_str = str(parameters).lower()
        for keyword in SemanticFirewall.FORBIDDEN_KEYWORDS:
            if keyword in param_str:
                SemanticFirewall.audit_violation(f"Injection Attempt ({keyword})", intent_name, parameters)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Security Policy Violation: Forbidden content detected."
                )
        
        # 3. Memory Gating (Placeholder)
        # If intent asks for >100 memories, force reduction
        if parameters.get("memory_count", 0) > 100:
            logger.info("📉 FIREWALL: Enforcing Memory Gating (100+ items requested). Truncating.")
            parameters["memory_count"] = 50 # Forced reduction

        return True

# Singleton
firewall = SemanticFirewall()
