from collections import deque

def meetings_overlap(meeting1, meeting2):
    if meeting1["day_of_week"] != meeting2["day_of_week"]:
        return False

    return (
        meeting1["start_time"] < meeting2["end_time"]
        and meeting2["start_time"] < meeting1["end_time"]
    )


def sections_overlap(section1, section2):
    for meeting1 in section1["meetings"]:
        for meeting2 in section2["meetings"]:
            if meetings_overlap(meeting1, meeting2):
                return True

    return False


def values_conflict(value1, value2):
    if isinstance(value1, dict) and isinstance(value2, dict):
        return sections_overlap(value1, value2)

    return value1 == value2


def is_consistent(course, value, assignment, neighbors):
    for other_course, other_value in assignment.items():
        if other_course in neighbors.get(course, set()):
            if values_conflict(value, other_value):
                return False

    return True


def select_unassigned_course(assignment, courses):
    for course in courses:
        if course not in assignment:
            return course

    return None


def select_unassigned_course_mrv(assignment, courses, domains, neighbors):
    min_count = float("inf")
    selected_course = None

    for course in courses:
        if course in assignment:
            continue

        valid_count = 0

        for value in domains[course]:
            if is_consistent(course, value, assignment, neighbors):
                valid_count += 1

        if valid_count < min_count:
            min_count = valid_count
            selected_course = course

    return selected_course


def unassigned_degree(course, assignment, neighbors):
    degree = 0

    for neighbor in neighbors.get(course, set()):
        if neighbor not in assignment:
            degree += 1

    return degree


def select_unassigned_course_mrv_degree(
    assignment,
    courses,
    domains,
    neighbors
):
    min_count = float("inf")
    max_degree = float("-inf")
    selected_course = None

    for course in courses:
        if course in assignment:
            continue

        valid_count = 0

        for value in domains[course]:
            if is_consistent(course, value, assignment, neighbors):
                valid_count += 1

        degree = unassigned_degree(course, assignment, neighbors)

        if valid_count < min_count:
            min_count = valid_count
            max_degree = degree
            selected_course = course

        elif valid_count == min_count:
            if degree > max_degree:
                max_degree = degree
                selected_course = course

    return selected_course


def backtrack(assignment, courses, domains, neighbors, stats):
    stats["calls"] += 1

    if len(assignment) == len(courses):
        return assignment

    course = select_unassigned_course(assignment, courses)

    for value in domains[course]:
        if is_consistent(course, value, assignment, neighbors):
            assignment[course] = value

            result = backtrack(
                assignment,
                courses,
                domains,
                neighbors,
                stats
            )

            if result is not None:
                return result

            del assignment[course]
            stats["backtracks"] += 1

    return None


def backtrack_mrv(assignment, courses, domains, neighbors, stats):
    stats["calls"] += 1

    if len(assignment) == len(courses):
        return assignment

    course = select_unassigned_course_mrv(
        assignment,
        courses,
        domains,
        neighbors
    )

    for value in domains[course]:
        if is_consistent(course, value, assignment, neighbors):
            assignment[course] = value

            result = backtrack_mrv(
                assignment,
                courses,
                domains,
                neighbors,
                stats
            )

            if result is not None:
                return result

            del assignment[course]
            stats["backtracks"] += 1

    return None


def backtrack_mrv_degree(
    assignment,
    courses,
    domains,
    neighbors,
    stats
):
    stats["calls"] += 1

    if len(assignment) == len(courses):
        return assignment

    course = select_unassigned_course_mrv_degree(
        assignment,
        courses,
        domains,
        neighbors
    )

    for value in domains[course]:
        if is_consistent(course, value, assignment, neighbors):
            assignment[course] = value

            result = backtrack_mrv_degree(
                assignment,
                courses,
                domains,
                neighbors,
                stats
            )

            if result is not None:
                return result

            del assignment[course]
            stats["backtracks"] += 1

    return None


def revise(x, y, domains):
    revised = False

    for x_value in domains[x].copy():
        supported = False

        for y_value in domains[y]:
            if not values_conflict(x_value, y_value):
                supported = True
                break

        if not supported:
            domains[x].remove(x_value)
            revised = True

    return revised


def ac3(domains, neighbors):
    queue = deque()

    for x in neighbors:
        for y in neighbors.get(x, set()):
            queue.append((x, y))

    while queue:
        x, y = queue.popleft()

        if revise(x, y, domains):
            if len(domains[x]) == 0:
                return False

            for z in neighbors.get(x, set()):
                if z != y:
                    queue.append((z, x))

    return True


def backtrack_mrv_degree_ac3(
    assignment,
    courses,
    domains,
    neighbors,
    stats
):
    stats["calls"] += 1

    if len(assignment) == len(courses):
        return assignment

    course = select_unassigned_course_mrv_degree(
        assignment,
        courses,
        domains,
        neighbors
    )

    for value in domains[course]:
        if is_consistent(course, value, assignment, neighbors):
            assignment[course] = value

            new_domains = {
                c: values.copy()
                for c, values in domains.items()
            }

            new_domains[course] = [value]

            if ac3(new_domains, neighbors):
                result = backtrack_mrv_degree_ac3(
                    assignment,
                    courses,
                    new_domains,
                    neighbors,
                    stats
                )

                if result is not None:
                    return result

            del assignment[course]
            stats["backtracks"] += 1

    return None

def build_neighbors(courses, domains):
    neighbors = {
        course: set()
        for course in courses
    }

    for i in range(len(courses)):
        for j in range(i + 1, len(courses)):
            course1 = courses[i]
            course2 = courses[j]

            conflict_possible = False

            for section1 in domains[course1]:
                for section2 in domains[course2]:
                    if sections_overlap(section1, section2):
                        conflict_possible = True
                        break

                if conflict_possible:
                    break

            if conflict_possible:
                neighbors[course1].add(course2)
                neighbors[course2].add(course1)

    return neighbors


def generate_timetable(section_data, courses):
    domains = {}

    for course in courses:
        if course not in section_data:
            raise ValueError(f"No section data found for {course}")

        if not section_data[course]:
            raise ValueError(f"No sections available for {course}")

        domains[course] = section_data[course].copy()

    neighbors = build_neighbors(courses, domains)

    stats = {
        "calls": 0,
        "backtracks": 0
    }

    solution = backtrack_mrv_degree_ac3(
        assignment={},
        courses=courses,
        domains=domains,
        neighbors=neighbors,
        stats=stats
    )

    return solution, stats, neighbors