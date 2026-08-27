from src.ai.scheduler import backtrack_mrv_degree, backtrack_mrv, backtrack_mrv_degree, backtrack_mrv_degree_ac3, backtrack
from time import perf_counter


RUNS = 1000


RUNS = 1000


SOLVERS = [
    ("Backtracking", backtrack),
    ("MRV", backtrack_mrv),
    ("MRV + Degree", backtrack_mrv_degree),
    ("MRV + Degree + AC-3", backtrack_mrv_degree_ac3),
]


SCENARIOS = {
    "Medium": {
        "courses": [
            "E",
            "D",
            "C",
            "B",
            "A",
        ],

        "domains": {
            "A": ["1", "2", "3"],
            "B": ["1", "2"],
            "C": ["2", "3"],
            "D": ["1", "3"],
            "E": ["1", "2", "3"],
        },

        "neighbors": {
            "A": {"B", "C", "D"},
            "B": {"A", "C", "E"},
            "C": {"A", "B", "D"},
            "D": {"A", "C", "E"},
            "E": {"B", "D"},
        },
    },

    "Hard": {
        "courses": [
            "H",
            "G",
            "F",
            "D",
            "A",
            "B",
            "E",
            "C",
        ],

        "domains": {
            "A": ["1", "2", "3"],
            "B": ["3", "1", "2"],
            "C": ["2", "1"],
            "D": ["2", "3"],
            "E": ["2", "3", "1"],
            "F": ["3", "1", "2"],
            "G": ["3", "2"],
            "H": ["3", "2", "1"],
        },

        "neighbors": {
            "A": {"C", "D", "F", "G", "H"},
            "B": {"C", "E", "G"},
            "C": {"A", "B", "E"},
            "D": {"A", "E"},
            "E": {"B", "C", "D", "F", "H"},
            "F": {"A", "E", "H"},
            "G": {"A", "B"},
            "H": {"A", "E", "F"},
        },
    },

    "Impossible": {
        "courses": [
            "A",
            "B",
            "C",
        ],

        "domains": {
            "A": ["1", "2"],
            "B": ["1", "2"],
            "C": ["1", "2"],
        },

        "neighbors": {
            "A": {"B", "C"},
            "B": {"A", "C"},
            "C": {"A", "B"},
        },
    },
}


def copy_domains(domains):
    return {
        course: values.copy()
        for course, values in domains.items()
    }


def run_once(solver, courses, domains, neighbors):
    stats = {
        "calls": 0,
        "backtracks": 0,
    }

    solution = solver(
        assignment={},
        courses=courses,
        domains=copy_domains(domains),
        neighbors=neighbors,
        stats=stats,
    )

    return solution, stats


def benchmark_solver(
    solver,
    courses,
    domains,
    neighbors
):
    start = perf_counter()

    for _ in range(RUNS):
        solver(
            assignment={},
            courses=courses,
            domains=copy_domains(domains),
            neighbors=neighbors,
            stats={
                "calls": 0,
                "backtracks": 0,
            },
        )

    end = perf_counter()

    average_ms = ((end - start) / RUNS) * 1000

    return average_ms


def main():
    print("CSP SCHEDULER BENCHMARK")
    print("=" * 85)
    print(f"Runs per algorithm: {RUNS}")

    for scenario_name, scenario in SCENARIOS.items():
        courses = scenario["courses"]
        domains = scenario["domains"]
        neighbors = scenario["neighbors"]

        print()
        print(scenario_name.upper())
        print("-" * 85)

        print(
            f"{'Algorithm':<25}"
            f"{'Result':>12}"
            f"{'Calls':>10}"
            f"{'Backtracks':>15}"
            f"{'Avg Time (ms)':>18}"
        )

        print("-" * 85)

        for name, solver in SOLVERS:
            solution, stats = run_once(
                solver,
                courses,
                domains,
                neighbors
            )

            average_ms = benchmark_solver(
                solver,
                courses,
                domains,
                neighbors
            )

            result = (
                "Solved"
                if solution is not None
                else "No solution"
            )

            print(
                f"{name:<25}"
                f"{result:>12}"
                f"{stats['calls']:>10}"
                f"{stats['backtracks']:>15}"
                f"{average_ms:>18.4f}"
            )


if __name__ == "__main__":
    main()