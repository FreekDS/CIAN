import re
from analyzer.utils.TestResultCommand import TestResultCommand


class JestResults(TestResultCommand):

    def get_summary(self):
        matches = re.findall(r"Tests:\s\s\s\s\s\s\s\d+.*\n", self.log)
        return matches[0] if matches else ""

    def _get_test_of_type(self, ttype):
        s = self.get_summary()
        match = re.findall(r"\d+ " + ttype, s)
        if match:
            return int(match[0].split(' ')[0])
        return 0

    def get_failed_test_count(self) -> int:
        return self._get_test_of_type('failed')

    def get_successful_test_count(self) -> int:
        return self._get_test_of_type('passed')

    def get_skipped_test_count(self) -> int:
        return self._get_test_of_type('skipped')

    def get_test_framework(self) -> str:
        return "jest"

    def detect(self) -> bool:
        match1 = len(re.findall("jest", self.log)) > 0
        match2 = len(re.findall("Test Suites:", self.log)) > 0
        return match1 and match2
