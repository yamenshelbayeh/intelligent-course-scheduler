from src.db import (
    get_prerequisite_graph,
    get_course_data
)

from src.ai.pathfinder import a_star_degree_plan

from src.ai.advisor import (
    build_advisor_report,
    get_next_semester_advice
)

from src.db import (
    get_prerequisite_graph,
    get_course_data
)

from src.ai.pathfinder import a_star_degree_plan

from src.ai.advisor import (
    build_advisor_report,
    get_next_semester_advice
)


def main():
    graph = get_prerequisite_graph()
    course_data = get_course_data()

    completed = {
        "CSE101",
        "MATH101"
    }

    advisor_report = build_advisor_report(
        graph,
        completed,
        course_data
    )

    degree_plan, expanded_states = a_star_degree_plan(
        graph=graph,
        completed=frozenset(completed),
        course_data=course_data,
        max_credits=15,
        max_difficulty=10
    )

    next_semester_advice = get_next_semester_advice(
        degree_plan,
        advisor_report
    )

    print("ACADEMIC ADVISOR")
    print("=" * 50)

    print("\nCompleted:")
    print(", ".join(advisor_report["completed"]))

    print("\nEligible:")
    print(", ".join(advisor_report["eligible"]))

    print("\nRecommended Next Semester:")
    print("-" * 50)

    for recommendation in next_semester_advice["recommendations"]:
        print()
        print(recommendation["explanation"])

    print("\nPlanned Courses:")
    print(", ".join(next_semester_advice["courses"]))

    print("\nA* Expanded States:")
    print(expanded_states)


if __name__ == "__main__":
    main()