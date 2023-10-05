import pytest

from fastapi.testclient import TestClient

from ...api.main import app
from ...config import get_settings
from ...db.database import Base


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as _client:
        yield _client


@pytest.fixture()
def base_url():
    return f"{get_settings().base_url}/"


@pytest.fixture()
def mock_url():
    return "https://www.python.org/"


@pytest.fixture()
def bad_request():
    return "The provided URL '123' is not valid! Please use this format: {}"


@pytest.fixture(scope="function")
def test_db_session():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    test_engine = create_engine(get_settings().db_url)

    Base.metadata.create_all(bind=test_engine)

    Session = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    test_db = Session()

    try:
        yield test_db
    finally:
        test_db.close()
