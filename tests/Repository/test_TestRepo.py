from analyzer.Builds import Build
from analyzer.Repository.TestRepo import TestRepo


def test_constructor():
    empty_dirs = [
        "directory/",
        "path/to/directory/"
    ]

    existing_paths = [
        "path/to/file",
        "path/to/other/file"
    ]

    other_repo_type = 'other'

    path = "username/repository"
    repo1 = TestRepo(path)

    assert repo1.path == path
    assert repo1.repo_type == 'test'
    assert len(repo1.empty_dirs) == 0
    assert len(repo1.existing_paths) == 0

    repo2 = TestRepo(path, existing_paths=existing_paths, empty_dirs=empty_dirs, repo_type=other_repo_type)
    assert repo2.path == path
    assert repo2.repo_type == other_repo_type
    assert repo2.existing_paths == existing_paths + empty_dirs
    assert repo2.empty_dirs == empty_dirs


def test_path_exists():
    existing_paths = [
        "path/to/file",
        "path/to/other/file"
    ]

    path = "username/repository"

    repo = TestRepo(path, existing_paths=existing_paths)
    for path in existing_paths:
        assert repo.path_exists(path)

    assert not repo.path_exists('unexisting/path')


def test_dir_empty():
    empty_dirs = [
        "directory/",
        "path/to/directory/"
    ]

    existing_paths = [
        "non-empty/dir"
    ]

    path = "username/repository"

    repo = TestRepo(path, empty_dirs=empty_dirs, existing_paths=existing_paths)

    for path in empty_dirs:
        assert repo.dir_empty(path)

    for path in existing_paths:
        assert not repo.dir_empty(path)


def test_fetch_builtin_ci():
    repo = TestRepo("username/repository")
    r_builds = [
        Build(
            state='passed',
            branch='main'
        ),
        Build(
            state='failed',
            branch='some_branch'
        )
    ]
    repo.set_remote_builds(r_builds)

    assert repo._remote_builds == r_builds
    assert len(repo.builds) == 0

    repo.fetch_builtin_ci()

    assert len(repo.builds) == len(r_builds)
    assert repo.builds == r_builds
