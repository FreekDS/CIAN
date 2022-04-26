from analyzer.AntiPatterns.BrokenRelease import BrokenRelease, BROKEN_RELEASE


def test_constructor():
    br = BrokenRelease([])
    assert br.name == BROKEN_RELEASE
    assert br.builds == {}
    assert br.custom_branches == []

    br = BrokenRelease([], custom_release_branches=["b1", "b2"])
    assert br.custom_branches == ["b1", "b2"]

    br = BrokenRelease([], default_branch="b1")
    assert br.custom_branches == ["b1"]

    br = BrokenRelease([], custom_release_branches=["b1", "b2"], default_branch="b0")
    assert br.custom_branches == ["b1", "b2", "b0"]
