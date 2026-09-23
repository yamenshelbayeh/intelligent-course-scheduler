import pytest

from src.db import load_curriculum

from src.ai.advisor import (
    get_missing_prerequisite_groups,
    get_blocked_courses,
    get_academic_status,
    get_course_dependents,
    get_future_unlocks,
    recommend_eligible_courses,
    explain_recommendation,
    explain_blocked_course,
    get_prerequisite_chain,
    build_advisor_report,
    get_next_semester_advice
)


# ============================================================
# SHARED CURRICULUM
# ============================================================

@pytest.fixture(scope="session")
def curriculum():
    return load_curriculum()


@pytest.fixture(scope="session")
def course_data(curriculum):
    return curriculum["courses"]


@pytest.fixture(scope="session")
def prerequisites(curriculum):
    return curriculum["prerequisites"]


@pytest.fixture(scope="session")
def course_rules(curriculum):
    return curriculum["course_rules"]


# ============================================================
# MISSING PREREQUISITES
# ============================================================

def test_ai_has_three_missing_groups(prerequisites):
    missing = get_missing_prerequisite_groups(
        "INBMA0526-24",
        prerequisites,
        completed=set()
    )

    assert len(missing) == 3

    assert ["INBMA0106-24"] in missing
    assert ["INBMA0207-17"] in missing
    assert ["INBMA0211-21"] in missing


def test_ai_prerequisites_satisfied(prerequisites):
    completed = {
        "INBMA0106-24",
        "INBMA0207-17",
        "INBMA0211-21"
    }

    missing = get_missing_prerequisite_groups(
        "INBMA0526-24",
        prerequisites,
        completed
    )

    assert missing == []


def test_or_group_accepts_one_option(prerequisites):
    completed = {
        "INBMA0528-17",
        "INBMA9937-17"
    }

    missing = get_missing_prerequisite_groups(
        "INBMA9940-17",
        prerequisites,
        completed
    )

    assert missing == []


def test_or_group_lists_both_options_when_missing(
    prerequisites
):
    completed = {
        "INBMA0528-17"
    }

    missing = get_missing_prerequisite_groups(
        "INBMA9940-17",
        prerequisites,
        completed
    )

    assert [
        "INBMA9937-17",
        "INBMA9939-17"
    ] in missing


# ============================================================
# BLOCKED / ELIGIBLE COURSES
# ============================================================

def test_completed_course_not_blocked(
    prerequisites,
    course_data,
    course_rules
):
    completed = {"INBMA0101-24"}

    blocked = get_blocked_courses(
        prerequisites,
        course_data,
        course_rules,
        completed
    )

    assert "INBMA0101-24" not in blocked


def test_ai_is_blocked_without_prerequisites(
    prerequisites,
    course_data,
    course_rules
):
    blocked = get_blocked_courses(
        prerequisites,
        course_data,
        course_rules,
        completed=set()
    )

    assert "INBMA0526-24" in blocked

    assert len(
        blocked["INBMA0526-24"][
            "missing_prerequisite_groups"
        ]
    ) == 3


def test_thesis_blocked_below_100_credits(
    prerequisites,
    course_data,
    course_rules
):
    blocked = get_blocked_courses(
        prerequisites,
        course_data,
        course_rules,
        completed=set()
    )

    thesis = blocked["INBMA0636-21"]

    assert thesis["minimum_completed_credits"] == 100


# ============================================================
# ACADEMIC STATUS
# ============================================================

def test_academic_status(
    prerequisites,
    course_data,
    course_rules
):
    completed = {"INBMA0101-24"}

    status = get_academic_status(
        prerequisites,
        course_data,
        course_rules,
        completed
    )

    assert "INBMA0101-24" in status["completed"]

    assert "eligible" in status
    assert "blocked" in status

    assert "INBMA0101-24" not in status["eligible"]
    assert "INBMA0101-24" not in status["blocked"]


