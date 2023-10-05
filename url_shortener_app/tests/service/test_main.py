from fastapi import status

from .fixtures import client, base_url, mock_url, bad_request, test_db_session
from ...api.main import app
from ...helpers.exceptions import SAMPLE_URL


def test_read_root(client):
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "Welcome to the URL shortener API :)"


def test_create_url_valid(client, base_url, mock_url):
    url = {"target_url": mock_url}
    response = client.post("/url", json=url)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["url"].startswith(base_url)
    assert "admin_url" in data


def test_create_url_invalid(client, bad_request):
    url = {"target_url": "123"}
    response = client.post("/url", json=url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": bad_request.format(SAMPLE_URL)}


def test_get_url_info_valid(client, base_url, mock_url):
    url = {"target_url": mock_url}
    response_create = client.post("/url", json=url)
    data_create = response_create.json()
    secret_key = data_create["admin_url"].split("/")[-1]

    response_get = client.get(f"/admin/{secret_key}")

    assert response_get.status_code == status.HTTP_200_OK

    data_get = response_get.json()

    assert data_get["url"].startswith(base_url)
    assert "admin_url" in data_get


def test_get_url_info_invalid(client):
    requested_key = "/admin/nonexistent_key"
    response = client.get(requested_key)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": f"URL 'http://testserver{requested_key}' doesn't exist"
    }


def test_delete_url_valid(client, mock_url):
    url = {"target_url": mock_url}
    response_create = client.post("/url", json=url)
    data_create = response_create.json()
    secret_key = data_create["admin_url"].split("/")[-1]
    response_delete = client.delete(f"/admin/{secret_key}")

    assert response_delete.status_code == status.HTTP_200_OK
    assert response_delete.json() == {
        "detail": f"Successfully deleted shortened URL for '{mock_url}'"
    }


def test_delete_url_invalid(client):
    requested_key = "/admin/nonexistent_key"
    response = client.delete(requested_key)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": f"URL 'http://testserver{requested_key}' doesn't exist"
    }
