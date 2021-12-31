from analyzer.utils.TestResultCommand import TestResultCommand
import re


class PytestResult(TestResultCommand):

    def get_skipped_test_count(self) -> int:
        pass

    def _get_summary(self):
        regex = r'============================= .* ============================='
        return re.findall(regex, self.log)[-1]

    def detect(self) -> bool:
        start = r'============================= test session starts =============================='
        end = r'============================= .* ============================='

        found_start = re.findall(start, self.log)
        found_end = re.findall(end, self.log)

        if found_start and found_end:
            exact_end = found_end[-1]

            start_i = self.log.index(start)
            end_i = self.log.index(exact_end, start_i) + len(exact_end)

            self.log = self.log[start_i:end_i]
            return True
        else:
            return False

    def _get_test_count_of_type(self, test_type):
        summary = self._get_summary()
        try:
            tests_str = re.findall(rf'\d+ {test_type}', summary)[0]
            test_count = int(tests_str.split(' ')[0])
            return test_count
        except ValueError or IndexError:
            return 0

    def get_failed_test_count(self):
        return self._get_test_count_of_type('failed')

    def get_successful_test_count(self):
        return self._get_test_count_of_type('passed')

    def execute(self):
        pass


if __name__ == '__main__':
    with open(r'C:\Users\Freek\Documents\School\Master-2\git-ci-analyzer\tests\data\actions_output_failed_example.txt') as f:
        text = f.read()
        detector = PytestResult(text)
        detector.detect()
        print(detector.get_successful_test_count())
        print(detector.get_failed_test_count())
        print(detector.get_skipped_test_count())
