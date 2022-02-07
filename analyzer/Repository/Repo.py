from abc import ABC, abstractmethod
from analyzer.Builds import Build
from typing import List


class Repo(ABC):
    def __init__(self, path, repo_type):
        self.path = path
        self.name = path.split('/')[-1] if '/' in path else path
        self.repo_type = repo_type
        self.builds: List[Build] = []

    @abstractmethod
    def path_exists(self, path) -> bool:
        pass

    @abstractmethod
    def dir_empty(self, path) -> bool:
        pass
