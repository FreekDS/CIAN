from typing import List, AnyStr
from .TravisDetector import TravisDetector
from .GithubActionsDectector import GithubActionsDetector
from .CircleCIDetector import CircleCIDetector


def detect_ci_tools(repo) -> List[AnyStr]:

    detectors = [
        TravisDetector(),
        GithubActionsDetector(),
        CircleCIDetector()
    ]

    tools = []
    for detector in detectors:
        detected = detector.execute(repo)
        if detected:
            tools.append(detected)

    return tools
