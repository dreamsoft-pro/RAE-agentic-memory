"""
RAE Math - Semantic Resonance Engine

Implements graph-based contextual reinforcement for memory retrieval.
This allows RAE-Lite to achieve 'quasi-reasoning' without an LLM by
analyzing the connectivity and centrality of retrieved memory manifolds.
"""

from typing import Any

import numpy as np


class SemanticResonanceEngine:
    """
    Orchestrates contextual reinforcement using memory graph topology.
    Uses 'Resonance Waves' to spread query energy across the memory manifold.
    """

    def __init__(self, resonance_factor: float = 0.3, iterations: int = 2):
        self.resonance_factor = resonance_factor
        self.iterations = iterations

    def compute_resonance(
        self,
        initial_results: list[dict[str, Any]],
        graph_edges: list[tuple[str, str, float]],
    ) -> tuple[list[dict[str, Any]], dict[str, float]]:
        """
        Adjust initial scores based on graph connectivity (Semantic Resonance).
        Returns (boosted_results, full_energy_map).

        SYSTEM 40.0: Density-Aware Scaling.
        """
        if not initial_results:
            return initial_results, {}

        # 1. Calculate Graph Density for scaling
        all_nodes = set()
        for u, v, _ in graph_edges:
            all_nodes.add(str(u))
            all_nodes.add(str(v))
        
        v_count = len(all_nodes)
        e_count = len(graph_edges)
        
        # Density D = 2|E| / (|V|(|V|-1))
        density = (2 * e_count) / (v_count * (v_count - 1)) if v_count > 1 else 0.0
        
        # Dynamic resonance factor: dampen in high-density areas to prevent noise saturation
        # Formula: factor = base_factor * exp(-density * 2.0)
        # This keeps resonance high (base_factor) for sparse graphs and drops it for dense ones.
        dynamic_factor = self.resonance_factor * np.exp(-density * 5.0)

        # 2. Initialize energy state
        energy = {str(r["id"]): r.get("search_score", 0.5) for r in initial_results}

        if not graph_edges:
            return initial_results, energy

        # Ensure all nodes have an entry in energy map
        for node_id in all_nodes:
            if node_id not in energy:
                energy[node_id] = 0.0

        # 3. Spread energy through waves (Multi-hop)
        damping = 0.85
        for _ in range(self.iterations):
            new_energy = {node_id: 0.0 for node_id in energy}

            for u, v, weight in graph_edges:
                u_str, v_str = str(u), str(v)

                # Bi-directional flow
                new_energy[u_str] += energy[v_str] * weight * dynamic_factor
                new_energy[v_str] += energy[u_str] * weight * dynamic_factor

            # Apply damping and update state
            for node_id in energy:
                energy[node_id] = (energy[node_id] * (1 - damping)) + (
                    new_energy[node_id] * damping
                )

        # 4. Update results with boosted scores
        for r in initial_results:
            r_id_str = str(r["id"])
            original_score = r.get("math_score") or r.get("search_score", 0.0)
            boost = energy.get(r_id_str, 0.0)

            # Non-linear combining (soft saturation)
            r["math_score"] = float(
                original_score + (1.0 - original_score) * np.tanh(boost)
            )
            r["resonance_metadata"] = {
                "boost": float(boost),
                "wave_energy": float(np.tanh(boost)),
                "graph_density": float(density),
                "dynamic_resonance_factor": float(dynamic_factor),
            }

        # 5. Final sort by the new 'Resonated' score
        initial_results.sort(key=lambda x: x.get("math_score", 0.0), reverse=True)
        return initial_results, energy

    def detect_conceptual_clusters(
        self, memories: list[dict[str, Any]]
    ) -> dict[str, list[str]]:
        """
        Groups memories into high-density conceptual manifolds.
        Useful for synthesizing context without an LLM.
        """
        # Placeholder for future spectral clustering logic
        return {"main_cluster": [m["id"] for m in memories]}
