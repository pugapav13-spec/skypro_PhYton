import requests
import pytest
from Config import config


@pytest.mark.order(2)
def test_positive_change():
    if not config.project_id:
        pytest.skip("Сначала запустите test_create.py для создания проекта")

    url = config.put_url()
    headers = config.headers()
    body = config.put_body()

    resp = requests.put(
        url,
        json=body,
        headers=headers
    )
    assert resp.status_code == 200


@pytest.mark.order(2)
def test_negative_change():
    url = config.put_url_negative()
    body = config.put_body()
    headers = config.headers()

    resp = requests.put(
        url,
        json=body,
        headers=headers
    )
    assert resp.status_code == 404
