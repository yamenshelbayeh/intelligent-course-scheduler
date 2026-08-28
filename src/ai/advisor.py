from src.ai.graph import get_eligible_courses


def get_blocked_courses(graph, completed):
    blocked = {}

    for course, prerequisites in graph.items():
        if course in completed:
            continue

        missing = [
            prereq
            for prereq in prerequisites
            if prereq not in completed
        ]

        if missing:
            blocked[course] = missing

    return blocked

def get_academic_status(graph, completed):
    eligible = get_eligible_courses(graph, completed)
    blocked = get_blocked_courses(graph, completed)

    return {
        "completed": sorted(completed),
        "eligible": sorted(eligible),
        "blocked": blocked
    }

def get_course_dependents(graph):
    dependents = {
        course: []
        for course in graph
    }
    for course, prerequisites in graph.items():
        for prerequisite in prerequisites:
            dependents.setdefault(prerequisite, []).append(course)

    return dependents

def recommend_eligible_courses(graph, completed, course_data):
    eligible = get_eligible_courses(graph, completed)
    dependents = get_course_dependents(graph)

    recommendations = []

    for course in eligible:
        unlocks = [
            dependent
            for dependent in dependents.get(course, [])
            if dependent not in completed
        ]

        future_unlocks = get_future_unlocks(course, graph, completed)

        recommendations.append({
            "course": course,
            "credits": course_data[course]["credits"],
            "difficulty": course_data[course]["difficulty"],
            "unlocks": sorted(unlocks),
            "unlock_count": len(unlocks),
            "future_unlocks": future_unlocks,
            "future_unlock_count": len(future_unlocks)
        })

    recommendations.sort(
        key=lambda recommendation: (
            -recommendation["future_unlock_count"],
            -recommendation["unlock_count"],
            recommendation["difficulty"],
            recommendation["course"]
        )
    )

    return recommendations

def explain_recommendation(recommendation):
    if recommendation["unlock_count"] > 0:
        course_names = ", ".join(recommendation["unlocks"])
        future_names = ", ".join(recommendation["future_unlocks"])

        word = (
            "course"
            if recommendation["unlock_count"] == 1
            else "courses"
        )

        if recommendation["future_unlock_count"] > 0:
            return (
                f"{recommendation['course']} is a strong next choice because "
                f"it directly unlocks {recommendation['unlock_count']} {word}:\n"
                f"{course_names}.\n"
                f"\nIt is connected to {recommendation['future_unlock_count']} "
                f"unfinished courses in the future prerequisite chain:\n"
                f"{future_names}.\n"
                f"Its difficulty is {recommendation['difficulty']}/5."
            )

        return (
            f"{recommendation['course']} is a strong next choice because "
            f"it directly unlocks {recommendation['unlock_count']} {word}: "
            f"{course_names}. Its difficulty is "
            f"{recommendation['difficulty']}/5."
        )

    return (
        f"{recommendation['course']} is currently eligible. "
        f"It does not directly unlock another unfinished course. "
        f"Its difficulty is {recommendation['difficulty']}/5."
    )

def explain_blocked_course(course, graph, completed):
    if course not in graph:
        return f"{course} was not found in the course catalog."

    blocked = get_blocked_courses(graph, completed)

    if course in completed:
        return f"{course} is already completed."

    if course not in blocked:
        return f"{course} is not blocked. You are eligible to take it."

    missing = [
        prereq
        for prereq in graph.get(course, [])
        if prereq not in completed
    ]

    return (
        f"{course} is blocked because you still need to complete: "
        f"{', '.join(missing)}."
    )

def get_future_unlocks(course, graph, completed):
    dependents = get_course_dependents(graph)

    visited = set()
    future_unlocks = set()

    def dfs(current):
        for dependent in dependents.get(current, []):
            if dependent in visited:
                continue

            visited.add(dependent)

            if dependent not in completed:
                future_unlocks.add(dependent)

            dfs(dependent)

    dfs(course)

    return sorted(future_unlocks)

def get_prerequisite_chain(course, graph, completed):
    visited = set()
    prereq_chain = set()

    def dfs(current):
        for prereq in graph.get(current, []):
            if prereq in visited:
                continue

            visited.add(prereq)

            if prereq in completed:
                continue

            prereq_chain.add(prereq)
            dfs(prereq)

    dfs(course)

    return sorted(prereq_chain)

def build_advisor_report(graph, completed, course_data):
    report = []
    status = get_academic_status(graph,completed)

    recommendations = recommend_eligible_courses(graph, completed, course_data)

    recommendation_details = []
    blocked_details = {}

    for recommendation in recommendations:
        recommendation_details.append({
            **recommendation,
            "explanation": explain_recommendation(recommendation)
        })

    for course, missing in status["blocked"].items():
        blocked_details[course] = {
            "missing_prerequisites": missing,
            "prerequisite_chain": get_prerequisite_chain(course, graph, completed),
            "explanation": explain_blocked_course(course, graph, completed)
        }

    return {
        "completed": status["completed"],
        "eligible": status["eligible"],
        "recommendations": recommendation_details,
        "blocked": blocked_details
    }

def get_next_semester_advice(degree_plan, advisor_report):
    if not degree_plan:
        return {
            "courses": [],
            "recommendations": []
        }

    next_semester = list(degree_plan[0])
    next_semester_recommendations = []

    for recommendation in advisor_report["recommendations"]:
        if recommendation["course"] not in next_semester:
            continue
        next_semester_recommendations.append(recommendation)

    return {
        "courses": next_semester,
        "recommendations": next_semester_recommendations
    }