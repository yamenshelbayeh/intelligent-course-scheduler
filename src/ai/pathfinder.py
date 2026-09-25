import math
from heapq import heappush, heappop

from src.ai.graph import (
    get_eligible_courses,
    prerequisites_satisfied,
    course_rules_satisfied
)

from itertools import combinations, count


def completed_category_credits(state, course_data, category):

    return sum(
        course_data[code]["credits"]
        for code in state
        if code in course_data
        and course_data[code]["category"] == category
    )


def differentiated_credits(state, course_data):

    return sum(
        course_data[code]["credits"]
        for code in state
        if code in course_data
        and course_data[code]["category"]
        in {"DIFFERENTIATED", "PROFESSIONAL_TRAINING"}
    )


def required_courses_completed(state, course_data):

    for code, data in course_data.items():

        if data["is_required"] and code not in state:
            return False

    return True


def is_goal(state, course_data, degree_requirements):
    """
    Check whether the structured curriculum requirements
    are completed.

    Free-choice courses are not checked here because the
    curriculum requires 12 free-choice credits but does not
    define fixed courses for them.
    """

    # Every individually compulsory course must be completed.
    if not required_courses_completed(state, course_data):
        return False

    for category, requirement in degree_requirements.items():

        required = requirement["required_credits"]

        # No fixed free-choice courses exist in our database.
        if category == "FREE_CHOICE":
            continue

        if category == "DIFFERENTIATED":
            completed = differentiated_credits(
                state,
                course_data
            )

        else:
            completed = completed_category_credits(
                state,
                course_data,
                category
            )

        if completed < required:
            return False

    return True


def remaining_planned_credits(state, course_data, degree_requirements):
    """
    Estimate how many structured curriculum credits still
    need to be completed.

    Free-choice credits are excluded because the curriculum
    does not specify which courses should satisfy them.
    """

    # Required courses except Professional Training.
    required_remaining = sum(
        data["credits"]
        for code, data in course_data.items()
        if data["is_required"]
        and code not in state
        and data["category"] != "PROFESSIONAL_TRAINING"
    )

    # Professional Training is mandatory.
    professional_remaining = sum(
        data["credits"]
        for code, data in course_data.items()
        if data["is_required"]
        and code not in state
        and data["category"] == "PROFESSIONAL_TRAINING"
    )

    # Professional Training also contributes toward the
    # 30 differentiated credits.
    diff_required = degree_requirements[
        "DIFFERENTIATED"
    ]["required_credits"]

    diff_completed = differentiated_credits(
        state,
        course_data
    )

    diff_remaining = max(
        0,
        diff_required - diff_completed
    )

    # Do NOT count Professional Training twice.
    remaining_diff_block = max(
        professional_remaining,
        diff_remaining
    )

    return required_remaining + remaining_diff_block


def heuristic(state, course_data, degree_requirements, max_credits):

    remaining = remaining_planned_credits(
        state,
        course_data,
        degree_requirements
    )

    return math.ceil(remaining / max_credits)


def course_available_in_semester(course_code, course_data, semester, include_irregular=False):
    """
    Check whether a course can be planned in this semester.

    Period 1 -> odd semesters
    Period 2 -> even semesters
    Period I -> irregular / occasionally announced

    Thesis and Professional Training cannot be placed before
    their recommended semester.
    """

    data = course_data[course_code]

    period = data["period"]
    recommended = data["recommended_semester"]
    category = data["category"]

    # Thesis and Professional Training have stronger
    # semester restrictions.
    if category in {"THESIS", "PROFESSIONAL_TRAINING"}:

        if (recommended is not None and semester < recommended):
            return False

    if period == "1":
        return semester % 2 == 1

    if period == "2":
        return semester % 2 == 0

    if period == "I":

        # Required irregular course, such as Professional
        # Training, can be used from its recommended semester.
        if data["is_required"]:

            if recommended is None:
                return True

            return semester >= recommended

        # Occasionally announced electives are not selected
        # automatically unless explicitly enabled.
        return include_irregular

    return True


