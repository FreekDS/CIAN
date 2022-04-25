import pytest
import os

from analyzer.ResultsCollector.GTestResults import GTestResults


def text(p):
    with open(p, 'rb') as f:
        lines = [s.decode('utf-8', errors='ignore') for s in f.readlines()]
        return '\n'.join(lines)


@pytest.fixture(scope='module')
def data(data_dir):
    return os.path.join(data_dir, 'GTestResults')


@pytest.fixture(scope='module')
def gtest1(data):
    return GTestResults(text(f"{data}/log_example.txt"))


@pytest.fixture(scope='module')
def gtest2(data):
    return GTestResults(text(f"{data}/log_example2.txt"))


@pytest.fixture(scope='module')
def invalid(data):
    return GTestResults(text(f"{data}/no_log.txt"))


@pytest.fixture(scope='module')
def invalid2(data):
    return GTestResults(text(f"{data}/invalid.txt"))


def test_get_framework(gtest1, gtest2, invalid, invalid2):
    assert gtest1.get_test_framework() == 'GoogleTest'
    assert gtest2.get_test_framework() == 'GoogleTest'
    assert invalid.get_test_framework() == 'GoogleTest'
    assert invalid2.get_test_framework() == 'GoogleTest'
