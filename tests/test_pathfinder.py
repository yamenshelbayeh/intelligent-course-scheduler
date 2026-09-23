import pytest

from src.db import load_curriculum

from src.ai.graph import (
    prerequisites_satisfied,
    course_rules_satisfied
)

from src.ai.pathfinder import (
    a_star_degree_plan,
    heuristic,
    remaining_planned_credits,
    differentiated_credits,
    is_goal,
    validate_plan,
    course_available_in_semester
)


# ============================================================
# SHARED CURRICULUM
# ============================================================

@pytest.fixture(scope="session")
def curriculum():
    """
    Load the real University of Debrecen
    Computer Science Engineering curriculum.
    """

    return load_curriculum()


@pytest.fixture(scope="session")
def course_data(curriculum):
    return curriculum["courses"]


@pytest.fixture(scope="session")
def prerequisites(curriculum):
    return curriculum["prerequisites"]


@pytest.fixture(scope="session")
def degree_requirements(curriculum):
    return curriculum["degree_requirements"]


@pytest.fixture(scope="session")
def course_rules(curriculum):
    return curriculum["course_rules"]


# Run A* only once for all tests.
# This keeps pytest much faster.
@pytest.fixture(scope="session")
def generated_plan(
    course_data,
    prerequisites,
    degree_requirements,
    course_rules
):
    return a_star_degree_plan(
        prerequisite_groups=prerequisites,
        course_data=course_data,
        course_rules=course_rules,
        degree_requirements=degree_requirements,
        completed=set(),
        start_semester=1,
        max_credits=30
    )


# ============================================================
# DATABASE / CURRICULUM TESTS
# ============================================================

def test_course_count(course_data):
    assert len(course_data) == 58


def test_degree_total_is_210(degree_requirements):

    total = sum(
        data["required_credits"]
        for data in degree_requirements.values()
        if data["counts_toward_degree"]
    )

    assert total == 210


def test_professional_training_not_double_counted(
    degree_requirements
):
    training = degree_requirements[
        "PROFESSIONAL_TRAINING"
    ]

    assert training["required_credits"] == 12
    assert training["counts_toward_degree"] is False


# ============================================================
# PREREQUISITE TESTS
# ============================================================

def test_ai_has_three_required_prerequisite_groups(
    prerequisites
):
    groups = prerequisites["INBMA0526-24"]

    assert len(groups) == 3

    assert {"INBMA0106-24"} in groups
    assert {"INBMA0207-17"} in groups
    assert {"INBMA0211-21"} in groups


def test_or_prerequisite_structure(prerequisites):
    """
    Development of Embedded Systems requires:

    Embedded Systems
    AND
    (Microcontrollers OR Programmable Logic Devices)
    """

    groups = prerequisites["INBMA9940-17"]

    assert {"INBMA0528-17"} in groups

    assert {
        "INBMA9937-17",
        "INBMA9939-17"
    } in groups


def test_or_prerequisite_accepts_microcontrollers(
    prerequisites
):
    completed = {
        "INBMA0528-17",
        "INBMA9937-17"
    }

    assert prerequisites_satisfied(
        "INBMA9940-17",
        prerequisites,
        completed
    )


def test_or_prerequisite_accepts_programmable_logic(
    prerequisites
):
    completed = {
        "INBMA0528-17",
        "INBMA9939-17"
    }

    assert prerequisites_satisfied(
        "INBMA9940-17",
        prerequisites,
        completed
    )


def test_or_prerequisite_rejects_missing_second_group(
    prerequisites
):
    completed = {
        "INBMA0528-17"
    }

    assert not prerequisites_satisfied(
        "INBMA9940-17",
        prerequisites,
        completed
    )


# ============================================================
# THESIS RULE TESTS
# ============================================================

def test_thesis_requires_100_credits(course_rules):

    assert "INBMA0636-21" in course_rules

    assert (
        course_rules["INBMA0636-21"]
        ["minimum_completed_credits"]
        == 100
    )