# ============================================================
# DEPENDENTS / FUTURE UNLOCKS
# ============================================================

def test_course_dependents(prerequisites):
    dependents = get_course_dependents(
        prerequisites
    )

    # Programming Languages 1 is a prerequisite
    # for several later courses.
    assert "INBMA0211-21" in dependents

    assert len(
        dependents["INBMA0211-21"]
    ) > 0


def test_ai_is_dependent_on_programming_languages_1(
    prerequisites
):
    dependents = get_course_dependents(
        prerequisites
    )

    assert (
        "INBMA0526-24"
        in dependents["INBMA0211-21"]
    )


def test_future_unlocks(prerequisites):
    result = get_future_unlocks(
        "INBMA0211-21",
        prerequisites,
        completed=set()
    )

    assert "INBMA0526-24" in result

    assert len(result) > 0


def test_leaf_course_has_no_future_unlocks(
    prerequisites
):
    # Introduction to Generative AI has no course
    # depending on it in the curriculum.
    result = get_future_unlocks(
        "INBMA9964-21",
        prerequisites,
        completed=set()
    )

    assert result == []


# ============================================================
# RECOMMENDATIONS
# ============================================================

def test_recommendations_only_contain_eligible_courses(
    prerequisites,
    course_data,
    course_rules
):
    completed = set()

    status = get_academic_status(
        prerequisites,
        course_data,
        course_rules,
        completed
    )

    recommendations = recommend_eligible_courses(
        prerequisites,
        completed,
        course_data,
        course_rules
    )

    recommended_courses = {
        recommendation["course"]
        for recommendation in recommendations
    }

    assert recommended_courses == set(
        status["eligible"]
    )


def test_recommendation_has_expected_fields(
    prerequisites,
    course_data,
    course_rules
):
    recommendations = recommend_eligible_courses(
        prerequisites,
        completed=set(),
        course_data=course_data,
        course_rules=course_rules
    )

    assert len(recommendations) > 0

    recommendation = recommendations[0]

    assert "course" in recommendation
    assert "name" in recommendation
    assert "credits" in recommendation
    assert "category" in recommendation
    assert "unlocks" in recommendation
    assert "unlock_count" in recommendation
    assert "future_unlocks" in recommendation
    assert "future_unlock_count" in recommendation

    # Difficulty was part of the old toy model.
    assert "difficulty" not in recommendation


def test_recommendations_are_ranked(
    prerequisites,
    course_data,
    course_rules
):
    recommendations = recommend_eligible_courses(
        prerequisites,
        completed=set(),
        course_data=course_data,
        course_rules=course_rules
    )

    for first, second in zip(
        recommendations,
        recommendations[1:]
    ):
        first_key = (
            -first["future_unlock_count"],
            -first["unlock_count"],
            first["recommended_semester"]
            if first["recommended_semester"] is not None
            else 99,
            first["course"]
        )

        second_key = (
            -second["future_unlock_count"],
            -second["unlock_count"],
            second["recommended_semester"]
            if second["recommended_semester"] is not None
            else 99,
            second["course"]
        )

        assert first_key <= second_key


# ============================================================
# EXPLANATIONS
# ============================================================

def test_explain_completed_course(
    prerequisites,
    course_data,
    course_rules
):
    result = explain_blocked_course(
        "INBMA0101-24",
        prerequisites,
        course_data,
        course_rules,
        {"INBMA0101-24"}
    )

    assert result == (
        "INBMA0101-24 is already completed."
    )


def test_explain_invalid_course(
    prerequisites,
    course_data,
    course_rules
):
    result = explain_blocked_course(
        "FAKE999",
        prerequisites,
        course_data,
        course_rules,
        set()
    )

    assert result == (
        "FAKE999 was not found in the course catalog."
    )


