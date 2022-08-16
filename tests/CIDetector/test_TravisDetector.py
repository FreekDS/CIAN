from analyzer.Repository.TestRepo import TestRepo
from analyzer.CIDetector.TravisDetector import TravisDetector, TRAVIS_CI


def test_execute_happyday():
    repo = TestRepo('FreekDS/CIAN')
    detector = TravisDetector()

    res = detector.execute(repo)
    assert res is not None
    assert res == TRAVIS_CI


def test_execute_non_existing_repo():
    repo = TestRepo('doesnt-exist/repository')
    detector = TravisDetector()
    res = detector.execute(repo)
    assert res != TRAVIS_CI
    assert res is None


def test_execute_travis_inactive():
    repo = TestRepo('FreekDS/MSI-Mystic-Light-Controller', repo_type='github')
    detector = TravisDetector()
    res = detector.execute(repo)
    assert res != TRAVIS_CI
    assert res is None
