import pytest
import os

from analyzer.ResultsCollector.QUnitResults import QUnitResults


@pytest.fixture(scope='module')
def data(data_dir):
    return os.path.join(data_dir, 'MochaResults')


def text(p):
    with open(p) as f:
        return '\n'.join(f.readlines())


@pytest.fixture(scope='module')
def mocha1(data):
    return QUnitResults(text(f"{data}/valid.txt"))


@pytest.fixture(scope='module')
def mocha2(data):
    return QUnitResults(text(f"{data}/valid2.txt"))


@pytest.fixture(scope='module')
def invalid_mocha(data):
    return QUnitResults(text(f"{data}/invalid.txt"))


@pytest.fixture(scope='module')
def invalid_mocha2(data):
    return QUnitResults(text(f"{data}/invalid2.txt"))


def test_get_summary(mocha1, mocha2, invalid_mocha, invalid_mocha2):
    pass


def test_get_tests_of_type(mocha1, mocha2, invalid_mocha, invalid_mocha2):
    assert invalid_mocha._get_tests_of_type('tests') == 0
    assert invalid_mocha._get_tests_of_type('failed') == 0
    assert invalid_mocha._get_tests_of_type('skipped') == 0
    assert invalid_mocha._get_tests_of_type('hahahahahhahaaa') == 0

    assert invalid_mocha2._get_tests_of_type('tests') == 0
    assert invalid_mocha2._get_tests_of_type('failed') == 0
    assert invalid_mocha2._get_tests_of_type('skipped') == 0
    assert invalid_mocha2._get_tests_of_type('hahahahahhahaaa') == 0

    assert mocha1._get_tests_of_type('tests') == 1678
    assert mocha1._get_tests_of_type('failed') == 0
    assert mocha1._get_tests_of_type('skipped') == 0
    assert mocha1._get_tests_of_type('hohohohohohohoho') == 0

    assert mocha2._get_tests_of_type('tests') == 5498
    assert mocha2._get_tests_of_type('failed') == 17
    assert mocha2._get_tests_of_type('skipped') == 90
    assert mocha2._get_tests_of_type('hihihihihihiiihiii') == 0


def test_skipped_failed_passed_count(mocha1, mocha2, invalid_mocha, invalid_mocha2):
    assert mocha1.get_test_count() == 1678
    assert mocha2.get_test_count() == 5498
    assert invalid_mocha.get_test_count() == 0
    assert invalid_mocha2.get_test_count() == 0

    assert mocha1.get_successful_test_count() == 1678
    assert mocha2.get_successful_test_count() == 5384
    assert invalid_mocha.get_successful_test_count() == 0
    assert invalid_mocha2.get_successful_test_count() == 0

    assert mocha1.get_failed_test_count() == 0
    assert mocha2.get_failed_test_count() == 17
    assert invalid_mocha.get_failed_test_count() == 0
    assert invalid_mocha2.get_failed_test_count() == 0

    assert mocha1.get_skipped_test_count() == 0
    assert mocha2.get_skipped_test_count() == 90
    assert invalid_mocha.get_skipped_test_count() == 0
    assert invalid_mocha2.get_skipped_test_count() == 0


def test_detect(mocha1, mocha2, invalid_mocha, invalid_mocha2):
    assert mocha1.detect()
    assert mocha2.detect()
    assert not invalid_mocha.detect()
    assert not invalid_mocha2.detect()
