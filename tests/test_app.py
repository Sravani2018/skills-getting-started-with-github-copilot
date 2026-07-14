from urllib.parse import quote

from fastapi.testclient import TestClient

from src import app as app_module


client = TestClient(app_module.app)

def test_register_participant_to_activity():
    activity_name = "Basketball_Club"
    email = "somerandomemail@xyz"
    app_module.activities[activity_name]["participants"] = [[email, "noah@mergington.edu"]]
    response = client.post(f"/activities/{quote(activity_name)}/participants/{quote(email)}")

    assert response.status_code == 200
    assert email in app_module.activities[activity_name]["participants"]
    assert response.json() == {"message" : f"Signed up {email} for {activity_name}"}

def test_reject_duplicate_registration():
    activity_name = "Drama_Club"
    email = "amelia@mergington.edu"
    # app_module.activities[activity_name]["participants"] = [email]

    response = client.post(
        f"/activities/{quote(activity_name)}/participants/{quote(email)}"
    )

    assert response.status_code == 400
    assert response.json() == {"detail" : f"Student already signed up for {activity_name}"}



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
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}
