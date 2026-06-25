from http import HTTPStatus

from src import app as app_module


def test_root_redirects_to_static_index(client):
    # Arrange: prepare a client fixture
    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == HTTPStatus.TEMPORARY_REDIRECT
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activity_names = set(app_module.activities.keys())

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert set(response.json().keys()) == expected_activity_names


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Math Olympiad"
    email = "new_student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_duplicate_participant_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Cooking Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_success(client):
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}
    assert email not in app_module.activities[activity_name]["participants"]


def test_remove_unknown_participant_returns_404(client):
    # Arrange
    activity_name = "Gym Class"
    email = "nonexistent@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "Participant not found in this activity"


def test_remove_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Cooking Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "Activity not found"
