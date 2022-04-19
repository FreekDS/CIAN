from analyzer.Cacher.CacherBase import CacherBase

# TODO add CLI option to enable/disable cache


class DetectorCache(CacherBase):

    def __init__(self, repo_path):
        super().__init__(repo_path, 'detection.cache')
