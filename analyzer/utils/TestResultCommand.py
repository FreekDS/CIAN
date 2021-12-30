from abc import abstractmethod
from analyzer.utils.Command import Command


class TestResultCommand(Command):
    __test__ = False

    @abstractmethod
    def get_test_count(self):
        pass

    @abstractmethod
    def get_failed_test_count(self):
        pass

    @abstractmethod
    def get_successful_test_count(self):
        pass

    def __init__(self, log):
        self.log = log
