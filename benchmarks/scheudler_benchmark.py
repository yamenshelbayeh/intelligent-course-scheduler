from src.ai.scheduler import backtrack_mrv_degree, backtrack_mrv, backtrack_mrv_degree, backtrack_mrv_degree_ac3, backtrack
from time import perf_counter


RUNS = 1000


COURSES = [
    "H",
    "G",
    "F",
    "D",
    "A",
    "B",
    "E",
    "C",
]


DOMAINS = {
    "A": ["1", "2", "3"],
    "B": ["3", "1", "2"],
    "C": ["2", "1"],
    "D": ["2", "3"],
    "E": ["2", "3", "1"],
    "F": ["3", "1", "2"],
    "G": ["3", "2"],
    "H": ["3", "2", "1"],
}


NEIGHBORS = {
    "A": {"C", "D", "F", "G", "H"},
    "B": {"C", "E", "G"},
    "C": {"A", "B", "E"},
    "D": {"A", "E"},
    "E": {"B", "C", "D", "F", "H"},
    "F": {"A", "E", "H"},
    "G": {"A", "B"},
    "H": {"A", "E", "F"},
}


SOLVERS = [
    ("Backtracking", backtrack),
    ("MRV", backtrack_mrv),
    ("MRV + Degree", backtrack_mrv_degree),
    ("MRV + Degree + AC-3", backtrack_mrv_degree_ac3),
]


def copy_domains():
    return {
        course: values.copy()
        for course, values in DOMAINS.items()
    }


def run_once(solver):
    stats = {
        "calls": 0,
        "backtracks": 0,
    }

    solution = solver(
        assignment={},
        courses=COURSES,
        domains=copy_domains(),
        neighbors=NEIGHBORS,
        stats=stats,
    )

    return solution, stats


def benchmark_solver(solver):
    start = perf_counter()

    for _ in range(RUNS):
        solver(
            assignment={},
            courses=COURSES,
            domains=copy_domains(),
            neighbors=NEIGHBORS,
            stats={
                "calls": 0,
                "backtracks": 0,
            },
        )

    end = perf_counter()

    total_time = end - start
    average_ms = (total_time / RUNS) * 1000

    return average_ms


def main():
    print("CSP SCHEDULER BENCHMARK")
    print("=" * 75)
    print(f"Runs per algorithm: {RUNS}")
    print()

    print(
        f"{'Algorithm':<25}"
        f"{'Calls':>10}"
        f"{'Backtracks':>15}"
        f"{'Avg Time (ms)':>18}"
    )

    print("-" * 75)

    for name, solver in SOLVERS:
        solution, stats = run_once(solver)

        if solution is None:
            print(f"{name:<25} No solution")
            continue

        average_ms = benchmark_solver(solver)

        print(
            f"{name:<25}"
            f"{stats['calls']:>10}"
            f"{stats['backtracks']:>15}"
            f"{average_ms:>18.4f}"
        )


if __name__ == "__main__":
    main()