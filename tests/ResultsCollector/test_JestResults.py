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
def invalid_jest(data):
    return JestResults(text(f"{data}/invalid.txt"))


def test_get_summary(jest1, invalid_jest):
    assert jest1.get_summary() == "Tests:       537 passed, 537 total\n"
    assert invalid_jest.get_summary() != "Tests:       537 passed, 537 total\n"
    assert invalid_jest.get_summary() == str()
