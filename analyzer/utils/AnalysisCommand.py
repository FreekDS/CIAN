from abc import ABC, abstractmethod

from analyzer.utils.Command import Command
from analyzer.Builds import Build
from typing import List, Dict, Any


class AnalysisCommand(Command, ABC):

    @abstractmethod
    def __init__(self, builds: List[Build], analysis_name, **kwargs):
        self.builds: List[Build] = builds
        self.name = analysis_name
        self.previous_analysis = None
        if self.analysis_dependencies():
            self.previous_analysis = kwargs.get('analysis_dependencies', dict())

    @abstractmethod
    def execute(self) -> Dict[str, Any]:
        pass

    @staticmethod
    def analysis_dependencies() -> List[str]:
        return list()
