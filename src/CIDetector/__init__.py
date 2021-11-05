from typing import List, AnyStr
from ..config import CIRCLE_CI, TRAVIS_CI, GH_ACTIONS


# Check if workflow files exists
# This is not enough as it does not mean there are actual executions
# TODO: test for run executions using the APIs
def detect_ci_tools(repo) -> List[AnyStr]:
    detected_tools = []
    if repo.path_exists(".circleci/config.yml"):
        detected_tools.append(CIRCLE_CI)
    if repo.path_exists(".travis.yml"):
        detected_tools.append(TRAVIS_CI)
    if not repo.dir_empty(".github/workflows/") and len(repo.workflows) != 0:
        detected_tools.append(GH_ACTIONS)

    return detected_tools