def get_actions(state, semester, prerequisite_groups, course_data, course_rules, degree_requirements, max_credits=30, include_irregular=False, unavailable_by_semester= None):
    """
    Generate possible course combinations for one semester.

    Only courses whose:
        - prerequisites are satisfied
        - special rules are satisfied
        - period matches the semester
        - credits fit the semester limit

    are considered.
    """

    if unavailable_by_semester == None:
        unavailable_by_semester = {}

    unavailable_now = unavailable_by_semester.get(semester, set())

    eligible = get_eligible_courses(prerequisite_groups, course_data, course_rules, state)

    diff_required = degree_requirements["DIFFERENTIATED"]["required_credits"]

    # Professional Training is mandatory and its 12 credits
    # are already part of the 30 differentiated credits.

    professional_training_credits = sum(
        data["credits"]
        for data in course_data.values()
        if data["category"] == "PROFESSIONAL_TRAINING"
        and data["is_required"]
    )

    optional_diff_target = (
            diff_required - professional_training_credits
    )

    optional_diff_completed = completed_category_credits(
        state,
        course_data,
        "DIFFERENTIATED"
    )

    optional_diff_remaining = max(
        0,
        optional_diff_target - optional_diff_completed
    )

    diff_completed = differentiated_credits(
        state,
        course_data
    )

    need_differentiated = (
        diff_completed < diff_required
    )

    candidates = []

    for code in eligible:

        data = course_data[code]

        # What-if constraint:
        # skip courses unavailable this semester.
        if code in unavailable_now:
            continue

        if not course_available_in_semester(code, course_data, semester, include_irregular):
            continue


        # Required courses are always relevant.
        if data["is_required"]:
            candidates.append(code)
            continue

        # Optional differentiated courses are relevant only
        # while differentiated credits are still needed.
        if (
            data["category"] == "DIFFERENTIATED"
            and need_differentiated
        ):
            candidates.append(code)

    # Sort so results are deterministic.
    candidates.sort()

    valid_actions = []

    for size in range(1, len(candidates) + 1):

        for combo in combinations(candidates, size):

            credits = sum(
                course_data[code]["credits"]
                for code in combo
            )

            if credits > max_credits:
                continue

            # Optional differentiated courses should contribute
            # only the credits actually needed for the degree.
            optional_diff_in_action = sum(
                course_data[code]["credits"]
                for code in combo
                if course_data[code]["category"] == "DIFFERENTIATED"
            )

            if optional_diff_in_action > optional_diff_remaining:
                continue

            valid_actions.append(combo)

    # If nothing can be taken this semester, allow the
    # planner to advance to the next semester.
    if not valid_actions:
        return [tuple()]

    # --------------------------------------------------------
    # Remove dominated actions
    # --------------------------------------------------------
    #
    # If another eligible course can still be added without
    # exceeding max_credits, taking the smaller combination
    # cannot be better when minimizing semesters.
    #
    # So keep only maximal semester loads.
    # --------------------------------------------------------

    maximal_actions = []

    for action in valid_actions:

        action_set = set(action)

        used_credits = sum(
            course_data[code]["credits"]
            for code in action
        )

        can_add_more = False

        for code in candidates:

            if code in action_set:
                continue

            if (
                used_credits
                + course_data[code]["credits"]
                <= max_credits
            ):
                can_add_more = True
                break

        if not can_add_more:
            maximal_actions.append(action)

    # Prefer required courses and recommended-semester courses
    # when A* has several equivalent choices.
    def action_priority(action):

        required_count = sum(
            course_data[code]["is_required"]
            for code in action
        )

        recommended_count = sum(
            course_data[code]["recommended_semester"]
            == semester
            for code in action
        )

        credits = sum(
            course_data[code]["credits"]
            for code in action
        )

        return (
            required_count,
            recommended_count,
            credits
        )

    maximal_actions.sort(
        key=action_priority,
        reverse=True
    )

    return maximal_actions


def transition(state, action):

    return frozenset(
        set(state).union(action)
    )

def action_recommendation_penalty(action, semester, course_data):
    """
    Used only as an A* tie-breaker.

    Plans closer to the curriculum's recommended semesters
    are explored first.
    """

    penalty = 0

    for code in action:

        recommended = course_data[code]["recommended_semester"]

        if recommended is not None:
            penalty += abs(semester - recommended)

    return penalty

