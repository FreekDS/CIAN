import re
from analyzer.utils.TestResultCommand import TestResultCommand


class QUnitResults(TestResultCommand):

    def get_summary(self):
        matches = re.findall(r">> \d+ tests completed with \d+ failed, \d+ skipped, and \d+ todo", self.log)
        if matches:
            return matches[0]
        return str()

    def _get_tests_of_type(self, ttype):
        if not self.detect():
            return 0
        s = self.get_summary()
        match = re.findall(r"\d+ " + ttype, s)
        if match:
            return int(match[0].split(' ')[0])
        return 0

    def get_test_count(self) -> int:
        return self._get_tests_of_type('tests')

    def get_failed_test_count(self) -> int:
        return self._get_tests_of_type('failed')

    def get_successful_test_count(self) -> int:
        todo = self._get_tests_of_type('todo')
        return self.get_test_count() - self.get_failed_test_count() - self.get_skipped_test_count() - todo

    def get_skipped_test_count(self) -> int:
        return self._get_tests_of_type('skipped')

    def get_test_framework(self) -> str:
        return "qunit"

    def detect(self) -> bool:
        match1 = len(re.findall("qunit", self.log)) > 0
        match2 = len(re.findall(r">> \d+ tests completed", self.log)) > 0
        return match1 and match2
