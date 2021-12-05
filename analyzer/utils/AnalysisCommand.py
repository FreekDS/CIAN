from abc import ABC, abstractmethod

from analyzer.utils.Command import Command
from analyzer.Builds import Build
from typing import List, Dict, Any


class AnalysisCommand(Command, ABC):
    def __init__(self, builds: List[Build], analysis_name):
        self.builds: List[Build] = builds
        self.name = analysis_name

    @abstractmethod
    def execute(self) -> Dict[str, Any]:
        pass


