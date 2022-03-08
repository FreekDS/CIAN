from analyzer.Cacher.CacherBase import CacherBase

# TODO add tests for cacher
# TODO add CLI option to enable/disable cache


class BranchInfoCache(CacherBase):

    def __init__(self, repo_name):
        super().__init__(repo_name, 'branches.cache')
