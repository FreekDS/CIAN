from analyzer.Cacher.CacherBase import CacherBase


class BranchInfoCache(CacherBase):

    def __init__(self, repo_path):
        super().__init__(repo_path, 'branches.cache')
