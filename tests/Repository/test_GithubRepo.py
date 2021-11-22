import os
from analyzer.Repository.GithubRepo import GithubRepo
from dotenv import load_dotenv


def test_constructor():
    load_dotenv()
    GithubRepo.init_github_token(os.getenv('GH_TOKEN'))
    r = GithubRepo("FreekDS/git-ci-analyzer")

    assert r._fetched is False
    assert r._repo is not None
    assert r._githubObject is not None
