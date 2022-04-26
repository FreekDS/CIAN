from analyzer.AntiPatterns.LateMerging import LATE_MERGING, LateMerging


def test_constructor():
    lm = LateMerging([], {})
    assert lm.builds == {}
    assert lm.name == LATE_MERGING
    assert lm.branch_info == {}
