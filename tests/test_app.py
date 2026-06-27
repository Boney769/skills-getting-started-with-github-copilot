import copy
from pathlib import Path
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)


def test_remove_participant_from_activity():
    client = TestClient(app)
    activity_name = "Chess Club"
    participant_email = "michael@mergington.edu"

    assert participant_email in activities[activity_name]["participants"]

    response = client.delete(f"/activities/{activity_name}/participants/{participant_email}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {participant_email} from {activity_name}"}
    assert participant_email not in activities[activity_name]["participants"]


def test_remove_missing_participant_returns_not_found():
    client = TestClient(app)

    response = client.delete("/activities/Chess Club/participants/not-a-member@example.com")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
