import pytest
from analyzer.Repository.GithubRepo import GithubRepo


@pytest.fixture(scope='module')
def default_repo():
    return GithubRepo("FreekDS/CIAN")


def test_constructor(default_repo):
    assert default_repo._base_url == 'https://api.github.com'
    assert default_repo._gh_access is not None


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
