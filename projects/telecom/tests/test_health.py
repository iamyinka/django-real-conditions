from unittest import mock

import pytest
from django.db import OperationalError


def test_healthz_is_ok_without_touching_the_database(client):
    # No django_db mark: pytest-django fails this test if the view touches the database.
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert "no-cache" in response["Cache-Control"]


def test_healthz_rejects_post(client):
    assert client.post("/healthz").status_code == 405


@pytest.mark.django_db
def test_readyz_is_ok_when_database_answers(client):
    response = client.get("/readyz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "checks": {"database": "ok"}}


def test_readyz_is_503_and_hides_details_when_database_fails(client, caplog):
    with mock.patch("core.views.connection") as conn:
        conn.cursor.side_effect = OperationalError("password authentication failed")
        response = client.get("/readyz")
    assert response.status_code == 503
    assert response.json() == {"status": "unavailable", "checks": {"database": "error"}}
    assert "password" not in response.content.decode()  # details are logged, not returned
    assert "Readiness check failed" in caplog.text
