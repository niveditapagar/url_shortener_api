import secrets
import string
from sqlalchemy.orm import Session
from typing import Dict
from . import crud


def key_exists(urls: Dict[str, Dict[str, str]], key: str) -> bool:
    """
    Check if a key exists in a dictionary of URLs.

    Args:
        urls (Dict[str, Dict[str, str]): Dictionary of URLs.
        key (str): The key to check.

    Returns:
        bool: True if the key exists, False otherwise.
    """
    return key in urls


def create_random_key(length: int = 6) -> str:
    """
    Create a random key with the specified length.

    Args:
        length (int): Length of the random key.

    Returns:
        str: The generated random key.
    """
    return "".join(
        secrets.choice(string.ascii_uppercase + string.digits) for _ in range(length)
    )


def create_unique_random_key(db: Session) -> str:
    """
    Create a unique random key not present in the database.

    Args:
        db (Session): The database session.

    Returns:
        str: The unique random key.
    """
    key = create_random_key()
    while crud.get_db_url_by_key(db, key):
        key = create_random_key()
    return key
