import os
import shutil

import pytest

from analyzer.Builds.Build import Build
from analyzer.Cacher.CacherBase import CacherBase
from analyzer.Cacher.BuildCache import BuildCache
from analyzer.Cacher.DetectorCache import DetectorCache
from analyzer.Cacher.BranchInfoCache import BranchInfoCache


@pytest.fixture(scope='module')
def cacher():
    return CacherBase(
        'repo',
        'file',
        test=True
    )


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


def test_hit(cacher):
    assert cacher.hit() is False
    if not os.path.exists('cache-t'):
        os.mkdir('cache-t')
    with open(cacher.fp, 'w') as f:
        f.write("\n")
    assert cacher.hit()
    shutil.rmtree('cache-t')
    assert not cacher.hit()


def test_create(cacher):
    if not os.path.exists('cache-t'):
        os.mkdir('cache-t')
    assert cacher.hit() is False

    assert cacher.create({'cache_me': True})
    assert os.path.exists(cacher.fp)

    assert not cacher.create({'dont_cache_me_now': True}, override=False)
    assert cacher.create({'cache_me_again': True})

    shutil.rmtree('cache-t')


def test_restore(cacher):
    if not os.path.exists('cache-t'):
        os.mkdir('cache-t')

    obj = {'cache_me': True}

    assert cacher.restore() is None
    assert cacher.restore(default=':(') == ':('

    assert cacher.create(obj)
    assert cacher.restore() == obj
    assert cacher.restore(default=':)') == obj

    shutil.rmtree('cache-t')


def test_remove(cacher):
    if not os.path.exists('cache-t'):
        os.mkdir('cache-t')
    assert not cacher.remove()
    assert cacher.create({'obj': True})
    assert os.path.exists(cacher.fp)
    assert cacher.remove()
    assert not os.path.exists(cacher.fp)

    shutil.rmtree('cache-t')


def test_detector_cache():
    dc = DetectorCache(
        'repo'
    )
    assert dc.fp.endswith('detection.cache')


def test_branch_info_cache():
    bic = BranchInfoCache('repo')
    assert bic.fp.endswith('branches.cache')


def test_build_cache():

    if not os.path.exists('cache-t'):
        os.mkdir('cache-t')

    bc = BuildCache('repo', test=True)
    assert bc.fp.endswith('builds.cache')

    builds = [Build('success'), Build('failure')]

    assert bc.create(builds)
    assert bc.restore() == builds
    assert bc.remove()

    shutil.rmtree('cache-t')
