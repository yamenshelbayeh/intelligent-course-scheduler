from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Course Scheduler API is running"
    }

def test_advisor_valid_request():
    response = client.post(
        "/advisor",
        json={
            "completed": ["CSE101", "MATH101"]
        }
    )
    assert response.status_code == 200

    data = response.json()

    assert data["completed"] == ["CSE101", "MATH101"]

    assert "CSE102" in data["eligible"]

    assert len(data["recommendations"]) > 0

def test_advisor_invalid_course():
    response = client.post(
        "/advisor",
        json={
            "completed": ["CSE101", "FAKE999"]
        }
    )

    assert response.status_code == 400

def test_degree_plan_impossible_constraints():
    response = client.post(
        "/degree-plan",
        json={
            "completed": [],
            "max_credits": 4,
            "max_difficulty": 10
        }
    )

    assert response.status_code == 422

def test_timetable_empty_courses():
    response = client.post(
        "/timetable",
        json={
            "courses": []
        }
    )

    assert response.status_code == 400

def test_timetable_invalid_course():
    response = client.post(
        "/timetable",
        json={
            "courses": ["CSE101", "FAKE999"]
        }
    )

    assert response.status_code == 400

def test_timetable_duplicate_courses():
    response = client.post(
        "/timetable",
        json={
            "courses": ["CSE101", "CSE101"]
        }
    )

    assert response.status_code == 400

def test_degree_plan_valid_request():
    response = client.post(
        "/degree-plan",
        json={
            "completed": ["CSE101", "MATH101"],
            "max_credits": 15,
            "max_difficulty": 10
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "plan" in data
    assert "expanded_states" in data
    assert len(data["plan"]) > 0

def test_timetable_valid_request():
    response = client.post(
        "/timetable",
        json={
            "courses": [
                "CSE101",
                "MATH101",
                "MATH201"
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "timetable" in data
    assert "stats" in data

    assert "CSE101" in data["timetable"]
    assert "MATH101" in data["timetable"]
    assert "MATH201" in data["timetable"]

    assert data["stats"]["calls"] > 0

def test_full_plan_valid_request():
    response = client.post(
        "/full-plan",
        json={
            "completed": ["CSE101", "MATH101"],
            "max_credits": 15,
            "max_difficulty": 10
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "advisor" in data
    assert "degree_plan" in data
    assert "degree_timetables" in data
    assert "expanded_states" in data

    assert len(data["degree_plan"]) > 0
    assert len(data["degree_timetables"]) == len(data["degree_plan"])


def test_full_plan_invalid_course():
    response = client.post(
        "/full-plan",
        json={
            "completed": ["FAKE999"],
            "max_credits": 15,
            "max_difficulty": 10
        }
    )

    assert response.status_code == 400


def test_full_plan_impossible_constraints():
    response = client.post(
        "/full-plan",
        json={
            "completed": [],
            "max_credits": 4,
            "max_difficulty": 10
        }
    )

    assert response.status_code == 422
