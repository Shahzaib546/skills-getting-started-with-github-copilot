from pathlib import Path
import sys

# Make sure src is importable when running pytest from repo root
src_path = str(Path(__file__).parent.parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from app import activities


def test_get_activities(client):
    # Arrange: no-op (activities pre-populated)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_adds_participant_and_prevents_duplicate(client):
    # Arrange
    activity = "Art Club"
    email = "tester@mergington.edu"
    initial = len(activities[activity]["participants"])

    # Act - first signup
    resp1 = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert first signup succeeded
    assert resp1.status_code == 200
    assert email in activities[activity]["participants"]
    assert len(activities[activity]["participants"]) == initial + 1

    # Act - duplicate signup
    resp2 = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert duplicate rejected
    assert resp2.status_code == 400
    assert "already" in resp2.json().get("detail", "").lower()


def test_remove_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "daniel@mergington.edu"
    initial = len(activities[activity]["participants"])

    # Act
    resp = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]
    assert len(activities[activity]["participants"]) == initial - 1
