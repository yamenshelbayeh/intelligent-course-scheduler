from src.db import get_prerequisite_graph


def has_cycle(graph):
    visited = set()
    visiting = set()

    def dfs(course):

        if course in visiting:
            return True

        if course in visited:
            return False

        visiting.add(course)

        for child in graph[course]:
            if dfs(child):
                return True

        visiting.remove(course)
        visited.add(course)

        return False

    for course in graph:
        if dfs(course):
            return True

    return False


def topological_sort(graph):
    if has_cycle(graph):
        raise ValueError("Cannot topologically sort a cyclic graph.")

    visited = set()
    order = []

    def dfs(course):

        if course in visited:
            return

        visited.add(course)

        for child in graph[course]:
            dfs(child)

        order.append(course)

    for course in graph:
        dfs(course)

    return order


def get_eligible_courses(graph, completed):
    eligible = []

    for course in graph:
        if course not in completed:
            if all(child in completed for child in graph[course]):
                eligible.append(course)

    return eligible