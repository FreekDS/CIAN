import pytest

from analyzer.AntiPatterns.BrokenRelease import BrokenRelease, BROKEN_RELEASE
from analyzer.Builds.Build import Build


@pytest.fixture(scope='module')
def builds():
    return [
        Build(branch='main', state='failure', workflow="wf1"),
        Build(branch='main', state='cool', workflow="wf1"),
        Build(branch='main', state='unknown', workflow="wf1"),
        Build(branch='master', state='failure', workflow="wf1"),
        Build(branch='other_branch', state='failure', workflow="wf1"),

        Build(branch='main', state='failure', workflow="wf2"),
        Build(branch='main', state='success', workflow="wf2"),
        Build(branch='main', state='failure', workflow="wf2"),
        Build(branch='master', state='failure', workflow="wf2"),
        Build(branch='other_branch', state='failure', workflow="wf2"),
        Build(branch='other_branch', state='failure', workflow="wf2"),
        Build(branch='other_branch2', state='failure', workflow="wf2")
    ]


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


def test_failing_builds():
    wf1 = "wf1"
    wf2 = "wf2"
    wf3 = "wf3"
    builds = {
        wf1: [
            Build(state='failure', workflow=wf1),
            Build(state='failure', workflow=wf1),
            Build(state='success', workflow=wf1),
            Build(state='failur', workflow=wf1),
            Build(state='failure', workflow=wf1),
            Build(state='error', workflow=wf1),
            Build(workflow=wf1),
            Build(state='failure', workflow=wf1)
        ],
        wf2: [
            Build(state='failure', workflow=wf2),
            Build(state='failure', workflow=wf2),
        ],
        wf3: [
            Build(workflow=wf3),
            Build(workflow=wf3),
            Build(workflow=wf3)
        ]
    }

    s = BrokenRelease.get_failing(builds)

    assert len(s[wf1]) == 4
    assert len(s[wf2]) == 2
    assert len(s[wf3]) == 0


def test_get_release_builds(builds):
    wf1 = "wf1"
    wf2 = "wf2"

    br = BrokenRelease(builds)
    bs = br.get_release_branch_builds()

    assert len(bs[wf1]) == 4
    assert len(bs[wf2]) == 4

    br = BrokenRelease(builds, default_branch='other_branch')
    bs = br.get_release_branch_builds()

    assert len(bs[wf1]) == 5
    assert len(bs[wf2]) == 6


def test_detect(builds):
    br = BrokenRelease(builds)
    d = br.detect()

    assert len(d.items()) == 2
    assert len(d['wf1'].get('data', [])) == 2
    assert len(d['wf2'].get('data', [])) == 3
