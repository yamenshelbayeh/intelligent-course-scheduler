from src.db import (
    get_prerequisite_graph,
    get_course_data,
    get_section_data
)

from src.ai.pathfinder import a_star_degree_plan
from src.ai.degree_scheduler import generate_degree_timetables


def main():
    graph = get_prerequisite_graph()
    course_data = get_course_data()
    section_data = get_section_data()

    completed = frozenset()

    degree_plan, expanded_states = a_star_degree_plan(
        graph=graph,
        completed=completed,
        course_data=course_data,
        max_credits=15,
        max_difficulty=10
    )

    if degree_plan is None:
        print("No degree plan found.")
        return

    degree_timetables = generate_degree_timetables(
        degree_plan,
        section_data
    )

    print("\nFINAL DEGREE SCHEDULE")
    print("=" * 50)

    for semester in degree_timetables:
        print(f"\nSemester {semester['semester']}")
        print("-" * 30)

        for course, section in semester["timetable"].items():
            print(
                f"{course} - Section "
                f"{section['section_code']}"
            )

            for meeting in section["meetings"]:
                print(
                    f"  Day {meeting['day_of_week']}: "
                    f"{meeting['start_time']} - "
                    f"{meeting['end_time']}"
                )

        print(
            f"CSP calls: {semester['stats']['calls']}, "
            f"backtracks: {semester['stats']['backtracks']}"
        )

    print("\nA* Search")
    print("-" * 30)
    print("Expanded states:", expanded_states)


if __name__ == "__main__":
    main()