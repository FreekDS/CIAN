import os

from analyzer.Repository.Repo import Repo
from analyzer.utils.GithubAccessor import GithubAccessor


class GithubRepo(Repo):

    def __init__(self, path):
        super().__init__(path, repo_type='github')
        self._gh_access = GithubAccessor()
        self._base_url = 'https://api.github.com'
        self._headers = {'Authorization': f'token {os.getenv("GH_TOKEN")}'}

    def path_exists(self, path) -> bool:
        return self._gh_access.get_content(self, path) is not None

    def dir_empty(self, path) -> bool:
        if not self.path_exists(path):
            return False
        content = self._gh_access.get_content(self, path)
        if isinstance(content, list):
            return len(content) == 0
        # is not directory, return True
        return True

    def get_last_sync(self, branch_name, main_b):
        prs = self._gh_access.get_closed_prs(self, base_branch=main_b, head_branch=branch_name)
        if prs:
            for p in prs:
                merged_date = p.get('merged_date', False)
                if merged_date:
                    return merged_date
        return False

    @staticmethod
    def get_main_branch_name(all_branches):
        if 'main' in all_branches:
            return 'main'
        return 'master'

    # TODO cache branch information
    def branch_information(self) -> dict:
        branch_info = dict()
        last_commit = self._gh_access.get_last_commit(self)

        branch_info['last_commit'] = last_commit.get('commit', {}).get('committer', {}).get('date', 'unknown')

        branches = self._gh_access.get_branches_with_latest_commit(self)

        main_b = self.get_main_branch_name([b.get('name') for b in branches])

        for branch in branches:
            b_name = branch.get('name')
            branch_info[b_name] = dict()

            last_commit = branch.get('commit').get('commit')
            branch_info[b_name]['last_commit'] = last_commit.get('committer', {}).get('date', 'unknown')

            l_sync = self.get_last_sync(b_name, main_b)
            if l_sync:
                branch_info[b_name]['merged'] = True
                branch_info[b_name]['sync'] = l_sync
            else:
                branch_info[b_name]['merged'] = False

        return branch_info
