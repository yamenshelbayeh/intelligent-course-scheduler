from src.ai.advisor import explain_blocked_course, get_future_unlocks, explain_recommendation, \
    recommend_eligible_courses, get_prerequisite_chain, build_advisor_report, get_next_semester_advice

GRAPH = {
    "CSE101": [],
    "CSE102": ["CSE101"],
    "CSE201": ["CSE102"],
    "CSE301": ["CSE102"],
    "CSE202": ["CSE201", "MATH201"],
    "CSE302": ["CSE202", "STAT201"],
    "CSE303": ["CSE302"],
    "MATH201": [],
    "STAT201": [],
}

COURSE_DATA = {
    "CSE101": {"credits": 5, "difficulty": 2},
    "CSE102": {"credits": 5, "difficulty": 3},
    "CSE201": {"credits": 5, "difficulty": 3},
    "CSE202": {"credits": 5, "difficulty": 4},
    "CSE301": {"credits": 5, "difficulty": 3},
    "CSE302": {"credits": 5, "difficulty": 4},
    "CSE303": {"credits": 5, "difficulty": 5},
    "MATH201": {"credits": 5, "difficulty": 3},
    "STAT201": {"credits": 5, "difficulty": 3},
}

def test_explain_completed_course():
    completed = {"CSE101"}

    result = explain_blocked_course(
        "CSE101",
        GRAPH,
        completed
    )

    assert result == "CSE101 is already completed."


def test_explain_eligible_course():
    completed = {"CSE101"}

    result = explain_blocked_course(
        "CSE102",
        GRAPH,
        completed
    )

    assert result == (
        "CSE102 is not blocked. "
        "You are eligible to take it."
    )


def test_explain_blocked_course():
    completed = set()

    result = explain_blocked_course(
        "CSE102",
        GRAPH,
        completed
    )

    assert result == (
        "CSE102 is blocked because you still need to complete: "
        "CSE101."
    )


def test_explain_invalid_course():
    completed = set()

    result = explain_blocked_course(
        "ABC999",
        GRAPH,
        completed
    )

    assert result == (
        "ABC999 was not found in the course catalog."
    )


def test_future_unlocks_cse102():
    completed = {"CSE101", "MATH101"}

    result = get_future_unlocks(
        "CSE102",
        GRAPH,
        completed
    )

    assert result == [
        "CSE201",
        "CSE202",
        "CSE301",
        "CSE302",
        "CSE303",
    ]


def test_future_unlocks_math201():
    completed = set()

    result = get_future_unlocks(
        "MATH201",
        GRAPH,
        completed
    )

    assert result == [
        "CSE202",
        "CSE302",
        "CSE303",
    ]


def test_future_unlocks_stat201():
    completed = set()

    result = get_future_unlocks(
        "STAT201",
        GRAPH,
        completed
    )

    assert result == [
        "CSE302",
        "CSE303",
    ]


def test_future_unlocks_leaf_course():
    completed = set()

    result = get_future_unlocks(
        "CSE303",
        GRAPH,
        completed
    )

    assert result == []


def test_future_unlocks_through_completed_course():
    graph = {
        "A": [],
        "B": ["A"],
        "C": ["B"],
    }

    completed = {"B"}

    result = get_future_unlocks(
        "A",
        graph,
        completed
    )

    assert result == ["C"]


def test_explain_recommendation_with_multiple_unlocks():
    recommendation = {
        "course": "CSE102",
        "credits": 5,
        "difficulty": 3,
        "unlocks": ["CSE201", "CSE301"],
        "unlock_count": 2,
        "future_unlocks": [
            "CSE201",
            "CSE202",
            "CSE301",
            "CSE302",
            "CSE303",
        ],
        "future_unlock_count": 5,
    }

    result = explain_recommendation(recommendation)

    assert "CSE102 is a strong next choice" in result
    assert "directly unlocks 2 courses" in result
    assert "CSE201, CSE301" in result
    assert "5 unfinished courses" in result
    assert "difficulty is 3/5" in result


