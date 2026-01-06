import importlib

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture(autouse=True)
def reset_app():
    # reload module to reset in-memory activities between tests
    importlib.reload(app_module)
    return app_module


def test_get_activities(reset_app):
    client = TestClient(reset_app.app)
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_success(reset_app):
    client = TestClient(reset_app.app)
    email = "new@mergington.edu"
    resp = client.post(f"/activities/Chess%20Club/signup?email={email}")
    assert resp.status_code == 200
    json_data = resp.json()
    assert "Signed up" in json_data["message"]

    # verify participant appears in activity
    resp2 = client.get("/activities")
    assert email in resp2.json()["Chess Club"]["participants"]


def test_signup_duplicate(reset_app):
    client = TestClient(reset_app.app)
    # michael@mergington.edu is already in Chess Club in initial data
    email = "michael@mergington.edu"
    resp = client.post(f"/activities/Chess%20Club/signup?email={email}")
    assert resp.status_code == 400


def test_signup_nonexistent_activity(reset_app):
    client = TestClient(reset_app.app)
    resp = client.post("/activities/NoSuchActivity/signup?email=test@x.com")
    assert resp.status_code == 404
