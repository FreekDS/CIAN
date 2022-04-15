from analyzer.Cacher.CacherBase import CacherBase

# TODO add tests for cacher
# TODO add CLI option to enable/disable cache


class BranchInfoCache(CacherBase):

    def __init__(self, repo_path):
        super().__init__(repo_path, 'branches.cache')
