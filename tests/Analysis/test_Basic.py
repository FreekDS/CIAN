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
            state='success',
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
    return build_examples


def test_constructor():
    b = BasicAnalysis([])
    assert b.name == 'basic'
    assert len(b.builds) == 0

    b2 = BasicAnalysis([Build()])
    assert b2.name == 'basic'
    assert len(b2.builds) == 1


def test_get_builds_from_tool(analyzer):
    pass


def test_filter_state(analyzer):
    pass


def test_get_failing_builds(analyzer):
    pass


def test_get_success_builds(analyzer):
    pass


def test_get_avg_duration(analyzer):
    pass


def test_get_builds_triggered_by(analyzer):
    pass


def test_execute(analyzer):
    pass
