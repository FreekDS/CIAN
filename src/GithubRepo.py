from typing import List

from github import Github, Repository


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

    def fetch_builtin_ci_workflows(self):
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


if __name__ == '__main__':
    GithubRepo.init_github_token("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")

    python_ci_testing = GithubRepo("FreekDS/python-ci-testing")
    python_ci_testing.fetch_builtin_ci_workflows()

    for wf in python_ci_testing.workflows:
        print(wf)
        for wf_run in wf.runs:
            print(wf_run)
        print("============\n")
