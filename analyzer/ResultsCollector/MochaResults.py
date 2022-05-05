import re
from analyzer.utils.TestResultCommand import TestResultCommand


class MochaResults(TestResultCommand):

    def _get_tests_of_type(self, ttype):
        if not self.detect():
            return 0
        matches = re.findall(r'\d+ ' + ttype, self.log)
        if matches:
            return int(matches[0].split(' ')[0])
        return 0

    def get_failed_test_count(self) -> int:
        return self._get_tests_of_type('failing')

    def get_successful_test_count(self) -> int:
        return self._get_tests_of_type('passing')

    def get_skipped_test_count(self) -> int:
        return self._get_tests_of_type('skipping') + self._get_tests_of_type('skipped')

    def get_test_framework(self) -> str:
        return "mocha"

    def detect(self) -> bool:
        match1 = len(re.findall("mocha", self.log)) > 0
        match2 = len(re.findall(r"✓", self.log)) > 0
        return match1 and match2
