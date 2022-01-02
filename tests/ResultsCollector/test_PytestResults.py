import os
import pytest

from analyzer.ResultsCollector.PytestResults import PytestResult

pytest_version = 'pytest-6.2.5'


@pytest.fixture(scope='module')
def data(data_dir):
    return os.path.join(data_dir, 'PytestResults')


def test_get_framework_happyday(data):
    with open(os.path.join(data, 'happy_day.txt'), 'r') as f1:
        with open(os.path.join(data, 'happy_day2.txt'), 'r') as f2:
            result1 = PytestResult(f1.read())
            result2 = PytestResult(f2.read())

            assert result1.get_test_framework() == pytest_version
            assert result2.get_test_framework() == pytest_version


def test_get_framework_wrong(data):
    with open(os.path.join(data, 'no_framework.txt')) as f:
        result = PytestResult(f.read())

        assert result.get_test_framework() != pytest_version
        assert result.get_test_framework() == str()
