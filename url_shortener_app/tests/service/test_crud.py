from .fixtures import test_db_session
from ...helpers import crud
from ...db import schemas
from ...helpers.exceptions import SAMPLE_URL


def test_create_db_url(test_db_session):
    test_url = schemas.URLBase(target_url=SAMPLE_URL)
    db_url = crud.create_db_url(test_db_session, test_url)

    assert db_url is not None
    assert db_url.target_url == SAMPLE_URL


def test_get_db_url_by_key(test_db_session):
    test_url = schemas.URLBase(target_url=SAMPLE_URL)
    db_url = crud.create_db_url(test_db_session, test_url)
    retrieved_url = crud.get_db_url_by_key(test_db_session, db_url.key)

    assert retrieved_url is not None
    assert retrieved_url.key == db_url.key
    assert retrieved_url.target_url == db_url.target_url


def test_deactivate_db_url_by_secret_key(test_db_session):
    test_url = schemas.URLBase(target_url=SAMPLE_URL)
    db_url = crud.create_db_url(test_db_session, test_url)
    deactivated_url = crud.deactivate_db_url_by_secret_key(
        test_db_session, db_url.secret_key
    )

    assert deactivated_url is not None
    assert not deactivated_url.is_active
