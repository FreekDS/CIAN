from Builds import Build
from analyzer.BuildCollector.GithubActionsCollector import GithubActionsCollector
from analyzer.Repository.TestRepo import TestRepo


def test_execute_gh_actions_collector():
    repo1 = TestRepo('some_user/some_repository')
    repo2 = TestRepo('some_user/some_other_repository', repo_type='github')

    remote_builds = [
        Build(
            state='success',
            id=1,
            number=5,
            duration=70,
            created_by='some_user',
            event_type='push',
            branch='main',
            used_tool='GitHub Actions'
        ),
        Build(
            state='failure',
            id=2,
            number=6,
            duration=50,
            created_by='some_other_user',
            event_type='push',
            branch='some_branch',
            used_tool='GitHub Actions'
        )
    ]

    repo1.set_remote_builds(remote_builds)
    repo2.set_remote_builds(remote_builds)
    collector = GithubActionsCollector(repo1)

    # type is not 'github'
    assert len(collector.execute()) == 0

    collector = GithubActionsCollector(repo2)
    collected = collector.execute()
    assert collected == remote_builds
