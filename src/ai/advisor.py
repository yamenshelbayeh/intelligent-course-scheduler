from src.ai.graph import (
    get_eligible_courses,
    prerequisites_satisfied,
    course_rules_satisfied,
    get_completed_credits
)


def get_missing_prerequisite_groups(
    course,
    prerequisite_groups,
    completed
):
    """
    Return prerequisite groups that are not satisfied.

    Each group represents one requirement.
    Multiple courses inside the same group mean OR.
    """

    missing_groups = []

    for group in prerequisite_groups.get(course, []):

        if not any(
            option in completed
            for option in group
        ):
            missing_groups.append(sorted(group))

    return missing_groups


def get_blocked_courses(
    prerequisite_groups,
    course_data,
    course_rules,
    completed
):
    """
    Return courses that cannot currently be taken.
    """

    blocked = {}

    completed_credits = get_completed_credits(
        course_data,
        completed
    )

    for course in course_data:

        if course in completed:
            continue

        missing_groups = get_missing_prerequisite_groups(
            course,
            prerequisite_groups,
            completed
        )

        rule = course_rules.get(course)

        minimum_credits_missing = None

        if rule:
            minimum = rule["minimum_completed_credits"]

            if completed_credits < minimum:
                minimum_credits_missing = minimum

        if missing_groups or minimum_credits_missing is not None:
            blocked[course] = {
                "missing_prerequisite_groups": missing_groups,
                "minimum_completed_credits": minimum_credits_missing
            }

    return blocked


def get_academic_status(
    prerequisite_groups,
    course_data,
    course_rules,
    completed
):
    """
    Return completed, eligible and blocked courses.
    """

    eligible = get_eligible_courses(
        prerequisite_groups,
        course_data,
        course_rules,
        completed
    )

    blocked = get_blocked_courses(
        prerequisite_groups,
        course_data,
        course_rules,
        completed
    )

    return {
        "completed": sorted(completed),
        "eligible": sorted(eligible),
        "blocked": blocked
    }


def get_course_dependents(prerequisite_groups):
    """
    Build the reverse prerequisite graph.

    Example:
        Programming Languages 1 -> courses that depend on it
    """

    dependents = {
        course: []
        for course in prerequisite_groups
    }

    for course, groups in prerequisite_groups.items():

        for group in groups:

            for prerequisite in group:

                dependents.setdefault(
                    prerequisite,
                    []
                ).append(course)

    for course in dependents:
        dependents[course] = sorted(
            set(dependents[course])
        )

    return dependents


def get_future_unlocks(
    course,
    prerequisite_groups,
    completed
):
    """
    Find unfinished courses that depend directly or indirectly
    on a course.
    """

    dependents = get_course_dependents(
        prerequisite_groups
    )

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


def recommend_eligible_courses(
    prerequisite_groups,
    completed,
    course_data,
    course_rules
):
    """
    Rank currently eligible courses.

    Courses that unlock more of the curriculum are placed first.
    """

    eligible = get_eligible_courses(
        prerequisite_groups,
        course_data,
        course_rules,
        completed
    )

    dependents = get_course_dependents(
        prerequisite_groups
    )

    recommendations = []

    for course in eligible:

        direct_unlocks = [
            dependent
            for dependent in dependents.get(course, [])
            if dependent not in completed
        ]

        future_unlocks = get_future_unlocks(
            course,
            prerequisite_groups,
            completed
        )

        data = course_data[course]

        recommendations.append({
            "course": course,
            "name": data["name"],
            "credits": data["credits"],
            "category": data["category"],
            "recommended_semester": data[
                "recommended_semester"
            ],
            "unlocks": sorted(direct_unlocks),
            "unlock_count": len(direct_unlocks),
            "future_unlocks": future_unlocks,
            "future_unlock_count": len(future_unlocks)
        })

    recommendations.sort(
        key=lambda recommendation: (
            -recommendation["future_unlock_count"],
            -recommendation["unlock_count"],
            recommendation["recommended_semester"]
            if recommendation["recommended_semester"] is not None
            else 99,
            recommendation["course"]
        )
    )

    return recommendations


