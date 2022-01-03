import pytest
import os
from dotenv import load_dotenv


@pytest.fixture(scope='session', autouse=True)
def configure_environment():
    load_dotenv()


@pytest.fixture(scope='session')
def data_dir():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, './data'))
