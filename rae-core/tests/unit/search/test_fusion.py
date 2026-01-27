"""Unit tests for search fusion strategies."""

from uuid import uuid4

from rae_core.search.fusion import ConfidenceWeightedFusion


def test_confidence_analysis():
    fusion = ConfidenceWeightedFusion()
    m1, m2 = uuid4(), uuid4()

    # 1. High confidence (clear gap)
    results = [(m1, 0.9), (m2, 0.2)]
    conf = fusion._analyze_confidence(results)
    assert conf > 0.5

    # 2. Low confidence (no gap)
    results = [(m1, 0.5), (m2, 0.49)]
    conf = fusion._analyze_confidence(results)
    assert conf < 0.2


def test_weighted_fusion_logic():
    fusion = ConfidenceWeightedFusion()
    m1, m2 = uuid4(), uuid4()

    # Vector found m1 with high confidence
    # Text found m2 with high confidence
    strategy_results = {
        "vector": [(m1, 0.95), (m2, 0.1)],
        "fulltext": [(m2, 0.99), (m1, 0.05)],
    }
    weights = {"vector": 1.0, "fulltext": 1.0}

    fused = fusion.fuse(strategy_results, weights)
    assert len(fused) == 2
    # Liderzy z obu powinni być na szczycie
    assert fused[0][1] > 0.5
