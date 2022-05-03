import pytest
import os

from analyzer.ResultsCollector.JestResults import JestResults


@pytest.fixture(scope='module')
def data(data_dir):
    return os.path.join(data_dir, 'JestResults')


def text(p):
    with open(p) as f:
        return '\n'.join(f.readlines())


@pytest.fixture(scope='module')
def jest1(data):
    return JestResults(text(f"{data}/valid.txt"))


@pytest.fixture(scope='module')
def jest2(data):
    return JestResults(text(f"{data}/valid2.txt"))


@pytest.fixture(scope='module')
def invalid_jest(data):
    return JestResults(text(f"{data}/invalid.txt"))


def test_get_summary(jest1, jest2, invalid_jest):
    assert jest1.get_summary() == "Tests:       537 passed, 537 total\n"
    assert invalid_jest.get_summary() != "Tests:       537 passed, 537 total\n"
    assert invalid_jest.get_summary() == str()

    assert jest2.get_summary() == "Tests:       121 failed, 7 skipped, 537 passed, 537 total\n"


def test_get_tests_of_type(jest1, jest2, invalid_jest):
    assert invalid_jest._get_test_of_type('passed') == 0
    assert invalid_jest._get_test_of_type('failed') == 0
    assert invalid_jest._get_test_of_type('skipped') == 0
    assert invalid_jest._get_test_of_type('hahahahahhahaaa') == 0

    assert jest1._get_test_of_type('passed') == 537
    assert jest1._get_test_of_type('failed') == 0
    assert jest1._get_test_of_type('skipped') == 0
    assert jest1._get_test_of_type('hohohohohohohoho') == 0

    assert jest2._get_test_of_type('passed') == 537
    assert jest2._get_test_of_type('failed') == 121
    assert jest2._get_test_of_type('skipped') == 7
    assert jest2._get_test_of_type('hihihihihihiiihiii') == 0


def test_skipped_failed_passed_count(jest1, jest2, invalid_jest):
    assert jest1.get_test_count() == 537
    assert jest2.get_test_count() == 665
    assert invalid_jest.get_test_count() == 0

    assert jest1.get_successful_test_count() == 537
    assert jest2.get_successful_test_count() == 537
    assert invalid_jest.get_successful_test_count() == 0

    assert jest1.get_failed_test_count() == 0
    assert jest2.get_failed_test_count() == 121
    assert invalid_jest.get_failed_test_count() == 0

    assert jest1.get_skipped_test_count() == 0
    assert jest2.get_skipped_test_count() == 7
    assert invalid_jest.get_skipped_test_count() == 0