def test_explain_recommendation_singular_course():
    recommendation = {
        "course": "MATH201",
        "credits": 5,
        "difficulty": 3,
        "unlocks": ["CSE202"],
        "unlock_count": 1,
        "future_unlocks": [
            "CSE202",
            "CSE302",
            "CSE303",
        ],
        "future_unlock_count": 3,
    }

    result = explain_recommendation(recommendation)

    assert "directly unlocks 1 course:" in result
    assert "1 courses" not in result


def test_explain_recommendation_no_unlocks():
    recommendation = {
        "course": "CSE303",
        "credits": 5,
        "difficulty": 5,
        "unlocks": [],
        "unlock_count": 0,
        "future_unlocks": [],
        "future_unlock_count": 0,
    }

    result = explain_recommendation(recommendation)

    assert result == (
        "CSE303 is currently eligible. "
        "It does not directly unlock another unfinished course. "
        "Its difficulty is 5/5."
    )


def test_recommend_eligible_courses_ranking():
    completed = {"CSE101"}
    recommendations = recommend_eligible_courses(GRAPH,completed, COURSE_DATA)

    courses = [
        recommendation["course"] for recommendation in recommendations
    ]

    assert courses == [
        "CSE102",
        "MATH201",
        "STAT201"
    ]

    assert recommendations[0]["future_unlock_count"] == 5
    assert recommendations[1]["future_unlock_count"] == 3
    assert recommendations[2]["future_unlock_count"] == 2


def test_prerequisite_chain_cse303():
    completed = set()

    result = get_prerequisite_chain(
        "CSE303",
        GRAPH,
        completed
    )

    assert result == [
        "CSE101",
        "CSE102",
        "CSE201",
        "CSE202",
        "CSE302",
        "MATH201",
        "STAT201",
    ]


def test_prerequisite_chain_with_completed_courses():
    completed = {
        "CSE101",
        "CSE102",
    }

    result = get_prerequisite_chain(
        "CSE303",
        GRAPH,
        completed
    )

    assert result == [
        "CSE201",
        "CSE202",
        "CSE302",
        "MATH201",
        "STAT201",
    ]


def test_prerequisite_chain_eligible_course():
    completed = {"CSE101"}

    result = get_prerequisite_chain(
        "CSE102",
        GRAPH,
        completed
    )

    assert result == []


def test_prerequisite_chain_course_without_prerequisites():
    completed = set()

    result = get_prerequisite_chain(
        "MATH201",
        GRAPH,
        completed
    )

    assert result == []


def test_build_advisor_report():
    completed = {"CSE101"}

    report = build_advisor_report(
        GRAPH,
        completed,
        COURSE_DATA
    )

    assert report["completed"] == ["CSE101"]

    assert report["eligible"] == [
        "CSE102",
        "MATH201",
        "STAT201",
    ]

    assert len(report["recommendations"]) == 3

    assert report["recommendations"][0]["course"] == "CSE102"
    assert report["recommendations"][0]["future_unlock_count"] == 5
    assert "explanation" in report["recommendations"][0]

    assert "CSE201" in report["blocked"]

    assert report["blocked"]["CSE201"]["missing_prerequisites"] == [
        "CSE102"
    ]

    assert report["blocked"]["CSE201"]["prerequisite_chain"] == [
        "CSE102"
    ]

    assert "explanation" in report["blocked"]["CSE201"]


def test_get_next_semester_advice():
    degree_plan = [
        ("CSE102", "MATH201"),
        ("CSE201", "STAT201"),
    ]

    advisor_report = {
        "recommendations": [
            {
                "course": "CSE102",
                "difficulty": 3,
            },
            {
                "course": "MATH201",
                "difficulty": 3,
            },
            {
                "course": "STAT201",
                "difficulty": 3,
            },
        ]
    }

    result = get_next_semester_advice(
        degree_plan,
        advisor_report
    )

    assert result["courses"] == [
        "CSE102",
        "MATH201",
    ]

    assert len(result["recommendations"]) == 2

    assert result["recommendations"][0]["course"] == "CSE102"
    assert result["recommendations"][1]["course"] == "MATH201"


def test_get_next_semester_advice_empty_plan():
    result = get_next_semester_advice(
        [],
        {"recommendations": []}
    )

    assert result == {
        "courses": [],
        "recommendations": []
    }
