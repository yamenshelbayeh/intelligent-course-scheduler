from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == (
        "Intelligent Course Scheduler API is running"
    )

    assert (
        data["curriculum"]
        == "University of Debrecen - Computer Science Engineering BSc"
    )


def test_curriculum():
    response = client.get("/curriculum")

    assert response.status_code == 200

    data = response.json()

    assert data["course_count"] == 58
    assert "courses" in data
    assert "degree_requirements" in data


def test_curriculum_contains_ai_course():
    response = client.get("/curriculum")

    data = response.json()

    courses = data["courses"]

    assert "INBMA0526-24" in courses

    assert (
        courses["INBMA0526-24"]["name"]
        == "Introduction into Artificial Intelligence"
    )


def test_degree_plan_valid_request():
    response = client.post(
        "/degree-plan",
        json={
            "completed": [],
            "max_credits": 30,
            "start_semester": 1
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "degree_plan" in data
    assert "statistics" in data
    assert "validation" in data

    assert len(data["degree_plan"]) == 7

    assert (
        data["statistics"]["planned_credits"]
        == 198
    )

    assert (
        data["statistics"]["free_choice_credits_remaining"]
        == 12
    )

    assert data["validation"]["valid"] is True


def test_degree_plan_has_210_total_credits():
    response = client.post(
        "/degree-plan",
        json={
            "completed": [],
            "max_credits": 30,
            "start_semester": 1
        }
    )

    assert response.status_code == 200

    data = response.json()

    structured = data["statistics"]["planned_credits"]
    free_choice = data["statistics"][
        "free_choice_credits_remaining"
    ]

    assert structured + free_choice == 210


def test_degree_plan_respects_credit_limit():
    response = client.post(
        "/degree-plan",
        json={
            "completed": [],
            "max_credits": 30,
            "start_semester": 1
        }
    )

    assert response.status_code == 200

    data = response.json()

    for semester in data["degree_plan"]:
        assert semester["total_credits"] <= 30


def test_degree_plan_contains_professional_training():
    response = client.post(
        "/degree-plan",
        json={
            "completed": [],
            "max_credits": 30,
            "start_semester": 1
        }
    )

    assert response.status_code == 200

    data = response.json()

    planned_codes = {
        course["code"]
        for semester in data["degree_plan"]
        for course in semester["courses"]
    }

    assert "INBMA9997-21" in planned_codes


def test_degree_plan_invalid_course():
    response = client.post(
        "/degree-plan",
        json={
            "completed": ["FAKE999"],
            "max_credits": 30,
            "start_semester": 1
        }
    )

    assert response.status_code == 400

    assert "Unknown courses" in response.json()["detail"]


def test_degree_plan_impossible_credit_limit():

    response = client.post(
        "/degree-plan",
        json={
            "completed": [],
            "max_credits": 2,
            "start_semester": 1
        }
    )

    assert response.status_code == 422


def test_degree_plan_rejects_invalid_start_semester():
    response = client.post(
        "/degree-plan",
        json={
            "completed": [],
            "max_credits": 30,
            "start_semester": 8
        }
    )

    assert response.status_code == 422

def test_completed_course_not_planned_again():
    completed = [
        "INBMA0101-24",
        "INBMA0102-24",
        "INBMA0104-24",
        "INBMA0105-24",
        "INBMA0106-24",
        "INBMA0120-24"
    ]

    response = client.post(
        "/degree-plan",
        json={
            "completed": completed,
            "max_credits": 30,
            "start_semester": 2
        }
    )

    assert response.status_code == 200

    data = response.json()

    planned_codes = {
        course["code"]
        for semester in data["degree_plan"]
        for course in semester["courses"]
    }

    for code in completed:
        assert code not in planned_codes


def test_api_returns_search_statistics():
    response = client.post(
        "/degree-plan",
        json={
            "completed": [],
            "max_credits": 30,
            "start_semester": 1
        }
    )

    assert response.status_code == 200

    stats = response.json()["statistics"]

    assert stats["expanded_states"] > 0
    assert stats["initial_heuristic"] == 7
    assert stats["total_semesters"] == 7