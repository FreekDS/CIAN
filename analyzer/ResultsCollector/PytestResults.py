from analyzer.utils.TestResultCommand import TestResultCommand


class PytestResult(TestResultCommand):

    def get_skipped_test_count(self) -> int:
        pass

    def detect(self) -> bool:
        pass

    def get_failed_test_count(self):
        pass

    def get_successful_test_count(self):
        pass

    def execute(self):
        pass

