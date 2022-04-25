from analyzer.Cacher.CacherBase import CacherBase


def test_ctor():
    cb = CacherBase(
        'some/repo-path',
        'file-to-cache'
    )

    assert cb.repo == 'some-repo-path'
    assert cb.fp == 'cache/some-repo-path-file-to-cache.cache'

    cb = CacherBase(
        'some/repo-path',
        'file.cache'
    )

    assert cb.fp == 'cache/some-repo-path-file.cache'

    cb = CacherBase(
        'some/repo-path',
        'some/file.cache'
    )

    assert cb.fp == 'cache/some-repo-path-some-file.cache'
