from datetime import time
from src.ai.scheduler import (
    is_consistent,
    select_unassigned_course_mrv,
    unassigned_degree,
    select_unassigned_course_mrv_degree,
    revise,
    ac3,
    backtrack,
    backtrack_mrv,
    backtrack_mrv_degree,
    backtrack_mrv_degree_ac3,
    meetings_overlap
)

def test_is_consistent_detects_conflict():
    neighbors = {
        "A": {"B"},
        "B": {"A"}
    }

    assignment = {
        "A": "Mon"
    }

    assert is_consistent(
        "B",
        "Mon",
        assignment,
        neighbors
    ) is False


def test_is_consistent_allows_non_neighbor():
    neighbors = {
        "A": {"B"},
        "B": {"A"},
        "C": set()
    }

    assignment = {
        "A": "Mon"
    }

    assert is_consistent(
        "C",
        "Mon",
        assignment,
        neighbors
    ) is True


def test_mrv_selects_smallest_domain():
    courses = ["A", "B", "C"]

    domains = {
        "A": ["1", "2", "3"],
        "B": ["1"],
        "C": ["1", "2"]
    }

    neighbors = {
        "A": {"B", "C"},
        "B": {"A", "C"},
        "C": {"A", "B"}
    }

    assignment = {}

    selected = select_unassigned_course_mrv(
        assignment,
        courses,
        domains,
        neighbors
    )

    assert selected == "B"


def test_unassigned_degree():
    neighbors = {
        "A": {"B", "C", "D"},
        "B": {"A"},
        "C": {"A"},
        "D": {"A"}
    }

    assignment = {
        "B": "1"
    }

    assert unassigned_degree(
        "A",
        assignment,
        neighbors
    ) == 2


def test_degree_breaks_mrv_tie():
    courses = ["B", "C", "A", "D"]

    domains = {
        "A": ["1", "2"],
        "B": ["1", "2"],
        "C": ["1", "2"],
        "D": ["1", "2"]
    }

    neighbors = {
        "A": {"B", "C", "D"},
        "B": {"A"},
        "C": {"A"},
        "D": {"A"}
    }

    assignment = {}

    selected = select_unassigned_course_mrv_degree(
        assignment,
        courses,
        domains,
        neighbors
    )

    assert selected == "A"

def test_revise_removes_unsupported_value():
    domains = {
        "A": ["Mon"],
        "B": ["Mon", "Tue"]
    }

    revised = revise("B", "A", domains)

    assert revised is True
    assert domains["B"] == ["Tue"]


def test_ac3_propagates_constraints():
    domains = {
        "A": ["Mon"],
        "B": ["Mon", "Tue"],
        "C": ["Tue", "Wed"]
    }

    neighbors = {
        "A": {"B"},
        "B": {"A", "C"},
        "C": {"B"}
    }

    result = ac3(domains, neighbors)

    assert result is True
    assert domains["A"] == ["Mon"]
    assert domains["B"] == ["Tue"]
    assert domains["C"] == ["Wed"]


def test_ac3_detects_impossible_problem():
    domains = {
        "A": ["Mon"],
        "B": ["Mon"]
    }

    neighbors = {
        "A": {"B"},
        "B": {"A"}
    }

    result = ac3(domains, neighbors)

    assert result is False

def assert_valid_solution(solution, courses, neighbors):
    assert solution is not None
    assert set(solution.keys()) == set(courses)

    for course in courses:
        for neighbor in neighbors[course]:
            assert solution[course] != solution[neighbor]

def test_plain_backtracking_finds_valid_solution():
    courses = ["A", "B", "C", "D"]

    domains = {
        "A": ["1", "2", "3"],
        "B": ["1", "2", "3"],
        "C": ["1", "2", "3"],
        "D": ["1", "2", "3"]
    }

    neighbors = {
        "A": {"B", "C"},
        "B": {"A", "C"},
        "C": {"A", "B", "D"},
        "D": {"C"}
    }

    stats = {
        "calls": 0,
        "backtracks": 0
    }

    solution = backtrack(
        {},
        courses,
        domains,
        neighbors,
        stats
    )

    assert_valid_solution(solution, courses, neighbors)


