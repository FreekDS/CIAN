import os
import pytest
from analyzer.Repository.GithubRepo import GithubRepo
from dotenv import load_dotenv


@pytest.fixture(scope='module')
def default_repo():
    load_dotenv()
    GithubRepo.init_github_token(os.getenv('GH_TOKEN'))
    return GithubRepo("FreekDS/git-ci-analyzer")


def test_constructor(default_repo):
    assert default_repo._fetched is False
    assert default_repo._repo is not None
    assert default_repo._githubObject is not None


def test_path_exists(default_repo):
    assert default_repo.path_exists('.circleci')
    assert default_repo.path_exists('.circleci/')
    assert default_repo.path_exists('.circleci/config.yml')
    assert not default_repo.path_exists('does/not/exist.txt')
    assert not default_repo.path_exists('does/not/exist/')


def test_dir_empty(default_repo):
    assert not default_repo.dir_empty('.circleci')
    assert not default_repo.dir_empty('.circleci/')
    assert not default_repo.dir_empty('does/not/exist/')
    assert not default_repo.dir_empty('does/not/exist')
    # Note: there are no empty directories on GitHub
