from tests.CIDetector.TestRepo import TestRepo
from analyzer.CIDetector.GithubActionsDectector import GH_ACTIONS, GithubActionsDetector
from dotenv import load_dotenv


def test_execute_happyday():
    load_dotenv()
    repo = TestRepo('FreekDS/git-ci-analyzer', 'github')
    detector = GithubActionsDetector()
    res = detector.execute(repo)
    assert res is not None
    assert res == GH_ACTIONS

# TODO add tests when TestRepo is separated from GithubRepo
