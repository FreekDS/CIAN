# from analyzer.Repository.TestRepo import TestRepo
from analyzer.Repository.GithubRepo import GithubRepo
from analyzer.CIDetector.GithubActionsDectector import GH_ACTIONS, GithubActionsDetector


def test_execute_happyday():
    repo = GithubRepo('FreekDS/git-ci-analyzer')
    detector = GithubActionsDetector()
    res = detector.execute(repo)
    assert res is not None
    assert res == GH_ACTIONS

# TODO add tests when TestRepo is separated from GithubRepo
