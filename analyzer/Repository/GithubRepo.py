import datetime

from github import Github, UnknownObjectException
from github import Repository as GH_Repository
from analyzer.Repository.Repo import Repo
from analyzer.Builds import Build
from analyzer.config import GH_ACTIONS


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

            for wf_run in gh_wf_runs:

                # TODO: workaround to fix issue with TimingData object in CI pipeline
                # locally, no attribute error is raised. May be problem with PyGithub package on Ubuntu environment
                try:
                    timing = wf_run.timing()
                    run_duration_ms = timing.run_duration_ms
                except AttributeError as ae:
                    print(ae)
                    run_duration_ms = 0

                ended_at = wf_run.created_at + datetime.timedelta(milliseconds=run_duration_ms)

                state = wf_run.conclusion if wf_run.conclusion else wf_run.status

                # translate to match allowed values for state
                if state == 'passed':
                    state = 'success'
                elif state == 'failed':
                    state = 'failure'

                build = Build(
                    state=state,
                    id=wf_run.id,
                    number=wf_run.run_number,
                    started_at=wf_run.created_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
                    ended_at=ended_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
                    duration=run_duration_ms / 1000,
                    created_by=wf_run.head_commit.committer.name,
                    event_type=wf_run.event,
                    branch=wf_run.head_branch,
                    used_tool=GH_ACTIONS
                )
                self.builds.append(build)

        self._fetched = True
