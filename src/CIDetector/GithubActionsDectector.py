from utils.Command import Command
from config import GH_ACTIONS


class GithubActionsDetector(Command):
    def execute(self, repo):
        if repo.repo_type == "github":
            repo.fetch_builtin_ci_workflows()
            if repo.path_exists('.github/workflows'):
                if not repo.dir_empty('.github/workflows') and repo.workflows:
                    return GH_ACTIONS
        return None
