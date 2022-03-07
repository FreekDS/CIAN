from abc import ABC, abstractmethod
from analyzer.Builds import Build
from analyzer.Cacher.BranchInfoCache import BranchInfoCache
from typing import List


class Repo(ABC):
    def __init__(self, path, repo_type):
        self.path = path
        self.name = path.split('/')[-1] if '/' in path else path
        self.repo_type = repo_type
        self.builds: List[Build] = []
        self.branch_info = None

    @abstractmethod
    def path_exists(self, path) -> bool:
        pass

    @abstractmethod
    def dir_empty(self, path) -> bool:
        pass

    def branch_information(self, use_cache=True, create_cache=True) -> dict:
        cache = BranchInfoCache(self.name)

        if cache.hit() and use_cache:
            return cache.restore(default={})

        b_info = self._branch_information()

        if create_cache:
            cache.create(b_info)

        return b_info

    @abstractmethod
    def _branch_information(self) -> dict:
        pass
