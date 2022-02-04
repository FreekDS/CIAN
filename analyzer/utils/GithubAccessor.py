import os
import functools
import requests


class GithubAccessorError(Exception):
    pass


class GithubAccessor:

    TOKENS = None
    TOKEN_PTR = 0

    def __init__(self):
        self.initialize()
        self._url_base = 'https://api.github.com'

    @property
    def token(self):
        return self.TOKENS[self.TOKEN_PTR]

    def _make_header(self):
        return {
            'Authorization': f'token {self.token}'
        }

    @staticmethod
    def use_token(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            ret = func(self, *args, **kwargs)
            GithubAccessor.TOKEN_PTR += 1
            GithubAccessor.TOKENS %= len(GithubAccessor.TOKENS)
            return ret
        return wrapper

    @staticmethod
    def initialize():
        if GithubAccessor.initialized():
            return
        t_count = int(os.getenv('GH_TOKEN_COUNT', 0))
        GithubAccessor.TOKENS = list()
        for i in range(t_count):
            token = os.getenv(f'GH_TOKEN_{i+1}', None)
            if token:
                GithubAccessor.TOKENS.append(token)

    @staticmethod
    def initialized():
        if GithubAccessor.TOKENS:
            return len(GithubAccessor.TOKENS) >= 1
        return False

    @use_token
    def _make_request(self, *args: str, query: str = str()):
        endpoint = '/'.join(args)
        url = f'{self._url_base}/{endpoint}'
        if query:
            url = f'{url}?{query}'
        response = requests.get(url, headers=self._make_header())
        if response.status_code == 200 or response.status_code == 201:
            return response.text
        raise GithubAccessorError(
            f"Cannot perform GitHub request '{url}', got response {response.status_code}"
        )
