from utils.Command import Command
from typing import Union


class CircleCIDetector(Command):
    def execute(self, repo) -> Union[None or str]:
        return None
