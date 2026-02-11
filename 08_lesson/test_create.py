import requests
import pytest
from Config import config


@pytest.mark.order(1)
def test_positive_create():
    url = config.post_url()
    headers = config.headers()
    body = config.post_body()

    resp = requests.post(
        url,
        json=body,
        headers=headers
    )
    assert resp.status_code == 201

    created_id = resp.json().get("id")
    config.project_id = created_id
    assert created_id is not None
    assert len(created_id) > 0


@pytest.mark.order(1)
def test_negative_create():
    url = config.post_url()
    body = config.post_body_negative()
    headers = config.headers()

    resp = requests.post(
        url,
        json=body,
        headers=headers
    )

    assert resp.status_code == 400
