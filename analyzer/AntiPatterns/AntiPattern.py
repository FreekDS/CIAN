from typing import List
from analyzer.Builds.Build import Build
from abc import ABC, abstractmethod


class AntiPattern(ABC):
    def __init__(self, builds: List[Build], name=''):
        self.builds = builds
        self.name = name

    @abstractmethod
    def detect(self):
        raise NotImplementedError()

