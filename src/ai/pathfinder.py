import math
import heapq

from itertools import combinations, count
from src.ai.graph import get_eligible_courses


def semester_load(action, course_data):
    total_credits = 0
    for course in action:
        total_credits += course_data[course]["credits"]
    return total_credits


def semester_difficulty(action, course_data):
    total_difficulty = 0

    for course in action:
        total_difficulty += course_data[course]["difficulty"]

    return total_difficulty


def is_goal(state, graph):
    return frozenset(graph.keys()).issubset(state)


def longest_remaining_chain(state, graph):
    memo = {}

    def dfs(course):
        if course in state:
            return 0

        if course in memo:
            return memo[course]

        unfinished_prereqs = [
            prereq
            for prereq in graph.get(course, [])
            if prereq not in state
        ]

        if not unfinished_prereqs:
            memo[course] = 1
        else:
            memo[course] = 1 + max(
                dfs(prereq)
                for prereq in unfinished_prereqs
            )

        return memo[course]

    remaining_courses = [
        course
        for course in graph
        if course not in state
    ]

    if not remaining_courses:
        return 0

    return max(
        dfs(course)
        for course in remaining_courses
    )


def heuristic(state, graph, course_data, max_credits):
    remaining_credits = 0

    for course in graph:
        if course not in state:
            remaining_credits += course_data[course]["credits"]

    credit_semesters = math.ceil(remaining_credits / max_credits)
    prerequisite_semesters = longest_remaining_chain(state, graph)

    return max(credit_semesters, prerequisite_semesters)


def zero_heuristic(state, graph, course_data, max_credits):
    return 0


def get_actions(state, graph, course_data, max_credits, max_difficulty):
    eligible_courses = get_eligible_courses(graph, state)
    actions = []

    for size in range(1, len(eligible_courses) + 1):
        for semester in combinations(eligible_courses, size):
            total_credits = 0
            total_difficulty = 0

            for course in semester:
                total_credits += course_data[course]["credits"]
                total_difficulty += course_data[course]["difficulty"]

            if (total_credits <= max_credits
                    and total_difficulty <= max_difficulty):
                actions.append(semester)

    return actions


def transition(state, action):
    return state | frozenset(action)


def a_star_degree_plan(graph, completed, course_data, max_credits, max_difficulty, heuristic_fn=heuristic):
    if not completed:
        completed = set()

    start_state = frozenset(completed)
    frontier = []
    tie_breaker = count()

    start_heuristic = heuristic_fn(start_state, graph, course_data, max_credits)
    heapq.heappush(
        frontier,
        (
            start_heuristic,
            0,
            0,
            0,
            next(tie_breaker),
            start_state,
            []
        )
    )
    best_cost = {
        start_state: (0, 0)
    }

    expanded_states = 0
    best_goal_path = None
    best_goal_g = None
    best_goal_balance = None

    while frontier:

        f, g, balance, _, _, state, path = heapq.heappop(frontier)

        if (g, balance) != best_cost.get(state):
            continue

        expanded_states += 1

        if best_goal_g is not None and f > best_goal_g:
            break

        if is_goal(state, graph):

            if (best_goal_path is None or
                    (g, balance) < (best_goal_g, best_goal_balance)):
                best_goal_path = path
                best_goal_g = g
                best_goal_balance = balance

            continue

        actions = get_actions(state, graph, course_data, max_credits, max_difficulty)

        for action in actions:
            new_state = transition(state, action)
            semester_penalty = semester_difficulty(action, course_data) ** 2
            new_balance_cost = balance + semester_penalty
            new_g = g + 1
            new_cost = (new_g, new_balance_cost)
            if new_state not in best_cost or new_cost < best_cost[new_state]:
                best_cost[new_state] = new_cost

                new_h = heuristic_fn(new_state, graph, course_data, max_credits)
                new_f = new_h + new_g

                new_path = path + [action]
                heapq.heappush(frontier,
                               (new_f, new_g, new_balance_cost, -semester_load(action, course_data), next(tie_breaker),
                                new_state, new_path))

    if best_goal_path is not None:
        return best_goal_path, expanded_states

    raise ValueError(
        "No valid degree plan could be found."
    )
