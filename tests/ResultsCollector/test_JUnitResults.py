import pytest
import os

from analyzer.ResultsCollector.JUnitResults import JUnitResults


@pytest.fixture(scope='module')
def data(data_dir):
    return os.path.join(data_dir, 'JUnitResults')


def text(p):
    with open(p) as f:
        return '\n'.join(f.readlines())


@pytest.fixture(scope='module')
def junit_1(data):
    return JUnitResults(text(f"{data}/log_example1.txt"))


@pytest.fixture(scope='module')
def junit_no_log(data):
    return JUnitResults(text(f"{data}/no_log.txt"))


def test_get_summary(junit_1, junit_no_log):
    assert junit_1.get_summary() != str()
    assert junit_1.get_summary() == 'Tests run: 1546, Failures: 0, Errors: 0, Skipped: 27'
    assert junit_no_log.get_summary() == str()


def test_get_framework(junit_1):
    assert junit_1.get_test_framework() == 'JUnit'