def test_explain_ai_blocked(
    prerequisites,
    course_data,
    course_rules
):
    result = explain_blocked_course(
        "INBMA0526-24",
        prerequisites,
        course_data,
        course_rules,
        set()
    )

    assert "INBMA0526-24 is blocked" in result

    assert "INBMA0106-24" in result
    assert "INBMA0207-17" in result
    assert "INBMA0211-21" in result


def test_explain_or_prerequisite(
    prerequisites,
    course_data,
    course_rules
):
    completed = {
        "INBMA0528-17"
    }

    result = explain_blocked_course(
        "INBMA9940-17",
        prerequisites,
        course_data,
        course_rules,
        completed
    )

    assert "complete one of" in result
    assert "INBMA9937-17" in result
    assert "INBMA9939-17" in result


def test_explain_thesis_credit_rule(
    prerequisites,
    course_data,
    course_rules
):
    result = explain_blocked_course(
        "INBMA0636-21",
        prerequisites,
        course_data,
        course_rules,
        set()
    )

    assert "100 completed credits" in result


def test_explain_recommendation():
    recommendation = {
        "course": "TEST101",
        "name": "Test Course",
        "credits": 5,
        "category": "COMPULSORY",
        "recommended_semester": 1,
        "unlocks": ["TEST201", "TEST202"],
        "unlock_count": 2,
        "future_unlocks": [
            "TEST201",
            "TEST202",
            "TEST301"
        ],
        "future_unlock_count": 3
    }

    result = explain_recommendation(
        recommendation
    )

    assert "TEST101 - Test Course" in result
    assert "directly unlocks 2 course(s)" in result
    assert "3 unfinished course(s)" in result


# ============================================================
# PREREQUISITE CHAIN
# ============================================================

def test_ai_prerequisite_chain(prerequisites):
    result = get_prerequisite_chain(
        "INBMA0526-24",
        prerequisites,
        completed=set()
    )

    assert "INBMA0106-24" in result
    assert "INBMA0207-17" in result
    assert "INBMA0211-21" in result


def test_completed_prerequisite_removed_from_chain(
    prerequisites
):
    completed = {
        "INBMA0106-24",
        "INBMA0207-17",
        "INBMA0211-21"
    }

    result = get_prerequisite_chain(
        "INBMA0526-24",
        prerequisites,
        completed
    )

    assert result == []


# ============================================================
# FULL ADVISOR REPORT
# ============================================================

def test_build_advisor_report(
    prerequisites,
    course_data,
    course_rules
):
    completed = set()

    report = build_advisor_report(
        prerequisites,
        completed,
        course_data,
        course_rules
    )

    assert "completed" in report
    assert "eligible" in report
    assert "recommendations" in report
    assert "blocked" in report

    assert report["completed"] == []

    assert len(report["eligible"]) > 0
    assert len(report["recommendations"]) > 0
    assert len(report["blocked"]) > 0

    assert "INBMA0526-24" in report["blocked"]

    assert (
        "explanation"
        in report["blocked"]["INBMA0526-24"]
    )


# ============================================================
# NEXT SEMESTER ADVICE
# ============================================================

def test_get_next_semester_advice():
    degree_plan = [
        ("COURSE1", "COURSE2"),
        ("COURSE3",)
    ]

    advisor_report = {
        "recommendations": [
            {
                "course": "COURSE1"
            },
            {
                "course": "COURSE2"
            },
            {
                "course": "COURSE3"
            }
        ]
    }

    result = get_next_semester_advice(
        degree_plan,
        advisor_report
    )

    assert result["courses"] == [
        "COURSE1",
        "COURSE2"
    ]

    assert len(result["recommendations"]) == 2

    assert (
        result["recommendations"][0]["course"]
        == "COURSE1"
    )

    assert (
        result["recommendations"][1]["course"]
        == "COURSE2"
    )


def test_get_next_semester_advice_empty_plan():
    result = get_next_semester_advice(
        [],
        {"recommendations": []}
    )

    assert result == {
        "courses": [],
        "recommendations": []
    }