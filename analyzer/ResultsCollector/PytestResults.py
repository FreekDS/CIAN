import re
from analyzer.utils.TestResultCommand import TestResultCommand


class PytestResult(TestResultCommand):

    def get_test_framework(self) -> str:
        try:
            matches = re.search(r'pytest(-((\d+\.?)+[a-zA-E-Z0-9-]*))?', self.log)
            if matches:
                pytest_version = matches[0]
                return pytest_version
            return str()
        except IndexError:
            return str()

    def _get_test_count_of_type(self, test_type):
        summary = self._get_summary()
        try:
            tests_str = re.findall(rf'\d+ {test_type}', summary)[0]
            test_count = int(tests_str.split(' ')[0])
            return test_count
        except ValueError:
            return 0
        except IndexError:
            return 0

    def _get_summary(self):
        regex = r'=+ .* =+'
        return re.findall(regex, self.log)[-1]

    def detect(self) -> bool:
        found_start = re.findall('=+ test session starts =+', self.log)
        possible_ends = re.findall('=+ .* =+', self.log)
        found_end = len(possible_ends) > 1

        if found_start and found_end:
            exact_end = possible_ends[-1]
            start = found_start[0]

            start_i = self.log.index(start)
            end_i = self.log.index(exact_end, start_i) + len(exact_end)

            self.log = self.log[start_i:end_i]
            return True
        else:
            return False

    def get_failed_test_count(self):
        return self._get_test_count_of_type('failed')

    def get_successful_test_count(self):
        return self._get_test_count_of_type('passed')

    def get_skipped_test_count(self) -> int:
        return self._get_test_count_of_type('skipped')
