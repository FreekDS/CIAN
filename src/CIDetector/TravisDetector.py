from utils.Command import Command
from config import TRAVIS_CI
import os
import requests
import json
from typing import Union


class TravisDetector(Command):
    def __init__(self):
        self.headers = {
            'Authorization': f'token {os.getenv("TRAVIS_CI")}',
            'Travis-API-Version': '3',
            'User-Agent': 'Git-Ci-Analyzer/v1.0'
        }

    def execute(self, repo) -> Union[None or str]:
        url_com = 'https://api.travis-ci.com/repo/' + repo.path.replace('/', '%2F')
        req_com = requests.get(url_com, headers=self.headers)
        if req_com.status_code == 200:
            resp_com = json.loads(req_com.text)
            if resp_com['active'] is True:
                return TRAVIS_CI
        return None
