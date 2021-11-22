import pytest
from dotenv import load_dotenv


@pytest.fixture(scope='session', autouse=True)
def configure_environment():
    load_dotenv()
