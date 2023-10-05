from fastapi import HTTPException
from starlette.datastructures import URL

SAMPLE_URL: str = "https://www.python.org/"


class InvalidURLException(HTTPException):
    def __init__(self, requested_url: str):
        message = f"The provided URL '{requested_url}' is not valid! Please use this format: {SAMPLE_URL}"
        super().__init__(status_code=400, detail=message)


class URLNotFoundException(HTTPException):
    def __init__(self, requested_url: URL):
        message = f"URL '{requested_url}' doesn't exist"
        super().__init__(status_code=404, detail=message)
