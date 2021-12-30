from abc import abstractmethod
from analyzer.utils.Command import Command


class TestResultCommand(Command):
    __test__ = False

    def get_test_count(self) -> int:
        return self.get_successful_test_count() + self.get_failed_test_count()

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
    def detect(self) -> bool:
        pass

    def __init__(self, log):
        self.log = log
