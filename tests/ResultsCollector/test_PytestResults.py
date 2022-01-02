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
            return [PytestResult(f1.read()), PytestResult(f2.read())]


@pytest.fixture(scope='module')
def fail_data(data):
    files = ['wrong_end.txt', 'wrong_end2.txt', 'wrong_start_log.txt']
    fails = []
    for f in files:
        with open(os.path.join(data, f), 'r') as file:
            fails.append(PytestResult(file.read()))
    return fails


def test_get_framework_happyday(happy_day):
    for result in happy_day:
        assert result.get_test_framework() == pytest_version


def test_get_framework_fail(data):
    with open(os.path.join(data, 'no_framework.txt')) as f:
        result = PytestResult(f.read())

        assert result.get_test_framework() != pytest_version
        assert result.get_test_framework() == str()


def test_detect_happyday(happy_day):
    for result in happy_day:
        assert result.detect()


def test_detect_fail(fail_data):
    for f in fail_data:
        assert not f.detect()


def test_get_failed_count(data, fail_data):
    for f in fail_data:
        assert f.get_failed_test_count() == 0

    def failed_count(filename, expected):
        with open(os.path.join(data, filename), 'r') as fi:
            happy_day1 = PytestResult(fi.read())
            assert happy_day1.get_failed_test_count() == expected

    failed_count('happy_day.txt', 0)
    failed_count('happy_day2.txt', 1)
