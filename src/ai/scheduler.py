from collections import deque

def is_consistent(course, time_slot, assignment, neighbors):
    for c, time in assignment.items():
        if c in neighbors[course] and time_slot == time:
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

        for time in domains[course]:
            if is_consistent(course, time, assignment, neighbors):
                valid_count += 1

        if valid_count < min_count:
            min_count = valid_count
            selected_course = course

    return selected_course
def unassigned_degree(course, assignment, neighbors):
    degree = 0

    for neighbor in neighbors[course]:
        if neighbor not in assignment:
            degree += 1

    return degree
def select_unassigned_course_mrv_degree(assignment, courses, domains, neighbors):
    min_count = float("inf")
    max_degree = float("-inf")
    selected_course = None

    for course in courses:
        if course in assignment:
            continue

        valid_count = 0

        for time in domains[course]:
            if is_consistent(course, time, assignment, neighbors):
                valid_count += 1

        degree = unassigned_degree(course, assignment, neighbors)

        if valid_count < min_count:
            min_count = valid_count
            selected_course = course
            max_degree = degree
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

    for time in domains[course]:
        if is_consistent(course, time_slot=time, assignment=assignment, neighbors=neighbors):
            assignment[course] = time
            result = backtrack(assignment, courses, domains, neighbors, stats)

            if result is not None:
                return result

            del assignment[course]
            stats["backtracks"] += 1

    return None
def backtrack_mrv(assignment, courses, domains, neighbors, stats):
    stats["calls"] += 1
    if len(assignment) == len(courses):
        return assignment

    course = select_unassigned_course_mrv(assignment, courses, domains, neighbors)

    for time in domains[course]:
        if is_consistent(course, time_slot=time, assignment=assignment, neighbors=neighbors):
            assignment[course] = time
            result = backtrack_mrv(assignment, courses, domains, neighbors, stats)

            if result is not None:
                return result

            del assignment[course]
            stats["backtracks"] += 1

    return None
def backtrack_mrv_degree(assignment, courses, domains, neighbors, stats):
    stats["calls"] += 1
    if len(assignment) == len(courses):
        return assignment

    course = select_unassigned_course_mrv_degree(assignment, courses, domains, neighbors)

    for time in domains[course]:
        if is_consistent(course, time_slot=time, assignment=assignment, neighbors=neighbors):
            assignment[course] = time
            result = backtrack_mrv_degree(assignment, courses, domains, neighbors, stats)

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
            if x_value != y_value:
                supported = True
                break

        if not supported:
            domains[x].remove(x_value)
            revised = True

    return revised
def ac3(domains, neighbors):
    queue = deque()
    for x in neighbors:
        for y in neighbors[x]:
            queue.append((x, y))

    while queue:
        x,y = queue.popleft()

        if revise(x,y,domains):

            if len(domains[x]) == 0:
                return False

            for z in neighbors[x]:
                if z != y:
                    queue.append((z, x))

    return True
def backtrack_mrv_degree_ac3(assignment, courses, domains, neighbors, stats):
    stats["calls"] += 1
    if len(assignment) == len(courses):
        return assignment

    course = select_unassigned_course_mrv_degree(assignment, courses, domains, neighbors)

    for time in domains[course]:
        if is_consistent(course, time_slot=time, assignment=assignment, neighbors=neighbors):
            assignment[course] = time

            new_domains = {
                c: values.copy()
                for c, values in domains.items()
            }

            new_domains[course] = [time]

            if ac3(new_domains, neighbors):
                result = backtrack_mrv_degree_ac3(assignment, courses, new_domains, neighbors, stats)

                if result is not None:
                    return result

            del assignment[course]
            stats["backtracks"] += 1

    return None