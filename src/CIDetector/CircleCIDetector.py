import json
import os
import requests
from config import CIRCLE_CI
from utils.Command import Command
from typing import Union


class CircleCIDetector(Command):
    def __init__(self):
        self.headers = {
            'Circle-Token': os.getenv('CIRCLE_CI')
        }

    def execute(self, repo) -> Union[None or str]:
        provider = 'gh' if repo.repo_type == 'github' else ''

        slug = f'{provider}/{repo.path}'

        url = f'https://circleci.com/api/v2/insights/{slug}/workflows'
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200:
            data = json.loads(resp.text)
            if len(data['items']) > 0:
                return CIRCLE_CI
        return None
