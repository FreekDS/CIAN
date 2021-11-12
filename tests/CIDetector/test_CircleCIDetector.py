from analyzer.CIDetector.CircleCIDetector import CircleCIDetector, CIRCLE_CI
from tests.CIDetector.TestRepo import TestRepo
from dotenv import load_dotenv


def test_constructor():
    load_dotenv()
    header = 'Circle-Token'

    detector = CircleCIDetector()

    assert header in detector.headers.keys()
    assert detector.headers.get(header) is not None


def test_execute_happyday():
    load_dotenv()
    repo = TestRepo("FreekDS/git-ci-analyzer", 'github')

    detector = CircleCIDetector()

    res = detector.execute(repo)
    assert res is not None
    assert res == CIRCLE_CI


def test_execute_unknown_repo_type():
    load_dotenv()
    repo = TestRepo("FreekDS/git-ci-analyzer", 'strange-type')
    detector = CircleCIDetector()
    res = detector.execute(repo)
    assert res != CIRCLE_CI
    assert res is None
