import os
import pytest

from analyzer.ResultsCollector.PytestResults import PytestResult

pytest_version = 'pytest-6.2.5'


@pytest.fixture(scope='module')
def data(data_dir):
    return os.path.join(data_dir, 'PytestResults')


@pytest.fixture(scope='module')
def happy_day(data):
    with open(os.path.join(data, 'happy_day.txt'), 'r') as f1:
        with open(os.path.join(data, 'happy_day2.txt'), 'r') as f2:
            return [f1.read(), f2.read()]


def test_get_framework_happyday(happy_day):
    for st in happy_day:
        result = PytestResult(st)
        assert result.get_test_framework() == pytest_version


def test_get_framework_fail(data):
    with open(os.path.join(data, 'no_framework.txt')) as f:
        result = PytestResult(f.read())

        assert result.get_test_framework() != pytest_version
        assert result.get_test_framework() == str()


def test_detect_happyday(happy_day):
    for st in happy_day:
        result = PytestResult(st)
        assert result.detect()


def test_detect_fail(data):

    def fail(file_name):
        with open(os.path.join(data, file_name), 'r') as f:
            result = PytestResult(f.read())
            assert not result.detect()

    files = ['wrong_end.txt', 'wrong_end2.txt', 'wrong_start_log.txt']
    for f in files:
        fail(f)
