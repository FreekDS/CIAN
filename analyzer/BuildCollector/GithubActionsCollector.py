import datetime
from typing import List
from collections import defaultdict

from analyzer.Repository.Repo import Repo
from analyzer.Builds import Build
from analyzer.utils.Command import Command
from analyzer.utils import format_date, timing
from analyzer.utils.GithubAccessor import GithubAccessor
from analyzer.ResultsCollector import collect_test_results
from analyzer.config import GH_ACTIONS


class GithubActionsCollector(Command):
    def __init__(self, repo: Repo, from_date=None):
        super(GithubActionsCollector, self).__init__()
        self.repo = repo
        self._gh_access = GithubAccessor()

        self.from_date = from_date

    @staticmethod
    def calculate_timing(workflow_runs):
        timings = list()
        for run in workflow_runs:
            start = format_date(run.get('created_at'))
            if not run.get('ended_at', None):
                end = format_date(run.get('updated_at'))
            else:
                end = format_date(run.get('ended_at'))

            timings.append((end - start).seconds * 1000)
        return timings

    @timing
    def execute(self, *args, **kwargs) -> List[Build]:
        if self.repo.repo_type != 'github':
            return []

        builds = list()

        if self.from_date:
            start_from = format_date(self.from_date)
        else:
            start_from = datetime.datetime.now() - datetime.timedelta(days=90)  # only last three months
        start_from = start_from.strftime("%Y-%m-%d")

        runs_json = self._gh_access.get_workflow_runs(self.repo, start_date=start_from)
        # print(f"Fetched {len(runs_json)} runs")
        workflows_json = self._gh_access.get_workflows(self.repo)
        # print(f"Fetched {len(workflows_json)} workflows")
        workflows = dict()

        run_ids = [int(run.get('id')) for run in runs_json.get('workflow_runs')]

        all_jobs_data = self._gh_access.batch_collect_jobs(self.repo, run_ids)
        # print(f"Fetched {len(all_jobs_data)} job data objects")
        # all_timings_data = self._gh_access.batch_collect_run_timing(self.repo, run_ids)
        all_timings_data = self.calculate_timing(runs_json.get('workflow_runs'))
        # print(f"Fetched {len(all_timings_data)} timing objects")

        job_ids = list()
        for i, run in enumerate(runs_json.get('workflow_runs')):
            date = format_date(run.get('created_at'))
            days_passed = (datetime.date.today() - date.date()).days
            if days_passed > 90:
                continue
            jobs = all_jobs_data[i]
            for job in jobs.get('jobs', []):
                if 'test' in job.get('name', '').lower():
                    job_ids.append(job.get('id'))

        # print(f"There are {len(job_ids)} job ids to check")
        all_job_logs = self._gh_access.batch_collect_job_logs(self.repo, job_ids)
        # print(f"Fetched {len(all_job_logs)} job logs")

        for wf in workflows_json.get('workflows'):
            workflows[wf.get('id')] = wf

        for i, run in enumerate(runs_json.get('workflow_runs')):
            run_id = run.get('id')

            timing_data = all_timings_data[i]
            jobs = all_jobs_data[i]

            test_results = defaultdict(list)
            for job in jobs.get('jobs', []):
                log = all_job_logs.get(job.get('id'), '')
                tests = collect_test_results(log)
                if not log:
                    test_results[job.get('name')] = ["log expired"]
                else:
                    test_results[job.get('name')].append(tests)

            created_at = datetime.datetime.strptime(run.get('created_at'), '%Y-%m-%dT%H:%M:%SZ')
            ended_at = created_at + datetime.timedelta(milliseconds=timing_data)

            conclusion = run.get('conclusion', None)
            state = conclusion if conclusion else run.get('status')
            if state == 'passed':
                state = 'success'
            elif state == 'failed':
                state = 'failure'

            head_commit = run.get('head_commit')
            chain_broken = False
            name = ''
            if not head_commit:
                chain_broken = True
                name = ''

            committer = None
            if not chain_broken:
                committer = head_commit.get('committer')
                if not committer:
                    name = ''
                    chain_broken = True

            if not chain_broken and committer:
                name = committer.get('name')
                if not name:
                    name = ''

            builds.append(
                Build(
                    state=state,
                    id=run_id,
                    number=run.get('run_number'),
                    started_at=run.get('created_at'),
                    ended_at=ended_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
                    duration=timing_data,
                    created_by=name,
                    event_type=run.get('event'),
                    branch=run.get('head_branch'),
                    used_tool=GH_ACTIONS,
                    test_results=dict(test_results),
                    workflow=run.get('name')
                )
            )
        return builds
