import re
from analyzer.utils.TestResultCommand import TestResultCommand


class GTestResults(TestResultCommand):
    # Can be tests with qmk/qmk_firmware (workflow unittest)

    def get_tests_of_type(self, test_type):
        regex = fr"[ {test_type} ] \d+ test"
        matches = re.findall(regex, self.log)
        count = 0
        for m in matches:
            c = m.split(' ')[3].strip()
            count += int(c)
        return count

    def get_failed_test_count(self) -> int:
        return self.get_tests_of_type('FAILED')

    def get_successful_test_count(self) -> int:
        return max(self.total_count() - self.get_failed_test_count() - self.get_successful_test_count(), 0)

    def get_skipped_test_count(self) -> int:
        return self.get_tests_of_type('PASSED')

    def get_test_framework(self) -> str:
        return 'GoogleTest'

    def total_count(self):
        all_test_matches = re.findall(r'Running \d+ tests from \d+ test suites.', self.log)
        count = 0
        for m in all_test_matches:
            tests_c = m.split(' ')[1]
            try:
                count += int(tests_c)
            except ValueError:
                continue
        return count

    def detect(self) -> bool:
        gtest_dependent_line = self.log.find('[----------] Global test environment set-up.')
        return gtest_dependent_line >= 0
