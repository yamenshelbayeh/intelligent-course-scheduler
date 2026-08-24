import pytest

from src.ai.pathfinder import (
    a_star_degree_plan,
    heuristic,
    longest_remaining_chain,
    semester_load,
    semester_difficulty,
)


# --------------------------------------------------
# Shared test data
# --------------------------------------------------

@pytest.fixture
def graph():
    return {
        "CSE101": [],
        "CSE102": ["CSE101"],
        "CSE201": ["CSE102"],
        "CSE202": ["CSE201", "MATH201"],
        "CSE301": ["CSE102"],
        "CSE302": ["CSE202", "STAT201"],
        "CSE303": ["CSE302"],
        "MATH101": [],
        "MATH201": [],
        "STAT201": []
    }


@pytest.fixture
def course_data():
    return {
        "CSE101": {"credits": 5, "difficulty": 2},
        "CSE102": {"credits": 5, "difficulty": 3},
        "CSE201": {"credits": 5, "difficulty": 3},
        "CSE202": {"credits": 5, "difficulty": 4},
        "CSE301": {"credits": 5, "difficulty": 3},
        "CSE302": {"credits": 5, "difficulty": 4},
        "CSE303": {"credits": 5, "difficulty": 5},
        "MATH101": {"credits": 5, "difficulty": 3},
        "MATH201": {"credits": 5, "difficulty": 3},
        "STAT201": {"credits": 5, "difficulty": 3}
    }


# --------------------------------------------------
# longest_remaining_chain tests
# --------------------------------------------------

def test_longest_chain_no_prerequisites():
    graph = {
        "A": [],
        "B": [],
        "C": []
    }

    result = longest_remaining_chain(
        frozenset(),
        graph
    )

    assert result == 1


def test_longest_chain_simple_chain():
    graph = {
        "A": [],
        "B": ["A"],
        "C": ["B"],
        "D": ["C"]
    }

    result = longest_remaining_chain(
        frozenset(),
        graph
    )

    assert result == 4


def test_longest_chain_with_completed_courses():
    graph = {
        "A": [],
        "B": ["A"],
        "C": ["B"],
        "D": ["C"]
    }

    completed = frozenset({"A", "B"})

    result = longest_remaining_chain(
        completed,
        graph
    )

    assert result == 2


def test_longest_chain_branching():
    graph = {
        "A": [],
        "B": [],
        "C": ["A"],
        "D": ["B"],
        "E": ["C", "D"]
    }

    result = longest_remaining_chain(
        frozenset(),
        graph
    )

    assert result == 3


def test_longest_chain_all_completed():
    graph = {
        "A": [],
        "B": ["A"],
        "C": ["B"]
    }

    completed = frozenset({"A", "B", "C"})

    result = longest_remaining_chain(
        completed,
        graph
    )

    assert result == 0



# --------------------------------------------------
# heuristic tests
# --------------------------------------------------

def test_heuristic_credit_bound():
    graph = {
        "A": [],
        "B": [],
        "C": [],
        "D": []
    }

    course_data = {
        "A": {"credits": 5},
        "B": {"credits": 5},
        "C": {"credits": 5},
        "D": {"credits": 5}
    }

    result = heuristic(
        frozenset(),
        graph,
        course_data,
        max_credits=10
    )

    # 20 remaining credits / 10 per semester
    assert result == 2


def test_heuristic_prerequisite_bound():
    graph = {
        "A": [],
        "B": ["A"],
        "C": ["B"],
        "D": ["C"]
    }

    course_data = {
        "A": {"credits": 5},
        "B": {"credits": 5},
        "C": {"credits": 5},
        "D": {"credits": 5}
    }

    result = heuristic(
        frozenset(),
        graph,
        course_data,
        max_credits=20
    )

    # Credits could fit in one semester,
    # but prerequisites require four semesters.
    assert result == 4


