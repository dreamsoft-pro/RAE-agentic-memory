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
import sys
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
        # Use current python interpreter for sub-processes
        self.python_bin = sys.executable
        
    def load_genome(self) -> Dict[str, Any]:
        if os.path.exists(GENOME_PATH):
            with open(GENOME_PATH, "r") as f:
                return json.load(f)
        return {
            "best_mrr": 0.0, 
            "generation": 0, 
            "domains": {},
            "pillars": {
                "logos": {"weight": 0.7},
                "psyche": {"weight": 0.3},
                "noos": {"weight": 0.5}
            }
        }

    def save_genome(self):
        with open(GENOME_PATH, "w") as f:
            json.dump(self.genome, f, indent=4)

    def mutate(self):
        """Mutates the genome using Structural Evolution (Tesla 3-6-9 Harmony)."""
        self.current_trace_id = str(uuid.uuid4())
        logger.info("evolution_mutation_start", 
                    generation=self.genome["generation"], 
                    trace_id=self.current_trace_id)
        
        if "industrial" not in self.genome["domains"]:
            self.genome["domains"]["industrial"] = {
                "sequence": ["logos", "synergy", "entropy", "decay"], 
                "params": {"logic_boost": 19.0, "synergy_factor": 3.0, "entropy_penalty": 0.5}
            }
            
        domain_cfg = self.genome["domains"]["industrial"]
        params = domain_cfg["params"]
        sequence = domain_cfg["sequence"]
        
        # Ensure pillars exist
        if "pillars" not in self.genome:
            self.genome["pillars"] = {
                "logos": {"weight": 0.7},
                "psyche": {"weight": 0.3},
                "noos": {"weight": 0.5}
            }
        
        # Determine mutation type: 40% Parametric, 40% Structural, 20% Pillar
        dice = random.random()
        
        if dice < 0.4:
            # 1. Parametric Mutation (Fine-tuning)
            # Ensure all available params are considered
            all_params = list(params.keys())
            for p in ["identity_signal_weight", "shape_signal_weight", "temporal_signal_weight"]:
                if p not in all_params: all_params.append(p)
                
            param_to_mutate = random.choice(all_params)
            tesla_factor = random.choice([3, 6, 9])
            
            if param_to_mutate == "logic_boost":
                params["logic_boost"] = max(1.0, params.get("logic_boost", 19.0) + (tesla_factor if random.random() > 0.5 else -tesla_factor))
            elif "signal_weight" in param_to_mutate:
                current = params.get(param_to_mutate, 1.0)
                params[param_to_mutate] = current * 1.5 if random.random() > 0.5 else current * 0.5
            else:
                current = params.get(param_to_mutate, 1.0)
                params[param_to_mutate] = current * 1.3 if random.random() > 0.5 else current * 0.7
                
            self.current_rationale = f"Parametric drift of {param_to_mutate} using Tesla factor {tesla_factor}."

        elif dice < 0.8:
            # 2. Structural Mutation (Architecture change)
            from rae_core.math.theories.atlas import MODULATORS
            available_modulators = list(MODULATORS.keys())
            
            sub_dice = random.random()
            if sub_dice < 0.4 and len(sequence) > 1:
                # Swap (Reorder)
                idx1, idx2 = random.sample(range(len(sequence)), 2)
                sequence[idx1], sequence[idx2] = sequence[idx2], sequence[idx1]
                self.current_rationale = f"Structural reorder: swapped elements in cascade."
            elif sub_dice < 0.7:
                # Add new theory from Atlas
                new_theory = random.choice(available_modulators)
                if new_theory not in sequence:
                    sequence.insert(random.randint(0, len(sequence)), new_theory)
                    self.current_rationale = f"Structural expansion: added {new_theory} to cascade."
                else:
                    self.current_rationale = "Structural mutation skipped: theory already in sequence."
            else:
                # Remove theory
                if len(sequence) > 1:
                    removed = sequence.pop(random.randint(0, len(sequence)-1))
                    self.current_rationale = f"Structural reduction: removed {removed} from cascade."
                else:
                    self.current_rationale = "Structural mutation skipped: sequence too short."

        else:
            # 3. Pillar Mutation (Philosophical balance)
            pillar = random.choice(["logos", "psyche", "noos"])
            current_weight = self.genome["pillars"][pillar]["weight"]
            self.genome["pillars"][pillar]["weight"] = min(1.0, max(0.1, current_weight + (0.1 if random.random() > 0.5 else -0.1)))
            self.current_rationale = f"Philosophical shift: adjusted {pillar} weight to {self.genome['pillars'][pillar]['weight']:.2f}."
            
        self.genome["generation"] += 1

    def run_experiment(self) -> float:
        """Executes the benchmark in a stable sandbox tenant and returns MRR."""
        # Fixed Sandbox Tenant ID (ISO Compliant Namespace)
        tenant_id = "550e8400-e29b-41d4-a716-446655440000"
        
        benchmark_cmd = [
            self.python_bin, 
            "benchmarking/scripts/run_benchmark.py", 
            "--set", "benchmarking/sets/industrial_small.yaml",
            "--tenant", tenant_id
        ]
        
        logger.info("evolution_experiment_run", 
                    cmd=" ".join(benchmark_cmd), 
                    tenant=tenant_id,
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

    def save_to_iso_audit(self, mrr: float, tenant_id: uuid.UUID):
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

    def run_tournament(self):
        """Systematically tests every theory in the Atlas alone with default params."""
        from rae_core.math.theories.atlas import MODULATORS
        logger.info("evolution_tournament_start", total_theories=len(MODULATORS))
        
        results = {}
        
        for name in MODULATORS.keys():
            logger.info("tournament_round_start", theory=name)
            
            # Temporary override genome to test ONLY this theory
            original_sequence = self.genome["domains"]["industrial"]["sequence"]
            self.genome["domains"]["industrial"]["sequence"] = [name]
            self.save_genome()
            
            mrr = self.run_experiment()
            results[name] = mrr
            logger.info("tournament_round_result", theory=name, mrr=mrr)
            
            # Restore
            self.genome["domains"]["industrial"]["sequence"] = original_sequence
            
        # Sort and report
        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
        print("\n🏆 THEORY TOURNAMENT RESULTS (Baseline MRR):")
        for name, mrr in sorted_results:
            print(f"   - {name:15}: {mrr:.4f}")
        print("\n")
        
        return sorted_results

if __name__ == "__main__":
    evolver = TheoryEvolver()
    
    # 1. Run Tournament to see who is the baseline leader
    evolver.run_tournament()
    
    # 2. Run Final Evolution (Structural & Parametric) - 200 generations
    for _ in range(200):
        evolver.step()