def test_mrv_finds_valid_solution():
    courses = ["A", "B", "C", "D"]

    domains = {
        "A": ["1", "2", "3"],
        "B": ["1", "2", "3"],
        "C": ["1", "2", "3"],
        "D": ["1", "2", "3"]
    }

    neighbors = {
        "A": {"B", "C"},
        "B": {"A", "C"},
        "C": {"A", "B", "D"},
        "D": {"C"}
    }

    stats = {
        "calls": 0,
        "backtracks": 0
    }

    solution = backtrack_mrv(
        {},
        courses,
        domains,
        neighbors,
        stats
    )

    assert_valid_solution(solution, courses, neighbors)

def test_mrv_degree_finds_valid_solution():
    courses = ["A", "B", "C", "D"]

    domains = {
        "A": ["1", "2", "3"],
        "B": ["1", "2", "3"],
        "C": ["1", "2", "3"],
        "D": ["1", "2", "3"]
    }

    neighbors = {
        "A": {"B", "C"},
        "B": {"A", "C"},
        "C": {"A", "B", "D"},
        "D": {"C"}
    }

    stats = {
        "calls": 0,
        "backtracks": 0
    }

    solution = backtrack_mrv_degree(
        {},
        courses,
        domains,
        neighbors,
        stats
    )

    assert_valid_solution(solution, courses, neighbors)


def test_mrv_degree_ac3_finds_valid_solution():
    courses = ["A", "B", "C", "D"]

    domains = {
        "A": ["1", "2", "3"],
        "B": ["1", "2", "3"],
        "C": ["1", "2", "3"],
        "D": ["1", "2", "3"]
    }

    neighbors = {
        "A": {"B", "C"},
        "B": {"A", "C"},
        "C": {"A", "B", "D"},
        "D": {"C"}
    }

    stats = {
        "calls": 0,
        "backtracks": 0
    }

    solution = backtrack_mrv_degree_ac3(
        {},
        courses,
        domains,
        neighbors,
        stats
    )

    assert_valid_solution(solution, courses, neighbors)

def test_solver_returns_none_for_unsatisfiable_problem():
    courses = ["A", "B", "C"]

    domains = {
        "A": ["1", "2"],
        "B": ["1", "2"],
        "C": ["1", "2"]
    }

    neighbors = {
        "A": {"B", "C"},
        "B": {"A", "C"},
        "C": {"A", "B"}
    }

    stats = {
        "calls": 0,
        "backtracks": 0
    }

    solution = backtrack_mrv_degree_ac3(
        {},
        courses,
        domains,
        neighbors,
        stats
    )

    assert solution is None

def test_meetings_overlap():
    meeting1 = {
        "day_of_week": 1,
        "start_time": time(9, 0),
        "end_time": time(10, 30)
    }

    meeting2 = {
        "day_of_week": 1,
        "start_time": time(10, 0),
        "end_time": time(11, 30)
    }

    assert meetings_overlap(meeting1, meeting2)


def test_meetings_do_not_overlap_different_days():
    meeting1 = {
        "day_of_week": 1,
        "start_time": time(9, 0),
        "end_time": time(10, 30)
    }

    meeting2 = {
        "day_of_week": 2,
        "start_time": time(9, 0),
        "end_time": time(10, 30)
    }

    assert not meetings_overlap(meeting1, meeting2)


def test_back_to_back_meetings_do_not_overlap():
    meeting1 = {
        "day_of_week": 1,
        "start_time": time(9, 0),
        "end_time": time(10, 30)
    }

    meeting2 = {
        "day_of_week": 1,
        "start_time": time(10, 30),
        "end_time": time(12, 0)
    }

    assert not meetings_overlap(meeting1, meeting2)
