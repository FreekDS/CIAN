from analyzer.BuildCollector.TravisCollector import TravisCollector
from analyzer.Repository.TestRepo import TestRepo


def test_execute_traviscollector_happyday():
    repo = TestRepo('FreekDS/git-ci-analyzer')
    collector = TravisCollector(repo)
    builds = collector.execute()
    assert len(builds) > 0
    for build in builds:
        assert build.used_tool == 'TravisCI'
        assert isinstance(build.branch, str)
        assert isinstance(build.created_by, str)
        assert build.branch != ""
        assert build.created_by != ""


def test_execute_traviscollector_unexisting_repo():
    repo = TestRepo('doesnt/exist')
    collector = TravisCollector(repo)
    assert len(collector.execute()) == 0
