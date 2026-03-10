"""
RAE Theory Evolver - Tesla 3-6-9 Edition
Inspired by Andrej Karpathy's 'autoresearch'.
Autonomously evolves mathematical strategies to hit MRR 1.0.
"""

import json
import os
import subprocess
import random
import uuid
import structlog
from typing import Dict, Any
from rae_core.math.theories.contract import EvolutionContract

logger = structlog.get_logger(__name__)

GENOME_PATH = "rae-core/rae_core/math/theories/theory_genome.json"
ISO_AUDIT_PATH = "ISO_AUDIT_GENEALOGY.jsonl"

class TheoryEvolver:
    def __init__(self):
        self.genome = self.load_genome()
        self.current_rationale = ""
        self.current_trace_id = ""
        
    def load_genome(self) -> Dict[str, Any]:
        if os.path.exists(GENOME_PATH):
            with open(GENOME_PATH, "r") as f:
                return json.load(f)
        return {"best_mrr": 0.0, "generation": 0, "domains": {}}

    def save_genome(self):
        with open(GENOME_PATH, "w") as f:
            json.dump(self.genome, f, indent=4)

    def mutate(self):
        """Mutates the genome using Tesla 3-6-9 harmonics with ISO Rationale."""
        self.current_trace_id = str(uuid.uuid4())
        logger.info("evolution_mutation_start", 
                    generation=self.genome["generation"], 
                    trace_id=self.current_trace_id)
        
        # 1. Mutate Industrial Domain (Our current target)
        if "industrial" not in self.genome["domains"]:
            self.genome["domains"]["industrial"] = {"sequence": ["logos", "synergy", "entropy", "decay"], "params": {}}
            
        params = self.genome["domains"]["industrial"]["params"]
        
        # Choose which parameter to mutate
        param_to_mutate = random.choice(["logic_boost", "synergy_factor", "entropy_penalty"])
        tesla_factor = random.choice([3, 6, 9])
        
        if param_to_mutate == "logic_boost":
            current = params.get("logic_boost", 10.0)
            change = tesla_factor if random.random() > 0.5 else -tesla_factor
            params["logic_boost"] = max(1.0, current + change)
            self.current_rationale = f"Adjusted logic_boost by {change} to sharpen/relax technical identity matching (Logos Pillar)."
            
        elif param_to_mutate == "synergy_factor":
            current = params.get("synergy_factor", 3.0)
            # Factor-based mutation for synergy
            direction = "increase" if random.random() > 0.5 else "decrease"
            params["synergy_factor"] = current * 1.3 if direction == "increase" else max(1.1, current / 1.3)
            self.current_rationale = f"{direction.capitalize()}d synergy_factor to modulate non-linear cross-theory agreement."
            
        elif param_to_mutate == "entropy_penalty":
            current = params.get("entropy_penalty", 0.5)
            direction = "increase" if random.random() > 0.5 else "decrease"
            params["entropy_penalty"] = min(1.0, current + 0.1) if direction == "increase" else max(0.0, current - 0.1)
            self.current_rationale = f"{direction.capitalize()}d entropy_penalty to filter out search noise."
            
        self.genome["generation"] += 1

    def run_experiment(self) -> float:
        """Executes the benchmark in a stable sandbox tenant and returns MRR."""
        # Use a deterministic UUID v5 for sandbox instead of strings/zeros
        tenant_id = EvolutionContract.generate_deterministic_id("EVO-SANDBOX-369")
        
        benchmark_cmd = [
            ".venv/bin/python3", 
            "benchmarking/scripts/run_benchmark.py", 
            "--set", "benchmarking/sets/industrial_small.yaml",
            "--tenant", str(tenant_id)
        ]
        
        logger.info("evolution_experiment_run", 
                    cmd=" ".join(benchmark_cmd), 
                    tenant=str(tenant_id),
                    trace_id=self.current_trace_id,
                    iso_audit=True)
        
        try:
            result = subprocess.run(benchmark_cmd, capture_output=True, text=True, timeout=300)
            
            # Parse MRR from output
            for line in result.stdout.split("\n"):
                if "MRR:" in line:
                    return float(line.split(":")[1].strip())
        except Exception as e:
            logger.error("experiment_failed", error=str(e), trace_id=self.current_trace_id)
            
        return 0.0

    def step(self):
        """One step of the evolution loop with ISO tracking."""
        backup_genome = json.loads(json.dumps(self.genome))
        
        self.mutate()
        self.save_genome()
        
        new_mrr = self.run_experiment()
        logger.info("evolution_result", 
                    mrr=new_mrr, 
                    best_mrr=backup_genome["best_mrr"],
                    trace_id=self.current_trace_id)
        
        # 2. Persist to ISO Audit Log (RAE-First Mandate)
        try:
            # Generate deterministic tenant ID for this generation's record
            tenant_id = EvolutionContract.generate_tenant_id("industrial", self.genome["generation"])
            self.save_to_iso_audit(new_mrr, tenant_id)
        except Exception as e:
            logger.error("iso_audit_failed", error=str(e))

        if new_mrr > backup_genome["best_mrr"]:
            logger.info("evolution_improvement_found", mrr=new_mrr, trace_id=self.current_trace_id)
            self.genome["best_mrr"] = new_mrr
            self.save_genome()
        else:
            logger.info("evolution_reverting", trace_id=self.current_trace_id)
            self.genome = backup_genome
            self.save_genome()

    def save_to_iso_audit(self, mrr: float, tenant_id: UUID):
        """Saves the experiment result to the ISO Compliance Genealogy log."""
        payload = EvolutionContract.get_reflective_payload(
            mrr, 
            self.genome, 
            self.current_rationale, 
            self.current_trace_id,
            tenant_id
        )
        
        # Audit Record for ISO 42001
        audit_record = {
            "iso_audit": True,
            "trace_id": self.current_trace_id,
            "human_label": payload["metadata"]["human_label"],
            "tenant": str(tenant_id),
            "agent_id": payload["agent_id"],
            "action": "mutate_theory_params",
            "rationale": self.current_rationale,
            "result_mrr": mrr,
            "genome_state": self.genome,
            "compliance": payload["metadata"]["iso_compliance"],
            "timestamp": payload["metadata"]["timestamp"]
        }
        
        with open(ISO_AUDIT_PATH, "a") as f:
            f.write(json.dumps(audit_record) + "\n")
            
        logger.info("iso_compliance_logged", trace_id=self.current_trace_id, path=ISO_AUDIT_PATH)

if __name__ == "__main__":
    evolver = TheoryEvolver()
    # Run 5 generations to find better synergy
    for _ in range(5):
        evolver.step()
