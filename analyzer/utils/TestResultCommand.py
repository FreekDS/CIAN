from abc import abstractmethod
from analyzer.utils.Command import Command


class TestResultCommand(Command):
    __test__ = False

    def get_test_count(self) -> int:
        return self.get_successful_test_count() + self.get_failed_test_count() + self.get_skipped_test_count()

    @abstractmethod
    def get_failed_test_count(self) -> int:
        pass

    @abstractmethod
    def get_successful_test_count(self) -> int:
        pass

    @abstractmethod
    def get_skipped_test_count(self) -> int:
        pass

    @abstractmethod
    def get_test_framework(self) -> str:
        pass

    @abstractmethod
    def detect(self) -> bool:
        pass

    def execute(self, *args, **kwargs):
        if self.detect():
            return {
                'test_count': self.get_test_count(),
                'failed_count': self.get_failed_test_count(),
                'successful_count': self.get_successful_test_count(),
                'skipped_count': self.get_skipped_test_count(),
                'framework': self.get_test_framework()
            }
        return None

    def __init__(self, log):
        self.log = log
