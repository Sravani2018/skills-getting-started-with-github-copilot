from urllib.parse import quote

from fastapi.testclient import TestClient

from src import app as app_module


client = TestClient(app_module.app)


def test_unregister_participant_from_activity():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    app_module.activities[activity_name]["participants"] = [email, "daniel@mergington.edu"]

    response = client.delete(
        f"/activities/{quote(activity_name)}/participants/{quote(email)}"
    )

    assert response.status_code == 200
    assert email not in app_module.activities[activity_name]["participants"]
    assert "daniel@mergington.edu" in app_module.activities[activity_name]["participants"]
