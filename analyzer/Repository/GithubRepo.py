from github import Github, UnknownObjectException
from github import Repository as GH_Repository
from analyzer.Repository.Repo import Repo
from analyzer.Workflow import WorkflowRun, Workflow


class GithubRepo(Repo):
    _githubObject = Github()

    @staticmethod
    def init_github_token(token):
        GithubRepo._githubObject = Github(login_or_token=token)

    def __init__(self, path):
        super().__init__(path, repo_type='github')
        self._fetched = False
        self._repo: GH_Repository = self._githubObject.get_repo(path)

    def path_exists(self, path) -> bool:
        if path.endswith('/'):
            path = path[:-1]
        try:
            content = self._repo.get_contents(path)
            if content:
                return True
        except UnknownObjectException as ex:
            if ex.status == 404:
                return False
            else:
                raise ex

    def dir_empty(self, path) -> bool:
        if path.endswith('/'):
            path = path[:-1]
        if not self.path_exists(path):
            return False
        try:
            content = self._repo.get_contents(path)
            while content:
                file_content = content.pop(0)
                if file_content.type == 'file':
                    return False
            return True
        except UnknownObjectException:
            return False

    def fetch_builtin_ci(self):
        if self._fetched:
            return

        gh_workflows = self._repo.get_workflows()

        for wf in gh_workflows:
            gh_wf_runs = wf.get_runs()
            runs = []
            for wf_run in gh_wf_runs:
                new_wf_run = WorkflowRun(
                    wf_run.id,
                    wf_run.event,
                    wf_run.run_number,
                    wf_run.url,
                    wf_run.conclusion,
                    wf_run.jobs_url,
                    wf_run.artifacts_url
                )
                runs.append(new_wf_run)

            new_wf = Workflow(
                wf.name,
                wf.id,
                wf.state,
                wf.created_at,
                wf.url,
                runs
            )
            self.workflows.append(new_wf)
        self._fetched = True
