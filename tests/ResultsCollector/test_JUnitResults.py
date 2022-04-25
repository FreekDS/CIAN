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
def junit_2(data):
    return JUnitResults(text(f"{data}/log_example2.txt"))


@pytest.fixture(scope='module')
def junit_no_log(data):
    return JUnitResults(text(f"{data}/no_log.txt"))


def test_get_summary(junit_1, junit_no_log):
    assert junit_1.get_summary() != str()
    assert junit_1.get_summary() == 'Tests run: 1546, Failures: 0, Errors: 0, Skipped: 27'
    assert junit_no_log.get_summary() == str()


def test_get_framework(junit_1):
    assert junit_1.get_test_framework() == 'JUnit'


def test_detect(junit_1, junit_no_log):
    assert junit_1.detect()
    assert not junit_no_log.detect()


def test_successful_count(junit_1, junit_2, junit_no_log):
    assert junit_no_log.get_successful_test_count() == 0
    assert junit_1.get_successful_test_count() == 1519
    assert junit_2.get_successful_test_count() == 1409


def test_skipped_count(junit_1, junit_2, junit_no_log):
    assert junit_no_log.get_skipped_test_count() == 0
    assert junit_1.get_skipped_test_count() == 27
    assert junit_2.get_skipped_test_count() == 27


def test_failed_count(junit_1, junit_2, junit_no_log):
    assert junit_no_log.get_failed_test_count() == 0
    assert junit_1.get_failed_test_count() == 0
    assert junit_2.get_failed_test_count() == 110
