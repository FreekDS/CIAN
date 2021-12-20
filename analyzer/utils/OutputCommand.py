from abc import ABC, abstractmethod
from typing import List, Dict, Any
from analyzer.utils.Command import Command


class OutputCommand(Command, ABC):

    @abstractmethod
    def __init__(self, type_name, analysis_results=None) -> None:
        super().__init__()
        self.analysis_results: List[Dict[str, Any]] = analysis_results if analysis_results else []
        self.type = type_name

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        pass