def test_heuristic_with_completed_courses():
    graph = {
        "A": [],
        "B": ["A"],
        "C": ["B"],
        "D": ["C"]
    }

    course_data = {
        "A": {"credits": 5},
        "B": {"credits": 5},
        "C": {"credits": 5},
        "D": {"credits": 5}
    }

    completed = frozenset({"A", "B"})

    result = heuristic(
        completed,
        graph,
        course_data,
        max_credits=20
    )

    assert result == 2


def test_heuristic_goal_state(graph, course_data):
    completed = frozenset(graph.keys())

    result = heuristic(
        completed,
        graph,
        course_data,
        max_credits=15
    )

    assert result == 0


# --------------------------------------------------
# A* tests
# --------------------------------------------------

def test_a_star_finds_plan(graph, course_data):
    plan, expanded_states = a_star_degree_plan(
        graph,
        completed=set(),
        course_data=course_data,
        max_credits=15,
        max_difficulty=12
    )

    assert plan is not None
    assert len(plan) > 0
    assert expanded_states > 0


def test_a_star_finishes_in_six_semesters(graph, course_data):
    plan, _ = a_star_degree_plan(
        graph,
        completed=set(),
        course_data=course_data,
        max_credits=15,
        max_difficulty=12
    )

    # The longest prerequisite chain requires six semesters.
    assert len(plan) == 6


def test_a_star_completes_every_course(graph, course_data):
    plan, _ = a_star_degree_plan(
        graph,
        completed=set(),
        course_data=course_data,
        max_credits=15,
        max_difficulty=12
    )

    planned_courses = {
        course
        for semester in plan
        for course in semester
    }

    assert planned_courses == set(graph.keys())


def test_a_star_does_not_repeat_courses(graph, course_data):
    plan, _ = a_star_degree_plan(
        graph,
        completed=set(),
        course_data=course_data,
        max_credits=15,
        max_difficulty=12
    )

    planned_courses = [
        course
        for semester in plan
        for course in semester
    ]

    assert len(planned_courses) == len(set(planned_courses))


def test_a_star_respects_credit_limit(graph, course_data):
    max_credits = 15

    plan, _ = a_star_degree_plan(
        graph,
        completed=set(),
        course_data=course_data,
        max_credits=max_credits,
        max_difficulty=12
    )

    for semester in plan:
        assert semester_load(
            semester,
            course_data
        ) <= max_credits


def test_a_star_respects_difficulty_limit(graph, course_data):
    max_difficulty = 12

    plan, _ = a_star_degree_plan(
        graph,
        completed=set(),
        course_data=course_data,
        max_credits=15,
        max_difficulty=max_difficulty
    )

    for semester in plan:
        assert semester_difficulty(
            semester,
            course_data
        ) <= max_difficulty


def test_a_star_respects_prerequisites(graph, course_data):
    plan, _ = a_star_degree_plan(
        graph,
        completed=set(),
        course_data=course_data,
        max_credits=15,
        max_difficulty=12
    )

    completed = set()

    for semester in plan:

        for course in semester:
            prerequisites = graph[course]

            assert all(
                prerequisite in completed
                for prerequisite in prerequisites
            )

        completed.update(semester)


def test_a_star_with_completed_courses(graph, course_data):
    already_completed = {
        "CSE101",
        "MATH101"
    }

    plan, _ = a_star_degree_plan(
        graph,
        completed=already_completed,
        course_data=course_data,
        max_credits=15,
        max_difficulty=12
    )

    planned_courses = {
        course
        for semester in plan
        for course in semester
    }

    # Already completed courses should not appear again.
    assert "CSE101" not in planned_courses
    assert "MATH101" not in planned_courses

    # Everything else should still be planned.
    expected = set(graph.keys()) - already_completed

    assert planned_courses == expected


def test_a_star_raises_when_no_plan_possible():
    graph = {
        "A": []
    }

    course_data = {
        "A": {
            "credits": 5,
            "difficulty": 10
        }
    }

    # A itself has difficulty 10, but the maximum allowed
    # semester difficulty is only 5.
    with pytest.raises(ValueError):
        a_star_degree_plan(
            graph,
            completed=set(),
            course_data=course_data,
            max_credits=15,
            max_difficulty=5
        )