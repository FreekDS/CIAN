import re
from analyzer.utils.TestResultCommand import TestResultCommand


class CTestResults(TestResultCommand):
    # Repo to test: NCAR/ParallelIO

    def _get_summary(self):
        summary = re.findall(r'\d+% tests passed.*\n', self.log)
        if summary:
            return summary[0]
        else:
            return str()

    def total_count(self):
        s = self._get_summary()
        matches = re.findall(r'\d+ tests failed out of \d+', s)
        if matches:
            i = matches[0].split(' ')[-1].strip()
            try:
                return int(i)
            except ValueError:
                return 0
        return 0

    def get_test_of_type(self, t_type):
        s = self._get_summary()
        s = s.split(',')[1:-1]
        for test_type in s:
            if t_type in test_type:
                i = test_type.split(' ')[0]
                try:
                    return int(i)
                except ValueError:
                    return 0
        return 0

    def get_failed_test_count(self) -> int:
        return self.get_test_of_type('failed')

    def get_successful_test_count(self) -> int:
        return max(self.get_test_count() - self.get_failed_test_count() - self.get_skipped_test_count(), 0)

    def get_skipped_test_count(self) -> int:
        return self.get_test_of_type('skipped')

    def get_test_framework(self) -> str:
        return 'ctest'

    def detect(self) -> bool:
        found_cmd = re.findall('ctest', self.log)
        found_constructing_msg = re.findall('Constructing a list of tests', self.log)
        return len(found_cmd) > 0 and len(found_constructing_msg) > 0
