import requests
import pytest
from Config import config


@pytest.mark.order(3)
def test_positive_get():
    if not config.project_id:
        pytest.skip("Сначала запустите test_create.py для создания проекта")

    url = config.get_url()
    headers = config.headers()

    resp = requests.get(
        url,
        headers=headers
    )
    assert resp.status_code == 200


@pytest.mark.order(3)
def test_negative_get():
    url = config.get_url()

    resp = requests.get(
        url
    )
    assert resp.status_code == 401
