import pytest
import os

from analyzer.ResultsCollector.CTestResults import CTestResults


def text(p):
    with open(p) as f:
        return '\n'.join(f.readlines())


@pytest.fixture(scope='module')
def data(data_dir):
    return os.path.join(data_dir, 'CTestResults')


@pytest.fixture(scope='module')
def ctest1(data):
    return CTestResults(text(f"{data}/log_example.txt"))


@pytest.fixture(scope='module')
def ctest2(data):
    return CTestResults(text(f"{data}/log_example2.txt"))


@pytest.fixture(scope='module')
def invalid(data):
    return CTestResults(text(f"{data}/no_log.txt"))


@pytest.fixture(scope='module')
def invalid2(data):
    return CTestResults(text(f"{data}/invalid.txt"))


def test_get_summary(ctest1, ctest2, invalid):
    assert invalid._get_summary() == str()
    assert ctest1._get_summary() != str()
    assert ctest2._get_summary() != str()
    assert ctest1._get_summary() == '100% tests passed, 0 tests failed out of 39\n'
    assert ctest2._get_summary() == '100% tests passed, 17 tests failed out of 39\n'


def test_get_total_count(ctest1, ctest2, invalid):
    assert invalid.get_test_count() == 0
    assert ctest1.get_test_count() == 39
    assert ctest2.get_test_count() == 39


def test_get_failed_count(ctest1, ctest2, invalid, invalid2):
    assert invalid.get_failed_test_count() == 0
    assert invalid2.get_failed_test_count() == 0
    assert ctest1.get_failed_test_count() == 0
    assert ctest2.get_failed_test_count() == 17
