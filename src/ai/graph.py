from src.db import load_curriculum

def get_completed_credits(course_data, completed):
    """
    Calculate how many credits the student has completed.
    """

    return sum(
        course_data[code]["credits"]
        for code in completed
        if code in course_data
    )


def prerequisites_satisfied(course_code, prerequisite_groups, completed):
    """
    Check whether all prerequisite groups for a course are satisfied.

    Different groups = AND
    Courses inside one group = OR

    Example:

    [
        {"A"},
        {"B", "C"}
    ]

    means:

    A AND (B OR C)
    """

    groups = prerequisite_groups.get(course_code, [])

    for group in groups:

        # At least one course from this group must be completed
        if not any(option in completed for option in group):
            return False

    return True


def course_rules_satisfied(
    course_code,
    course_data,
    course_rules,
    completed
):
    """
    Check special course rules.

    Example:
    Thesis 1 requires at least 100 completed credits.
    """

    rules = course_rules.get(course_code)

    # No special rules
    if rules is None:
        return True

    completed_credits = get_completed_credits(
        course_data,
        completed
    )

    minimum_credits = rules.get(
        "minimum_completed_credits",
        0
    )

    return completed_credits >= minimum_credits


def is_course_eligible(
    course_code,
    prerequisite_groups,
    course_data,
    course_rules,
    completed
):
    """
    Check whether one course can currently be taken.
    """

    # Already completed
    if course_code in completed:
        return False

    # Normal prerequisites
    if not prerequisites_satisfied(
        course_code,
        prerequisite_groups,
        completed
    ):
        return False

    # Special rules
    if not course_rules_satisfied(
        course_code,
        course_data,
        course_rules,
        completed
    ):
        return False

    return True


def get_eligible_courses(
    prerequisite_groups,
    course_data,
    course_rules,
    completed
):
    """
    Return all courses the student is currently eligible to take.
    """

    eligible = []

    for course_code in course_data:

        if is_course_eligible(
            course_code,
            prerequisite_groups,
            course_data,
            course_rules,
            completed
        ):
            eligible.append(course_code)

    return eligible


def build_dependency_graph(prerequisite_groups):
    """
    Build a simple dependency graph for visualization
    and cycle checking.

    OR alternatives are all represented as possible edges.
    """

    graph = {
        course: set()
        for course in prerequisite_groups
    }

    for course, groups in prerequisite_groups.items():

        for group in groups:

            for prerequisite in group:
                graph[course].add(prerequisite)

                # Make sure prerequisite also exists as a node
                if prerequisite not in graph:
                    graph[prerequisite] = set()

    return graph


def has_cycle(prerequisite_groups):
    """
    Detect cycles in the prerequisite dependency graph.
    """

    graph = build_dependency_graph(prerequisite_groups)

    visited = set()
    visiting = set()

    def dfs(course):

        if course in visiting:
            return True

        if course in visited:
            return False

        visiting.add(course)

        for prerequisite in graph.get(course, set()):

            if dfs(prerequisite):
                return True

        visiting.remove(course)
        visited.add(course)

        return False

    for course in graph:

        if dfs(course):
            return True

    return False


def topological_sort(prerequisite_groups):
    """
    Return a topological ordering of the prerequisite graph.

    Mainly useful for validation and visualization.
    """

    graph = build_dependency_graph(prerequisite_groups)

    if has_cycle(prerequisite_groups):
        raise ValueError(
            "Cannot perform topological sort: "
            "prerequisite graph contains a cycle."
        )

    visited = set()
    order = []

    def dfs(course):

        if course in visited:
            return

        visited.add(course)

        for prerequisite in graph.get(course, set()):
            dfs(prerequisite)

        order.append(course)

    for course in graph:
        dfs(course)

    return order


# ------------------------------------------------------------
# Quick tests
# ------------------------------------------------------------

if __name__ == "__main__":

    from src.db import load_curriculum

    curriculum = load_curriculum()

    course_data = curriculum["courses"]
    prerequisites = curriculum["prerequisites"]
    course_rules = curriculum["course_rules"]

    completed = {
        "INBMA0101-24",
        "INBMA0104-24",
        "INBMA0105-24"
    }

    print("Completed:")
    for code in completed:
        print(code)

    print(
        "\nCompleted credits:",
        get_completed_credits(
            course_data,
            completed
        )
    )

    print("\nEligible courses:")

    eligible = get_eligible_courses(
        prerequisites,
        course_data,
        course_rules,
        completed
    )

    for code in eligible:
        print(
            code,
            "-",
            course_data[code]["name"]
        )

    print(
        "\nCycle detected:",
        has_cycle(prerequisites)
    )