"""
Theory Evolution Contract - Tesla 3-6-9 Edition.
Defines hard rules for experimental data partitioning and storage.
Zero Drift Policy: naming conventions are enforced via code, not comments.
"""

import json
import uuid
from typing import Dict, Any, List
from datetime import datetime
from uuid import UUID

class EvolutionContract:
    """
    Hard contract for identity and data integrity in RAE Evolution.
    Enforces ISO 42001/27001 via deterministic UUIDs and required schemas.
    """
    # RAE System Namespace (Deterministic base for UUID v5)
    RAE_NAMESPACE = UUID("550e8400-e29b-41d4-a716-446655440000")
    
    PREFIX = "EVO"
    ARCH_VERSION = "369"

    # Strict Schema Requirements
    REQUIRED_MEMORY_FIELDS = [
        "content", "importance", "layer", "metadata", "tenant_id", "agent_id"
    ]

    @classmethod
    def generate_deterministic_id(cls, seed: str) -> UUID:
        """Generates a stable, non-zero UUID v5 based on RAE namespace."""
        return uuid.uuid5(cls.RAE_NAMESPACE, seed)

    @classmethod
    def generate_tenant_id(cls, domain: str, generation: int) -> UUID:
        """Generates a deterministic UUID for a specific experiment tenant."""
        seed = f"{cls.PREFIX}-{domain.lower()}-{cls.ARCH_VERSION}-{generation:04d}"
        return cls.generate_deterministic_id(seed)

    @classmethod
    def validate_memory_payload(cls, payload: Dict[str, Any]):
        """Ensures all ISO-required fields are present before storage."""
        missing = [f for f in cls.REQUIRED_MEMORY_FIELDS if f not in payload]
        if missing:
            raise ValueError(f"ISO Compliance Error: Missing required fields: {missing}")

    @classmethod
    def generate_human_label(cls, domain: str, generation: int) -> str:
        """Generates a human-friendly name for an experiment."""
        return f"{domain.capitalize()}-{cls.ARCH_VERSION}-Gen-{generation:04d}"

    @staticmethod
    def get_reflective_payload(mrr: float, genome: Dict[str, Any], rationale: str, trace_id: str, tenant_id: UUID) -> Dict[str, Any]:
        """
        Structure for storing the result in RAE Reflective Memory.
        ISO 42001 Compliant: includes Rationale, Traceability, and Human Label.
        """
        # Extract domain from metadata or use a default for the label
        domain = genome.get("domains", {}).get("industrial", {}).get("name", "Industrial")
        gen = genome.get("generation", 0)
        human_label = EvolutionContract.generate_human_label(domain, gen)

        payload = {
            "content": f"Theory Evolution Result: MRR {mrr:.4f} | Rationale: {rationale}",
            "importance": mrr,
            "layer": "reflective",
            "tenant_id": str(tenant_id),
            "agent_id": "RAE-Evolver-v369",
            "metadata": {
                "type": "evolution_audit_iso",
                "human_label": human_label,
                "mrr": mrr,
                "genome": genome,
                "rationale": rationale,
                "trace_id": str(trace_id),
                "iso_compliance": ["ISO-27001", "ISO-42001"],
                "timestamp": datetime.now().isoformat()
            }
        }
        # Final validation against the contract
        EvolutionContract.validate_memory_payload(payload)
        return payload
