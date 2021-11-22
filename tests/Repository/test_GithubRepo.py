import os
from analyzer.Repository.GithubRepo import GithubRepo
from dotenv import load_dotenv

# TODO factor out loading of the github token


def test_constructor():
    load_dotenv()
    GithubRepo.init_github_token(os.getenv('GH_TOKEN'))
    r = GithubRepo("FreekDS/git-ci-analyzer")

    assert r._fetched is False
    assert r._repo is not None
    assert r._githubObject is not None


def test_path_exists():
    load_dotenv()
    GithubRepo.init_github_token(os.getenv('GH_TOKEN'))
    r = GithubRepo("FreekDS/git-ci-analyzer")

    assert r.path_exists('.circleci')
    assert r.path_exists('.circleci/')
    assert r.path_exists('.circleci/config.yml')
    assert not r.path_exists('does/not/exist.txt')
    assert not r.path_exists('does/not/exist/')