def a_star_degree_plan(prerequisite_groups, course_data, course_rules, degree_requirements, completed=None, start_semester=1, max_credits=30, include_irregular=False, max_semesters=10, unavailable_by_semester=None):
    """
    Generate a degree plan using A* search.

    State:
        frozenset of completed course codes

    Action:
        tuple of courses taken during one semester

    Cost:
        number of semesters

    Goal:
        all required curriculum requirements are satisfied
    """

    if completed is None:
        completed = set()

    if unavailable_by_semester is None:
        unavailable_by_semester = {}

    start_state = frozenset(completed)

    initial_h = heuristic(start_state, course_data, degree_requirements, max_credits)

    tie_breaker = count()

    frontier = []

    heappush(frontier,(initial_h, 0, 0, next(tie_breaker), start_semester, start_state, []))

    visited = set()

    expanded_states = 0

    while frontier:

        (
            f,
            negative_g,
            penalty,
            _,
            semester,
            state,
            path
        ) = heappop(frontier)

        g = -negative_g

        state_key = (
            state,
            semester
        )

        if state_key in visited:
            continue

        visited.add(state_key)

        # ----------------------------------------
        # Goal test
        # ----------------------------------------

        if is_goal(state, course_data, degree_requirements):
            return (path, expanded_states, initial_h)

        # Prevent endless waiting/searching
        if g >= max_semesters:
            continue

        expanded_states += 1

        # ----------------------------------------
        # Generate semester actions
        # ----------------------------------------

        actions = get_actions(
            state=state,
            semester=semester,
            prerequisite_groups=prerequisite_groups,
            course_data=course_data,
            course_rules=course_rules,
            degree_requirements=degree_requirements,
            max_credits=max_credits,
            include_irregular=include_irregular,
            unavailable_by_semester = unavailable_by_semester
        )

        for action in actions:

            next_state = transition(state, action)

            next_semester = semester + 1
            new_g = g + 1

            h = heuristic(next_state, course_data, degree_requirements, max_credits)

            new_f = new_g + h

            new_penalty = (penalty + action_recommendation_penalty(action, semester, course_data))

            new_path = path + [action]

            heappush(
                frontier,
                (
                    new_f,

                    # When f is equal, explore deeper
                    # states first. This prevents A*
                    # from behaving like breadth-first
                    # search across hundreds of equal
                    # solutions.
                    -new_g,

                    new_penalty,

                    next(tie_breaker),

                    next_semester,
                    next_state,
                    new_path
                )
            )

    return (None, expanded_states, initial_h)


def validate_plan(
    plan,
    prerequisite_groups,
    course_data,
    course_rules,
    degree_requirements,
    completed=None,
    start_semester=1,
    max_credits=30,
    unavailable_by_semester=None
):
    """
    Validate a generated degree plan.

    Checks:
    - credit limit
    - no repeated courses
    - semester availability
    - prerequisites
    - special course rules
    - final degree requirements
    - If the subject is not available by semester
    """

    if completed is None:
        completed = set()

    if unavailable_by_semester is None:
        unavailable_by_semester = {}

    current_completed = set(completed)
    errors = []

    for offset, action in enumerate(plan):

        semester = start_semester + offset

        # ----------------------------------------
        # Semester credit limit
        # ----------------------------------------

        semester_credits = sum(
            course_data[code]["credits"]
            for code in action
        )

        if semester_credits > max_credits:
            errors.append(
                f"Semester {semester}: "
                f"{semester_credits} credits exceeds "
                f"the {max_credits}-credit limit."
            )

        # ----------------------------------------
        # Validate each course
        # ----------------------------------------

        for code in action:

            if code in current_completed:
                errors.append(
                    f"Semester {semester}: "
                    f"{code} was already completed."
                )

            if code in unavailable_by_semester.get(
                    semester,
                    set()
            ):
                errors.append(
                    f"Semester {semester}: "
                    f"{code} was marked unavailable."
                )

            if not course_available_in_semester(
                code,
                course_data,
                semester
            ):
                errors.append(
                    f"Semester {semester}: "
                    f"{code} is not available."
                )

            if not prerequisites_satisfied(
                code,
                prerequisite_groups,
                current_completed
            ):
                errors.append(
                    f"Semester {semester}: "
                    f"prerequisites not satisfied for {code}."
                )

            if not course_rules_satisfied(
                code,
                course_data,
                course_rules,
                current_completed
            ):
                errors.append(
                    f"Semester {semester}: "
                    f"special rules not satisfied for {code}."
                )

        # Courses from the semester become completed
        # only AFTER the semester.
        current_completed.update(action)

    # ----------------------------------------
    # Final degree goal
    # ----------------------------------------

    if not is_goal(
        frozenset(current_completed),
        course_data,
        degree_requirements
    ):
        errors.append(
            "Final plan does not satisfy degree requirements."
        )

    return len(errors) == 0, errors


if __name__ == "__main__":

    from src.db import load_curriculum

    curriculum = load_curriculum()

    course_data = curriculum["courses"]
    prerequisites = curriculum["prerequisites"]
    degree_requirements = curriculum["degree_requirements"]
    course_rules = curriculum["course_rules"]

    scenario = {
        1: {"INBMA0101-24"}
    }

    plan, expanded_states, initial_h = a_star_degree_plan(
        prerequisite_groups=prerequisites,
        course_data=course_data,
        course_rules=course_rules,
        degree_requirements=degree_requirements,
        completed=set(),
        start_semester=1,
        max_credits=30,
        unavailable_by_semester=scenario
    )

    print("Semesters:", len(plan))
    print("Expanded states:", expanded_states)

    for semester, action in enumerate(plan, start=1):
        print(semester, action)

    valid, errors = validate_plan(
        plan=plan,
        prerequisite_groups=prerequisites,
        course_data=course_data,
        course_rules=course_rules,
        degree_requirements=degree_requirements,
        completed=set(),
        start_semester=1,
        max_credits=30,
        unavailable_by_semester=scenario
    )

    print("Valid:", valid)
    print("Errors:", errors)