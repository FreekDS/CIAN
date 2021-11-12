from analyzer.Repository.TestRepo import TestRepo
from analyzer.CIDetector.TravisDetector import TravisDetector, TRAVIS_CI
from dotenv import load_dotenv


def test_constructor():
    load_dotenv()
    detector = TravisDetector()

    auth_header = 'Authorization'
    api_version_header = 'Travis-API-Version'
    user_agent_header = 'User-Agent'

    headers = [auth_header, api_version_header, user_agent_header]

    for h in headers:
        assert h in detector.headers.keys()
        assert detector.headers.get(h) is not None


def test_execute_happyday():
    load_dotenv()
    repo = TestRepo('FreekDS/git-ci-analyzer')
    detector = TravisDetector()

    res = detector.execute(repo)
    assert res is not None
    assert res == TRAVIS_CI


def test_execute_non_existing_repo():
    load_dotenv()
    repo = TestRepo('doesnt-exist/repository')
    detector = TravisDetector()
    res = detector.execute(repo)
    assert res != TRAVIS_CI
    assert res is None


def test_execute_travis_inactive():
    load_dotenv()
    repo = TestRepo('FreekDS/MSI-Mystic-Light-Controller', repo_type='github')
    detector = TravisDetector()
    res = detector.execute(repo)
    assert res != TRAVIS_CI
    assert res is None
