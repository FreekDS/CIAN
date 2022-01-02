import pytest
import os
from dotenv import load_dotenv


@pytest.fixture(scope='session', autouse=True)
def configure_environment():
    load_dotenv()


@pytest.fixture(scope='session')
def data_dir():
    return os.path.abspath('./data')