def explain_recommendation(recommendation):
    """
    Create a simple explanation for a recommended course.
    """

    course = recommendation["course"]
    name = recommendation["name"]
    unlock_count = recommendation["unlock_count"]
    future_count = recommendation["future_unlock_count"]

    if unlock_count > 0:

        direct = ", ".join(
            recommendation["unlocks"]
        )

        return (
            f"{course} - {name} is currently eligible. "
            f"It directly unlocks {unlock_count} course(s): "
            f"{direct}. It is connected to "
            f"{future_count} unfinished course(s) "
            f"in the future prerequisite chain."
        )

    return (
        f"{course} - {name} is currently eligible. "
        f"It does not directly unlock another unfinished course."
    )


def explain_blocked_course(
    course,
    prerequisite_groups,
    course_data,
    course_rules,
    completed
):
    """
    Explain why a course cannot currently be taken.
    """

    if course not in course_data:
        return f"{course} was not found in the course catalog."

    if course in completed:
        return f"{course} is already completed."

    if (
        prerequisites_satisfied(
            course,
            prerequisite_groups,
            completed
        )
        and course_rules_satisfied(
            course,
            course_data,
            course_rules,
            completed
        )
    ):
        return (
            f"{course} is not blocked. "
            f"You are eligible to take it."
        )

    reasons = []

    missing_groups = get_missing_prerequisite_groups(
        course,
        prerequisite_groups,
        completed
    )

    for group in missing_groups:

        if len(group) == 1:
            reasons.append(
                f"complete {group[0]}"
            )

        else:
            reasons.append(
                "complete one of: "
                + " or ".join(group)
            )

    rule = course_rules.get(course)

    if rule:

        minimum = rule["minimum_completed_credits"]

        completed_credits = get_completed_credits(
            course_data,
            completed
        )

        if completed_credits < minimum:
            reasons.append(
                f"reach at least {minimum} completed credits"
            )

    return (
        f"{course} is blocked because you still need to "
        + "; ".join(reasons)
        + "."
    )


def get_prerequisite_chain(
    course,
    prerequisite_groups,
    completed
):
    """
    Return unfinished courses appearing in the prerequisite
    network before the selected course.

    For OR groups, all possible alternatives are shown.
    """

    visited = set()
    chain = set()

    def dfs(current):

        for group in prerequisite_groups.get(current, []):

            for prerequisite in group:

                if prerequisite in visited:
                    continue

                visited.add(prerequisite)

                if prerequisite in completed:
                    continue

                chain.add(prerequisite)

                dfs(prerequisite)

    dfs(course)

    return sorted(chain)


def build_advisor_report(
    prerequisite_groups,
    completed,
    course_data,
    course_rules
):
    """
    Build a full academic advisor report.
    """

    status = get_academic_status(
        prerequisite_groups,
        course_data,
        course_rules,
        completed
    )

    recommendations = recommend_eligible_courses(
        prerequisite_groups,
        completed,
        course_data,
        course_rules
    )

    recommendation_details = []

    for recommendation in recommendations:

        recommendation_details.append({
            **recommendation,
            "explanation": explain_recommendation(
                recommendation
            )
        })

    blocked_details = {}

    for course in status["blocked"]:

        blocked_details[course] = {
            **status["blocked"][course],

            "prerequisite_chain":
                get_prerequisite_chain(
                    course,
                    prerequisite_groups,
                    completed
                ),

            "explanation":
                explain_blocked_course(
                    course,
                    prerequisite_groups,
                    course_data,
                    course_rules,
                    completed
                )
        }

    return {
        "completed": status["completed"],
        "eligible": status["eligible"],
        "recommendations": recommendation_details,
        "blocked": blocked_details
    }


def get_next_semester_advice(
    degree_plan,
    advisor_report
):
    """
    Match advisor recommendations with the first semester
    of the generated degree plan.
    """

    if not degree_plan:

        return {
            "courses": [],
            "recommendations": []
        }

    next_semester = list(
        degree_plan[0]
    )

    next_semester_recommendations = []

    for recommendation in advisor_report[
        "recommendations"
    ]:

        if recommendation["course"] in next_semester:

            next_semester_recommendations.append(
                recommendation
            )

    return {
        "courses": next_semester,
        "recommendations":
            next_semester_recommendations
    }