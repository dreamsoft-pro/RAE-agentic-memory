"""Tests for Semantic Resonance Engine."""

from rae_core.math.resonance import SemanticResonanceEngine


def test_semantic_resonance_boost():
    engine = SemanticResonanceEngine(resonance_factor=0.5)

    # Initial results: A is a direct match, B is not (low score)
    initial_results = [
        {"id": "mem_A", "search_score": 0.9, "content": "Direct hit"},
        {"id": "mem_B", "search_score": 0.1, "content": "Hidden context"},
    ]

    # Graph: A and B are strongly connected
    graph_edges = [("mem_A", "mem_B", 1.0)]

    resonated, energy = engine.compute_resonance(initial_results, graph_edges)

    mem_B = next(r for r in resonated if r["id"] == "mem_B")

    # B should have a significantly higher math_score now
    assert mem_B["math_score"] > 0.1
    assert "resonance_metadata" in mem_B
    assert mem_B["resonance_metadata"]["boost"] > 0


def test_resonance_waves_multi_hop():
    engine = SemanticResonanceEngine(resonance_factor=0.5, iterations=2)

    id_a = "mem_A"
    id_b = "mem_B"

    # Initial results
    initial = [
        {"id": id_a, "search_score": 0.8, "content": "Doc A"},
        {"id": id_b, "search_score": 0.2, "content": "Doc B"},
    ]

    # Graph: A -> B
    edges = [(id_a, id_b, 1.0)]

    results, energy = engine.compute_resonance(initial, edges)

    boosted_b = [r for r in results if r["id"] == id_b][0]
    assert boosted_b["math_score"] > 0.2
    assert "resonance_metadata" in boosted_b


def test_resonance_energy_map_includes_neighbors():
    engine = SemanticResonanceEngine(resonance_factor=0.5, iterations=1)

    id_a = "mem_A"
    id_c = "mem_C"  # Not in initial results

    initial = [{"id": id_a, "search_score": 0.9}]
    edges = [(id_a, id_c, 1.0)]

    _, energy = engine.compute_resonance(initial, edges)

    # Energy map must contain Doc C even if it wasn't in initial results
    assert id_c in energy
    assert energy[id_c] > 0.0
