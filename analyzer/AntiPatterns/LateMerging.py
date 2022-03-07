import datetime

from analyzer.AntiPatterns.AntiPattern import AntiPattern
from analyzer.Builds.Build import Build
from typing import List

import numpy as np


class LateMerging(AntiPattern):

    def __init__(self, builds: List[Build], branch_info):
        super().__init__(builds, 'Late Merging')
        self.branch_info = branch_info

    def detect(self) -> dict:
        pass
