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


def test_get_summary(qunit1, qunit2, invalid_qunit):
    pass


def test_get_tests_of_type(qunit1, qunit2, invalid_qunit):
    pass


def test_skipped_failed_passed_count(qunit1, qunit2, invalid_qunit):
    pass


def test_detect(qunit1, qunit2, invalid_qunit):
    pass
