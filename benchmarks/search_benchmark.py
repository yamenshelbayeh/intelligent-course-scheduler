from time import perf_counter

from src.ai.pathfinder import (
    a_star_degree_plan,
    heuristic,
    zero_heuristic,
)
from src.db import get_prerequisite_graph, get_course_data


def build_large_test_problem():
    graph = {
        "C01": [],
        "C02": [],
        "C03": [],
        "C04": [],

        "C05": ["C01"],
        "C06": ["C01"],
        "C07": ["C02"],
        "C08": ["C03"],
        "C09": ["C03", "C04"],

        "C10": ["C05", "C07"],
        "C11": ["C06"],
        "C12": ["C07", "C08"],
        "C13": ["C09"],

        "C14": ["C10", "C11"],
        "C15": ["C11", "C12"],
        "C16": ["C12", "C13"],

        "C17": ["C14", "C15"],
        "C18": ["C15", "C16"],

        "C19": ["C17"],
        "C20": ["C18", "C19"],
    }

    course_data = {}

    for i, course in enumerate(graph):
        course_data[course] = {
            "credits": 5,
            "difficulty": 2 + (i % 4)
        }

    return graph, course_data


def benchmark_algorithm(
    graph,
    course_data,
    heuristic_fn,
    runs=1000
):
    completed = set()

    start = perf_counter()

    for _ in range(runs):
        plan, expanded_states = a_star_degree_plan(
            graph,
            completed,
            course_data,
            max_credits=15,
            max_difficulty=10,
            heuristic_fn=heuristic_fn
        )

    end = perf_counter()

    average_runtime = (end - start) / runs

    return plan, expanded_states, average_runtime


def print_results(name, plan, expanded_states, runtime):
    print(name)
    print("Semesters:", len(plan))
    print("Expanded states:", expanded_states)
    print(f"Average runtime: {runtime * 1000:.4f} ms")
    print()


def main():
    runs = 1000

    # --------------------------------
    # 10-course database benchmark
    # --------------------------------

    print("=== 10-COURSE DATABASE GRAPH ===")
    print()

    graph = get_prerequisite_graph()
    course_data = get_course_data()

    a_star_plan, a_star_expanded, a_star_runtime = benchmark_algorithm(
        graph,
        course_data,
        heuristic,
        runs
    )

    ucs_plan, ucs_expanded, ucs_runtime = benchmark_algorithm(
        graph,
        course_data,
        zero_heuristic,
        runs
    )

    print_results(
        "A*",
        a_star_plan,
        a_star_expanded,
        a_star_runtime
    )

    print_results(
        "UCS",
        ucs_plan,
        ucs_expanded,
        ucs_runtime
    )

    # --------------------------------
    # 20-course synthetic benchmark
    # --------------------------------

    print("=== 20-COURSE SYNTHETIC GRAPH ===")
    print()

    graph, course_data = build_large_test_problem()

    a_star_plan, a_star_expanded, a_star_runtime = benchmark_algorithm(
        graph,
        course_data,
        heuristic,
        runs
    )

    ucs_plan, ucs_expanded, ucs_runtime = benchmark_algorithm(
        graph,
        course_data,
        zero_heuristic,
        runs
    )

    print_results(
        "A*",
        a_star_plan,
        a_star_expanded,
        a_star_runtime
    )

    print_results(
        "UCS",
        ucs_plan,
        ucs_expanded,
        ucs_runtime
    )


if __name__ == "__main__":
    main()