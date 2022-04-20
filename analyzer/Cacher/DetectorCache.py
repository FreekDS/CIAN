from analyzer.Cacher.CacherBase import CacherBase


class DetectorCache(CacherBase):

    def __init__(self, repo_path):
        super().__init__(repo_path, 'detection.cache')
