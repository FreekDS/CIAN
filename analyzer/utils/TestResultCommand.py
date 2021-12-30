from abc import ABC, abstractmethod

from analyzer.utils import Command


class TestResultCommand(Command, ABC):
    __test__ = False

    @abstractmethod
    def __init__(self, log):
        self.log = log
