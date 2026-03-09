"""Hardened unit tests for all three reflection layers (L1, L2, L3)."""

import pytest
from rae_core.reflection.layers.l1_operational import (
    L1OperationalReflection, EvidenceVerifier, ContractEnforcer, UncertaintyEstimator
)
from rae_core.reflection.layers.l2_structural import (
    L2StructuralReflection, RetrievalAnalyzer, PatternDetector, CostOptimizer
)
from rae_core.reflection.layers.l3_meta import (
    L3MetaFieldReflection, FieldDensityMonitor, RenormalizationEngine, SymmetryAndAnomalyDetector
)

# --- L1 Operational Tests ---

def test_l1_evidence_verifier():
    ev = EvidenceVerifier()
    # No sources, short draft
    assert ev.verify({"answer_draft": "short"})["coverage_ratio"] == 0.0
    # No sources, long draft
    assert ev.verify({"answer_draft": "This is a long draft without sources."})["coverage_ratio"] == 0.0
    # With sources
    assert ev.verify({"retrieved_sources": ["src1"]})["coverage_ratio"] == 1.0

def test_l1_uncertainty_estimator():
    ue = UncertaintyEstimator()
    # Low uncertainty
    res = ue.estimate({"answer_draft": "Fact A is true.", "retrieved_sources": ["s1"]})
    assert res["uncertainty_level"] == 0.0
    # Higher uncertainty due to keywords
    res = ue.estimate({"answer_draft": "Probably true.", "retrieved_sources": ["s1"]})
    assert res["uncertainty_level"] == 0.3
    # High uncertainty due to missing sources
    res = ue.estimate({"answer_draft": "Maybe.", "retrieved_sources": []})
    assert res["uncertainty_level"] == 0.8 # 0.3 + 0.5

def test_l1_operational_reflection_blocking():
    l1 = L1OperationalReflection(coverage_threshold=0.8, max_uncertainty=0.5)
    
    # Blocked by uncertainty
    res = l1.reflect({"answer_draft": "Probably.", "retrieved_sources": []})
    assert res["block"] is True
    assert res["uncertainty_level"] > 0.5
    
    # Not blocked
    res = l1.reflect({"answer_draft": "Certain.", "retrieved_sources": ["s1", "s2"]})
    assert res["block"] is False
    assert res["coverage_ratio"] == 1.0

# --- L2 Structural Tests ---

def test_l2_retrieval_analyzer():
    ra = RetrievalAnalyzer()
    # Good quality
    res = ra.analyze({"answer_draft": "Simple answer", "retrieved_sources": ["s1"]})
    assert res["retrieval_quality"] == 1.0
    # Missed log source
    res = ra.analyze({"answer_draft": "Look at the log files", "retrieved_sources": ["doc1"]})
    assert "log_source" in res["missed_sources"]
    assert res["retrieval_quality"] < 1.0

def test_l2_pattern_detector():
    pd = PatternDetector()
    res = pd.detect({"answer_draft": "The speed drop is visible here."})
    assert any(p["pattern"] == "speed_drop_detected" for p in res["insight_candidates"])

def test_l2_cost_optimizer():
    co = CostOptimizer()
    # High cost suggestion
    res = co.optimize({"retrieved_sources": ["s"] * 25})
    assert res["optimization_suggestion"] == "decrease_top_k"
    # Low info suggestion
    res = co.optimize({"answer_draft": "hi", "retrieved_sources": ["s1"]})
    assert res["optimization_suggestion"] == "increase_top_k"

def test_l2_structural_reflection():
    l2 = L2StructuralReflection()
    res = l2.reflect({"answer_draft": "test", "retrieved_sources": ["s1"]})
    assert "retrieval_quality" in res
    assert "insight_candidates" in res

# --- L3 Meta Tests ---

def test_l3_field_density_monitor():
    fdm = FieldDensityMonitor()
    res = fdm.monitor({"answer_draft": "Local strategy defined."})
    assert "local_first + grant_strategy" in res["emerging_clusters"]

def test_l3_renormalization_engine():
    re = RenormalizationEngine()
    # Contradiction detected
    res = re.renormalize({"answer_draft": "Always true except when false."})
    assert "generalization_contradiction" in res["scale_inconsistencies"]
    assert res["scale_inconsistency_penalty"] > 0

def test_l3_symmetry_anomaly_detector():
    sad = SymmetryAndAnomalyDetector()
    # Policy violation: assertion without evidence
    res = sad.detect({"answer_draft": "A" * 60, "retrieved_sources": []})
    assert any(a["type"] == "policy_violation" for a in res["anomalies"])
    # Domain leakage
    res = sad.detect({"answer_draft": "confidential and public data"})
    assert any(a["type"] == "domain_leakage" for a in res["anomalies"])

def test_l3_meta_field_reflection_blocking():
    l3 = L3MetaFieldReflection(critical_threshold=0.7)
    
    # Blocked by critical anomaly
    res = l3.reflect({"answer_draft": "A" * 100, "retrieved_sources": []})
    assert res["block"] is True
    assert res["field_stability_index"] < 0.5
    
    # Blocked by scale penalty
    res = l3.reflect({"answer_draft": "always except " * 10})
    assert res["block"] is True
    
    # Stable field
    res = l3.reflect({"answer_draft": "Stable local strategy.", "retrieved_sources": ["s1"]})
    assert res["block"] is False
    assert res["field_stability_index"] >= 0.9 # Base 1.0 + cluster bonus 0.1 - small penalty?
