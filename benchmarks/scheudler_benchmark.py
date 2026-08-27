from src.ai.scheduler import backtrack_mrv_degree, backtrack_mrv, backtrack_mrv_degree, backtrack_mrv_degree_ac3, \
    backtrack


def main():
    courses = ["H", "G", "F", "D", "A", "B", "E", "C"]

    domains = {
        "A": ["1", "2", "3"],
        "B": ["3", "1", "2"],
        "C": ["2", "1"],
        "D": ["2", "3"],
        "E": ["2", "3", "1"],
        "F": ["3", "1", "2"],
        "G": ["3", "2"],
        "H": ["3", "2", "1"]
    }

    neighbors = {
        "A": {"C", "D", "F", "G", "H"},
        "B": {"C", "E", "G"},
        "C": {"A", "B", "E"},
        "D": {"A", "E"},
        "E": {"B", "C", "D", "F", "H"},
        "F": {"A", "E", "H"},
        "G": {"A", "B"},
        "H": {"A", "E", "F"}
    }

    plain_stats = {"calls": 0, "backtracks": 0}
    mrv_stats = {"calls": 0, "backtracks": 0}
    degree_stats = {"calls": 0, "backtracks": 0}
    ac3_stats = {"calls": 0, "backtracks": 0}

    plain_solution = backtrack(
        {},
        courses,
        domains,
        neighbors,
        plain_stats
    )

    mrv_solution = backtrack_mrv(
        {},
        courses,
        domains,
        neighbors,
        mrv_stats
    )

    degree_solution = backtrack_mrv_degree(
        {},
        courses,
        domains,
        neighbors,
        degree_stats
    )

    ac3_solution = backtrack_mrv_degree_ac3(
        {},
        courses,
        domains,
        neighbors,
        ac3_stats
    )

    print("Plain Backtracking")
    print("Solution:", plain_solution)
    print("Calls:", plain_stats["calls"])
    print("Backtracks:", plain_stats["backtracks"])

    print()

    print("MRV")
    print("Solution:", mrv_solution)
    print("Calls:", mrv_stats["calls"])
    print("Backtracks:", mrv_stats["backtracks"])

    print()

    print("MRV + Degree")
    print("Solution:", degree_solution)
    print("Calls:", degree_stats["calls"])
    print("Backtracks:", degree_stats["backtracks"])

    print()

    print("MRV + Degree + AC-3")
    print("Solution:", ac3_solution)
    print("Calls:", ac3_stats["calls"])
    print("Backtracks:", ac3_stats["backtracks"])


if __name__ == "__main__":
    main()