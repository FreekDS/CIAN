from abc import ABC, abstractmethod
from analyzer.Workflow import WorkflowRun, Workflow
from typing import List


class Repo(ABC):
    def __init__(self, path, repo_type):
        self.path = path
        self.repo_type = repo_type
        self.workflows: List[Workflow] = []
        self.workflow_runs: List[WorkflowRun] = []

    @abstractmethod
    def path_exists(self, path) -> bool:
        pass

    @abstractmethod
    def dir_empty(self, path) -> bool:
        pass

    @abstractmethod
    def fetch_builtin_ci(self):
        pass
