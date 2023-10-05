from ...helpers.exceptions import InvalidURLException, URLNotFoundException, SAMPLE_URL


def test_invalid_url_exception():
    requested_url = "invalid_url"
    exception = InvalidURLException(requested_url)

    assert exception.status_code == 400
    assert (
        exception.detail
        == f"The provided URL '{requested_url}' is not valid! Please use this format: {SAMPLE_URL}"
    )


def test_url_not_found_exception():
    requested_url = SAMPLE_URL
    exception = URLNotFoundException(requested_url)

    assert exception.status_code == 404
    assert exception.detail == f"URL '{requested_url}' doesn't exist"
