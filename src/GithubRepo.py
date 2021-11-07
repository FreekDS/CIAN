import os

from typing import List

from github import Github, Repository, UnknownObjectException
from dotenv import load_dotenv
from CIDetector import detect_ci_tools


class CIWorkflowRun:
    def __init__(self, id, event, run_number, url, conclusion, jobs_url, artifacts_url):
        self.id = id
        self.run_number = run_number
        self.event = event
        self.url = url
        self.conclusion = conclusion
        self.jobs_url = jobs_url
        self.artifacts_url = artifacts_url

    def __repr__(self):
        return f"CIWorkflowRun(\n\t" \
               f"{self.id}\n\t" \
               f"{self.event}\n\t" \
               f"{self.conclusion}\n\t" \
               f"{self.jobs_url}"


class CIWorkflow:
    def __init__(self, name, id, state, created_at, url, runs):
        self.name: str = name
        self.id = id
        self.state = state
        self.created_at = created_at
        self.url = url
        self.runs = runs

    def __repr__(self):
        return f"CIWorkflow(\n\t" \
               f"{self.name}\n\t" \
               f"{self.url}\n\t" \
               f"Runs: {len(self.runs)}\n" \
               f")"


class GithubRepo:
    _githubObject = Github()

    @staticmethod
    def init_github_token(token):
        GithubRepo._githubObject = Github(login_or_token=token)

    def __init__(self, path):
        self._repo: Repository = self._githubObject.get_repo(path)
        self.workflows: List[CIWorkflow] = []
        self.workflow_runs = list()
        self.path = path
        self.repo_type = "github"
        self._fetched = False

    def fetch_builtin_ci_workflows(self):
        if self._fetched:
            return

        gh_workflows = self._repo.get_workflows()

        for wf in gh_workflows:
            gh_wf_runs = wf.get_runs()
            runs = []
            for wf_run in gh_wf_runs:
                new_wf_run = CIWorkflowRun(
                    wf_run.id,
                    wf_run.event,
                    wf_run.run_number,
                    wf_run.url,
                    wf_run.conclusion,
                    wf_run.jobs_url,
                    wf_run.artifacts_url
                )
                runs.append(new_wf_run)

            new_wf = CIWorkflow(
                wf.name,
                wf.id,
                wf.state,
                wf.created_at,
                wf.url,
                runs
            )
            self.workflows.append(new_wf)
        self._fetched = True

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

    def dir_empty(self, path):
        if path.endswith('/'):
            path = path[:-1]
        assert self.path_exists(path), "Directory path does not exist"
        try:
            content = self._repo.get_contents(path)
            while content:
                file_content = content.pop(0)
                if file_content.type == 'file':
                    return False
                print(file_content.type)
            return True
        except UnknownObjectException:
            pass


if __name__ == '__main__':
    load_dotenv()
    GithubRepo.init_github_token(os.getenv("GITHUB_TOKEN"))

    this = GithubRepo("FreekDS/git-ci-analyzer")
    this.fetch_builtin_ci_workflows()
    print("Detected tools in this repo:", detect_ci_tools(this))

    python_ci_testing = GithubRepo("FreekDS/python-ci-testing")
    python_ci_testing.fetch_builtin_ci_workflows()
    print("Detected tools:", detect_ci_tools(python_ci_testing))

    for wf in python_ci_testing.workflows:
        print(wf)
        for wf_run in wf.runs:
            print(wf_run)
        print("============\n")
