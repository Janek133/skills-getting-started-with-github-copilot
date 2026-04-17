from fastapi import status


def test_get_activities(client):
    response = client.get("/activities")

    assert response.status_code == status.HTTP_200_OK
    assert "Chess Club" in response.json()
    assert response.json()["Chess Club"]["max_participants"] == 12


def test_root_redirects_to_static(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert response.headers["location"] == "/static/index.html"


def test_signup_for_activity(client):
    activity_name = "Science Club"
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in client.get("/activities").json()[activity_name]["participants"]


def test_duplicate_signup_returns_400(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Student already signed up"


def test_unregister_for_activity(client):
    activity_name = "Gym Class"
    email = "john@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_unregister_missing_student_returns_400(client):
    activity_name = "Programming Class"
    email = "missingstudent@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Student not registered for this activity"


def test_signup_for_missing_activity_returns_404(client):
    response = client.post("/activities/Nonexistent/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Activity not found"


def test_unregister_for_missing_activity_returns_404(client):
    response = client.delete("/activities/Nonexistent/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Activity not found"