def test_thesis_rule_rejects_less_than_100():

    course_data = {
        "A": {
            "credits": 90
        }
    }

    rules = {
        "THESIS": {
            "minimum_completed_credits": 100
        }
    }

    completed = {"A"}

    assert not course_rules_satisfied(
        "THESIS",
        course_data,
        rules,
        completed
    )


def test_thesis_rule_accepts_100_or_more():

    course_data = {
        "A": {
            "credits": 60
        },
        "B": {
            "credits": 40
        }
    }

    rules = {
        "THESIS": {
            "minimum_completed_credits": 100
        }
    }

    completed = {"A", "B"}

    assert course_rules_satisfied(
        "THESIS",
        course_data,
        rules,
        completed
    )


# ============================================================
# SEMESTER AVAILABILITY TESTS
# ============================================================

def test_period_1_course_available_in_odd_semester(
    course_data
):
    assert course_available_in_semester(
        "INBMA0101-24",
        course_data,
        semester=1
    )

    assert not course_available_in_semester(
        "INBMA0101-24",
        course_data,
        semester=2
    )


def test_period_2_course_available_in_even_semester(
    course_data
):
    assert course_available_in_semester(
        "INBMA0211-21",
        course_data,
        semester=2
    )

    assert not course_available_in_semester(
        "INBMA0211-21",
        course_data,
        semester=3
    )


# ============================================================
# HEURISTIC TESTS
# ============================================================

def test_initial_remaining_structured_credits(
    course_data,
    degree_requirements
):
    result = remaining_planned_credits(
        frozenset(),
        course_data,
        degree_requirements
    )

    assert result == 198


def test_initial_heuristic_is_seven(
    course_data,
    degree_requirements
):
    result = heuristic(
        frozenset(),
        course_data,
        degree_requirements,
        max_credits=30
    )

    assert result == 7


def test_goal_false_for_empty_state(
    course_data,
    degree_requirements
):
    assert not is_goal(
        frozenset(),
        course_data,
        degree_requirements
    )


# ============================================================
# A* TESTS
# ============================================================

def test_a_star_finds_plan(generated_plan):

    plan, expanded_states, initial_h = generated_plan

    assert plan is not None
    assert len(plan) > 0
    assert expanded_states > 0
    assert initial_h == 7


def test_a_star_finishes_in_seven_semesters(
    generated_plan
):
    plan, _, _ = generated_plan

    assert len(plan) == 7


def test_a_star_respects_credit_limit(
    generated_plan,
    course_data
):
    plan, _, _ = generated_plan

    for semester in plan:

        credits = sum(
            course_data[code]["credits"]
            for code in semester
        )

        assert credits <= 30


def test_a_star_does_not_repeat_courses(
    generated_plan
):
    plan, _, _ = generated_plan

    planned_courses = [
        code
        for semester in plan
        for code in semester
    ]

    assert len(planned_courses) == len(
        set(planned_courses)
    )


def test_a_star_plans_198_structured_credits(
    generated_plan,
    course_data
):
    plan, _, _ = generated_plan

    total = sum(
        course_data[code]["credits"]
        for semester in plan
        for code in semester
    )

    assert total == 198


def test_a_star_completes_30_differentiated_credits(
    generated_plan,
    course_data
):
    plan, _, _ = generated_plan

    completed = {
        code
        for semester in plan
        for code in semester
    }

    credits = differentiated_credits(
        completed,
        course_data
    )

    assert credits >= 30


def test_professional_training_is_in_plan(
    generated_plan
):
    plan, _, _ = generated_plan

    planned_courses = {
        code
        for semester in plan
        for code in semester
    }

    assert "INBMA9997-21" in planned_courses


# ============================================================
# FULL PLAN VALIDATION
# ============================================================

def test_generated_plan_is_valid(
    generated_plan,
    prerequisites,
    course_data,
    course_rules,
    degree_requirements
):
    plan, _, _ = generated_plan

    valid, errors = validate_plan(
        plan=plan,
        prerequisite_groups=prerequisites,
        course_data=course_data,
        course_rules=course_rules,
        degree_requirements=degree_requirements,
        max_credits=30
    )

    assert valid, (
        "Generated plan failed validation:\n"
        + "\n".join(errors)
    )