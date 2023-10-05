from sqlalchemy.orm import Session
from . import utils
from ..db import models, schemas


def create_db_url(db: Session, url: schemas.URLBase) -> models.URL:
    """
    Create a new URL in the database.

    Args:
        db (Session): The database session.
        url (schemas.URLBase): The URL information to create.

    Returns:
        models.URL: The created URL.
    """
    key = utils.create_unique_random_key(db)
    secret_key = f"{key}_{utils.create_random_key(length=8)}"

    db_url = models.URL(target_url=url.target_url, key=key, secret_key=secret_key)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def get_db_url_by_key(db: Session, url_key: str) -> models.URL:
    """
    Retrieve a URL from the database by its key.

    Args:
        db (Session): The database session.
        url_key (str): The key of the URL to retrieve.

    Returns:
        models.URL: The retrieved URL, if it exists and is active.
    """
    return (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active)
        .first()
    )


def get_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
    """
    Retrieve a URL from the database by its secret key.

    Args:
        db (Session): The database session.
        secret_key (str): The secret key of the URL to retrieve.

    Returns:
        models.URL: The retrieved URL, if it exists and is active.
    """
    return (
        db.query(models.URL)
        .filter(models.URL.secret_key == secret_key, models.URL.is_active)
        .first()
    )


def update_db_clicks(db: Session, db_url: schemas.URL) -> schemas.URL:
    """
    Update the click count for a URL.

    Args:
        db (Session): The database session.
        db_url (schemas.URL): The URL to update.

    Returns:
        schemas.URL: The updated URL.
    """
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url


def deactivate_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
    """
    Deactivate a URL by its secret key.

    Args:
        db (Session): The database session.
        secret_key (str): The secret key of the URL to deactivate.

    Returns:
        models.URL: The deactivated URL, if it exists and is deactivated.
    """
    db_url = get_db_url_by_secret_key(db, secret_key)
    if db_url:
        db_url.is_active = False
        db.commit()
        db.refresh(db_url)
    return db_url
