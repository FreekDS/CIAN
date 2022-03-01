import datetime
from typing import List
from collections import defaultdict

from analyzer.Repository.Repo import Repo
from analyzer.Builds import Build
from analyzer.utils.Command import Command
from analyzer.utils.GithubAccessor import GithubAccessor
from analyzer.ResultsCollector import collect_test_results
from analyzer.config import GH_ACTIONS


class GithubActionsCollector(Command):
    def __init__(self, repo: Repo):
        super(GithubActionsCollector, self).__init__()
        self.repo = repo
        self._gh_access = GithubAccessor()

    def execute(self, *args, **kwargs) -> List[Build]:
        if self.repo.repo_type != 'github':
            return []

        builds = list()

        runs_json = self._gh_access.get_workflow_runs(self.repo)
        workflows_json = self._gh_access.get_workflows(self.repo)
        workflows = dict()
        for wf in workflows_json.get('workflows'):
            workflows[wf.get('id')] = wf

        for run in runs_json.get('workflow_runs'):
            run_id = run.get('id')
            timing = self._gh_access.get_workflow_run_timing(self.repo, run_id)
            jobs = self._gh_access.get_jobs(self.repo, run_id)

            test_results = defaultdict(list)
            for job in jobs.get('jobs'):
                log = self._gh_access.get_job_log(self.repo, job.get('id'))
                tests = collect_test_results(log)
                if not log:
                    test_results[job.get('name')] = ["log expired"]
                else:
                    test_results[job.get('name')].append(tests)

            created_at = datetime.datetime.strptime(run.get('created_at'), '%Y-%m-%dT%H:%M:%SZ')
            ended_at = created_at + datetime.timedelta(milliseconds=timing.get('run_duration_ms', 0))

            conclusion = run.get('conclusion', None)
            state = conclusion if conclusion else run.get('status')
            if state == 'passed':
                state = 'success'
            elif state == 'failed':
                state = 'failure'

            builds.append(
                Build(
                    state=state,
                    id=run_id,
                    number=run.get('run_number'),
                    started_at=run.get('created_at'),
                    ended_at=ended_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
                    duration=timing.get('run_duration_ms', 0),
                    created_by=run.get('head_commit').get('committer').get('name'),
                    event_type=run.get('event'),
                    branch=run.get('head_branch'),
                    used_tool=GH_ACTIONS,
                    test_results=dict(test_results),
                    workflow=run.get('name')
                )
            )
        return builds
