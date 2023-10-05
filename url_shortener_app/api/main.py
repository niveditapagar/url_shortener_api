from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.datastructures import URL
from validators import url as is_valid_url

from ..config import get_settings
from ..db import models, schemas
from ..db.database import SessionLocal, engine
from ..helpers import crud
from ..helpers.exceptions import InvalidURLException, URLNotFoundException

app = FastAPI()


@app.on_event("startup")
def create_database():
    """
    Create the tables in the database if they don't already exist.
    """
    models.Base.metadata.create_all(bind=engine)


def get_db():
    """
    Database session to be used in request handlers.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    """
    Get administrative info for a shortened URL.
    """
    base_url = URL(get_settings().base_url)
    admin_endpoint = app.url_path_for(
        "administration info", secret_key=db_url.secret_key
    )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url


@app.get("/")
def read_root():
    """
    Root endpoint that returns a welcome message.
    """
    return "Welcome to the URL shortener API :)"


@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    """
    Create a shortened URL.
    """
    if not is_valid_url(url.target_url):
        raise InvalidURLException(url.target_url)
    db_url = crud.create_db_url(db=db, url=url)
    return get_admin_info(db_url)


@app.get("/{url_key}")
def forward_to_target_url(
    url_key: str, request: Request, db: Session = Depends(get_db)
):
    """
    Redirect to the target URL associated with the given URL key.
    """
    if db_url := crud.get_db_url_by_key(db=db, url_key=url_key):
        crud.update_db_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.target_url, status_code=status.HTTP_302_FOUND)
    else:
        raise URLNotFoundException(request.url)


@app.get(
    "/admin/{secret_key}",
    name="administration info",
    response_model=schemas.URLInfo,
)
def get_url_info(secret_key: str, request: Request, db: Session = Depends(get_db)):
    """
    Retrieve administrative info for a shortened URL.
    """
    if db_url := crud.get_db_url_by_secret_key(db, secret_key=secret_key):
        return get_admin_info(db_url)
    else:
        raise URLNotFoundException(request.url)


@app.delete("/admin/{secret_key}")
def delete_url(secret_key: str, request: Request, db: Session = Depends(get_db)):
    """
    Delete a shortened URL.
    """
    db_url = crud.deactivate_db_url_by_secret_key(db, secret_key=secret_key)
    if db_url:
        message = f"Successfully deleted shortened URL for '{db_url.target_url}'"
        return {"detail": message}
    else:
        raise URLNotFoundException(request.url)