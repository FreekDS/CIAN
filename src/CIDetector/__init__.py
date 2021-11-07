from typing import List, AnyStr
from config import CIRCLE_CI, TRAVIS_CI, GH_ACTIONS
from .TravisDetector import TravisDetector
from .GithubActionsDectector import GithubActionsDetector


# Check if workflow files exists
# This is not enough as it does not mean there are actual executions
def detect_ci_tools(repo) -> List[AnyStr]:
    detected_tools = []
    if repo.path_exists(".circleci/config.yml"):
        detected_tools.append(CIRCLE_CI)
    if TravisDetector().execute(repo):
        detected_tools.append(TRAVIS_CI)
    if GithubActionsDetector().execute(repo):
        detected_tools.append(GH_ACTIONS)

    return detected_tools
