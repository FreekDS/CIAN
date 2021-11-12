from analyzer.GithubRepo import GithubRepo


class TestRepo(GithubRepo):
    # TODO change to generic repo object
    def __init__(self, path, repo_type):
        super().__init__(path)
        self.repo_type = repo_type

    def fetch_builtin_ci_workflows(self):
        super().fetch_builtin_ci_workflows()

    def path_exists(self, path) -> bool:
        return super().path_exists(path)

    def dir_empty(self, path):
        return super().dir_empty(path)