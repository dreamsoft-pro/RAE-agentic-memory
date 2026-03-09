from uuid import uuid4

from rae_core.math.fusion import RRFFusion


def test_rrf_basic():
    id1, id2, id3 = uuid4(), uuid4(), uuid4()
    list1 = [(id1, 0.9, 0.0), (id2, 0.8, 0.0)]
    list2 = [(id2, 0.9, 0.0), (id3, 0.7, 0.0)]

    fusion = RRFFusion()
    strategy_results = {"s1": list1, "s2": list2}

    fused = fusion.fuse(strategy_results)

    assert len(fused) == 3
    # id2 is in both, so it should be first
    assert fused[0][0] == id2
