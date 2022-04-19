import re
from analyzer.utils.TestResultCommand import TestResultCommand


class JUnitResults(TestResultCommand):
    # Repo to test opentripplanner/OpenTripPlanner

    def get_summary(self):
        matches = re.findall(r'Tests run: \d+, Failures: \d+, Errors: \d+, Skipped: \d+', self.log)
        return matches[-1] if matches else str()

    def get_failed_test_count(self) -> int:
        s = self.get_summary()
        count = 0
        failure_matches = re.findall(r'Failures: \d+', s)
        error_matches = re.findall(r'Errors: \d+', s)

        if failure_matches:
            try:
                count += int(failure_matches[0].split(' ')[-1])
            except ValueError:
                pass
        if error_matches:
            try:
                count += int(error_matches[0].split(' ')[-1])
            except ValueError:
                pass
        return count

    def total_test_count(self):
        s = self.get_summary()
        total_matches = re.findall(r'Tests run: \d+', s)
        if total_matches:
            try:
                return int(total_matches[0].split(' ')[-1])
            except ValueError:
                return 0
        return 0

    def get_successful_test_count(self) -> int:
        return max(self.total_test_count() - self.get_failed_test_count() - self.get_skipped_test_count(), 0)

    def get_skipped_test_count(self) -> int:
        s = self.get_summary()
        skipped_matches = re.findall(r'Skipped: \d+', s)
        if skipped_matches:
            try:
                return int(skipped_matches[0].split(' ')[-1])
            except ValueError:
                return 0
        return 0

    def get_test_framework(self) -> str:
        return 'JUnit'

    def detect(self) -> bool:
        return self.log.find('junit') >= 0
