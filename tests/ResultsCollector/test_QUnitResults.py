import pytest
import os

from analyzer.ResultsCollector.QUnitResults import QUnitResults


@pytest.fixture(scope='module')
def data(data_dir):
    return os.path.join(data_dir, 'QUnitResults')


def text(p):
    with open(p) as f:
        return '\n'.join(f.readlines())


@pytest.fixture(scope='module')
def qunit1(data):
    return QUnitResults(text(f"{data}/valid.txt"))


@pytest.fixture(scope='module')
def qunit2(data):
    return QUnitResults(text(f"{data}/valid2.txt"))


@pytest.fixture(scope='module')
def invalid_qunit(data):
    return QUnitResults(text(f"{data}/invalid.txt"))


@pytest.fixture(scope='module')
def invalid_qunit2(data):
    return QUnitResults(text(f"{data}/invalid2.txt"))


def test_get_summary(qunit1, qunit2, invalid_qunit, invalid_qunit2):
    assert qunit1.get_summary() == '>> 1678 tests completed with 0 failed, 0 skipped, and 0 todo'
    assert qunit2.get_summary() == '>> 5498 tests completed with 17 failed, 90 skipped, and 7 todo'
    assert invalid_qunit.get_summary() == ""

    # invalid2 contains kunit instead of qunit, but summary is not changed
    assert invalid_qunit2.get_summary() == ">> 1678 tests completed with 0 failed, 0 skipped, and 0 todo"


def test_get_tests_of_type(qunit1, qunit2, invalid_qunit, invalid_qunit2):
    assert invalid_qunit._get_tests_of_type('tests') == 0
    assert invalid_qunit._get_tests_of_type('failed') == 0
    assert invalid_qunit._get_tests_of_type('skipped') == 0
    assert invalid_qunit._get_tests_of_type('hahahahahhahaaa') == 0

    assert invalid_qunit2._get_tests_of_type('tests') == 0
    assert invalid_qunit2._get_tests_of_type('failed') == 0
    assert invalid_qunit2._get_tests_of_type('skipped') == 0
    assert invalid_qunit2._get_tests_of_type('hahahahahhahaaa') == 0

    assert qunit1._get_tests_of_type('tests') == 1678
    assert qunit1._get_tests_of_type('failed') == 0
    assert qunit1._get_tests_of_type('skipped') == 0
    assert qunit1._get_tests_of_type('hohohohohohohoho') == 0

    assert qunit2._get_tests_of_type('tests') == 5498
    assert qunit2._get_tests_of_type('failed') == 17
    assert qunit2._get_tests_of_type('skipped') == 90
    assert qunit2._get_tests_of_type('hihihihihihiiihiii') == 0


def test_skipped_failed_passed_count(qunit1, qunit2, invalid_qunit, invalid_qunit2):
    pass


def test_detect(qunit1, qunit2, invalid_qunit, invalid_qunit2):
    pass
