import pytest

from analyzer.Analysis.Basic import BasicAnalysis
from analyzer.Builds import Build
from analyzer.config import TRAVIS_CI, GH_ACTIONS, CIRCLE_CI


@pytest.fixture
def analyzer():
    build_examples = [
        Build(
            state='success',
            id=1,
            number=1,
            duration=4,
            created_by='Freek',
            event_type='push',
            branch='main',
            used_tool=TRAVIS_CI
        ),
        Build(
            state='passed',
            id=1,
            number=1,
            duration=4,
            created_by='Freek',
            event_type='pull_request',
            branch='main',
            used_tool=TRAVIS_CI
        ),
        Build(
            state='failure',
            id=2,
            number=2,
            duration=10,
            created_by='Freek',
            event_type='push',
            branch='main',
            used_tool=GH_ACTIONS
        ),

    ]
    return BasicAnalysis(build_examples)


def test_constructor():
    b = BasicAnalysis([])
    assert b.name == 'basic'
    assert len(b.builds) == 0

    b2 = BasicAnalysis([Build()])
    assert b2.name == 'basic'
    assert len(b2.builds) == 1


def test_get_builds_from_tool(analyzer):
    t_builds = analyzer._get_builds_from_tool(TRAVIS_CI)
    assert len(t_builds) == 2
    gh_builds = analyzer._get_builds_from_tool(GH_ACTIONS)
    assert len(gh_builds) == 1
    c_builds = analyzer._get_builds_from_tool(CIRCLE_CI)
    assert len(c_builds) == 0


def test_filter_state(analyzer):
    positive_builds = analyzer._filter_state(['success', 'passed'])
    assert len(positive_builds) == 2
    negative_builds = analyzer._filter_state(['failed', 'failure'])
    assert len(negative_builds) == 1

    unknown_types = analyzer._filter_state(['blabla'])
    assert len(unknown_types) == 0

    empty_types = analyzer._filter_state([])
    assert len(empty_types) == 0


def test_get_failing_builds(analyzer):
    failing = analyzer.get_failing_builds()
    assert len(failing) == 1
    failing_t = analyzer.get_failing_builds(TRAVIS_CI)
    assert len(failing_t) == 1
    failing_gh = analyzer.get_failing_builds(GH_ACTIONS)
    assert len(failing_gh) == 0
    failing_c = analyzer.get_failing_builds(CIRCLE_CI)
    assert len(failing_c) == 0


def test_get_success_builds(analyzer):
    success = analyzer.get_success_builds()
    assert len(success) == 2
    success_t = analyzer.get_success_builds(TRAVIS_CI)
    assert len(success_t) == 2
    success_gh = analyzer.get_success_builds(GH_ACTIONS)
    assert len(success_gh) == 0
    success_c = analyzer.get_success_builds(CIRCLE_CI)
    assert len(success_c) == 0


def test_get_avg_duration(analyzer):
    pass


def test_get_builds_triggered_by(analyzer):
    pass


def test_execute(analyzer):
    pass
