from typing import List
from collections import defaultdict

from analyzer.Builds.Build import Build
from analyzer.AntiPatterns.AntiPattern import AntiPattern
from analyzer.config import SKIP_FAILING_TESTS


class SkipFailingTests(AntiPattern):

    def __init__(self, builds: List[Build]):
        super().__init__(builds, SKIP_FAILING_TESTS)
        self.builds = self.sort_by_number()

    @staticmethod
    def _delta(results1, results2, what):
        return int(results2.get(what)) - int(results1.get(what))

    def delta_runs(self, results1, results2):
        return self._delta(results1, results2, 'test_count')

    def delta_breaks(self, results1, results2):
        return self._delta(results1, results2, 'failed_count')

    def delta_skipped(self, results1, results2):
        return self._delta(results1, results2, 'skipped_count')

    def build_has_skipped(self, prev_build: Build, build: Build):

        results = {}

        if not build.test_results:
            return False

        same_job_count = len(prev_build.test_results.items()) == len(build.test_results.items())
        build_has_tests = len(list(build.test_results.values())[0]) > 0

        if not same_job_count or not build_has_tests:
            return False

        for i, (job_name, test_results) in enumerate(build.test_results.items()):
            for j, test_result in enumerate(test_results):
                try:
                    if test_result == 'log expired':
                        continue
                    test_result = test_result[0]
                    framework = test_result.get('framework')

                    # i: position of current (job, results) pair
                    # .values() gives the list of test frameworks
                    # j: current test framework results
                    prev_test_result = list(prev_build.test_results.values())[i][j]
                    if prev_test_result == 'log expired':
                        continue
                    prev_test_result = prev_test_result[0]

                    # should be true by know I think
                    # assert (framework == prev_test_result.get('framework'))
                    # not always true (eg when updating framework)

                    delta_run = self.delta_runs(prev_test_result, test_result)
                    delta_break = self.delta_breaks(prev_test_result, test_result)
                    delta_skip = self.delta_skipped(prev_test_result, test_result)

                    skipped = delta_break < 0 and (delta_run < 0 or delta_skip > 0)

                    if skipped:
                        if job_name not in results.keys():
                            results[job_name] = {}
                        results[job_name][framework] = {
                            'delta_breaks': delta_break,
                            'delta_skip': delta_skip,
                            'delta_run': delta_run,
                            'skipped': skipped
                        }

                except IndexError:
                    # print("IE", IE, "continuing...")
                    continue

        return results

    def detect(self) -> dict:
        """
        Detect whether skip failing tests anti pattern arises
        :return: dict with following format:
        {
            'workflow': [
                {
                    'build_number': int,
                    'build_date': date_str,
                    'job name': {
                        'test framework': {
                            'delta_break': int,
                            'delta_skip': int,
                            'delta_run': int,
                            'skipped': bool
                        }
                    },
                    'used_tool': str
                }
            ]
        }
        """
        result = defaultdict(list)

        for wf, builds in self.builds.items():
            for i, build in enumerate(builds[1:]):
                prev_build = builds[i - 1]
                detect_result = self.build_has_skipped(prev_build, build)
                if detect_result:
                    d = {
                        'build_number': build.number,
                        'build_date': build.started_at,
                        'used_tool': build.used_tool,
                        'build_id': build.id,
                        'prev_build_id': prev_build.id
                    }
                    d.update(
                        detect_result
                    )
                    result[wf].append(d)
        return dict(result)
