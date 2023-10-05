from .fixtures import test_db_session
from ...helpers.utils import key_exists, create_random_key, create_unique_random_key
from ...helpers.exceptions import SAMPLE_URL
from ...helpers import crud
from ...db.schemas import URLBase


def test_key_exists():
    urls = {"key1": {"target_url": SAMPLE_URL}}

    assert key_exists(urls, "key1") is True
    assert key_exists(urls, "key2") is False


def test_create_random_key():
    key = create_random_key(8)
    assert len(key) == 8


def test_create_unique_random_key(test_db_session):
    db = test_db_session

    key = "test_key"
    url_base = URLBase(target_url=SAMPLE_URL)
    url_base.target_url = SAMPLE_URL
    crud.create_db_url(db, url_base)

    unique_key = create_unique_random_key(db)
    assert unique_key != key
