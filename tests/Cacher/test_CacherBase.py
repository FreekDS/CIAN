import os
import shutil

import pytest
from analyzer.Cacher.CacherBase import CacherBase


@pytest.fixture(scope='module')
def cacher():
    return CacherBase(
        'repo',
        'file'
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
    os.mkdir('cache')
    with open(cacher.fp, 'w') as f:
        f.write("\n")
    assert cacher.hit()
    shutil.rmtree('cache')
    assert not cacher.hit()


def test_create(cacher):
    if not os.path.exists('cache'):
        os.mkdir('cache')
    assert cacher.hit() is False

    assert cacher.create({'cache_me': True})
    assert os.path.exists(cacher.fp)

    assert not cacher.create({'dont_cache_me_now': True}, override=False)
    assert cacher.create({'cache_me_again': True})

    shutil.rmtree('cache')


def test_restore(cacher):
    if not os.path.exists('cache'):
        os.mkdir('cache')

    obj = {'cache_me': True}

    assert cacher.restore() is None
    assert cacher.restore(default=':(') == ':('

    assert cacher.create(obj)
    assert cacher.restore() == obj
    assert cacher.restore(default=':)') == obj

    shutil.rmtree('cache')


def test_remove(cacher):
    if not os.path.exists('cache'):
        os.mkdir('cache')
    assert not cacher.remove()
    assert cacher.create({'obj': True})
    assert os.path.exists(cacher.fp)
    assert cacher.remove()
    assert not os.path.exists(cacher.fp)

    shutil.rmtree('cache')
