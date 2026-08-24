from src.ai.graph import get_eligible_courses
from src.db import get_prerequisite_graph
from src.db import get_course_data


def generate_degree_plan(graph, completed, course_data, max_credits=15, max_difficulty=10):
    plan = []
    current_completed = completed.copy()


    while len(current_completed) < len(graph):

        eligible_courses = get_eligible_courses(graph, current_completed)

        if len(eligible_courses) == 0:
            raise ValueError(
                "Unable to generate degree plan: "
                "no eligible course fits within the semester constraints."
            )

        semester = []
        semester_credits = 0
        semester_difficulty = 0


        for course in eligible_courses:
            if (semester_credits + course_data[course]["credits"] <= max_credits
                    and semester_difficulty + course_data[course]["difficulty"] <= max_difficulty):
                semester.append(course)
                semester_credits += course_data[course]["credits"]
                semester_difficulty += course_data[course]["difficulty"]

        if len(semester) == 0:
            raise ValueError(
                "Unable to generate degree plan: "
                "no eligible course fits within the semester constraints."
            )


        plan.append(semester)

        for course in semester:
            current_completed.add(course)

    return plan


def main():
    graph = get_prerequisite_graph()
    course_data = get_course_data()

    completed = set()

    plan = generate_degree_plan(
        graph,
        completed,
        course_data,
        max_credits=15,
        max_difficulty=10
    )

    for semester_number, semester in enumerate(plan, start=1):

        total_credits = sum(
            course_data[course]["credits"]
            for course in semester
        )

        total_difficulty = sum(
            course_data[course]["difficulty"]
            for course in semester
        )

        print(
            f"Semester {semester_number}: {semester} "
            f"({total_credits} credits, "
            f"difficulty {total_difficulty})"
        )


if __name__ == "__main__":
    main()