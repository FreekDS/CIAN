from analyzer.CIDetector.CircleCIDetector import CircleCIDetector, CIRCLE_CI
from analyzer.Repository.TestRepo import TestRepo


def test_constructor():
    header = 'Circle-Token'

    detector = CircleCIDetector()

    assert header in detector.headers.keys()
    assert detector.headers.get(header) is not None


def test_execute_happyday():
    # Fill in 'github as repo type to trick detector that it is a GithubRepo object
    repo = TestRepo("FreekDS/CIAN", repo_type='github')

    detector = CircleCIDetector()

    res = detector.execute(repo)
    assert res is not None
    assert res == CIRCLE_CI


def test_execute_unknown_repo_type():
    # TestRepo has 'test' as repo_type which is not recognized by the detector
    repo = TestRepo("FreekDS/CIAN")
    detector = CircleCIDetector()
    res = detector.execute(repo)
    assert res != CIRCLE_CI
    assert res is None
