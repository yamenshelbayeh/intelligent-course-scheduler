from src.ai.scheduler import generate_timetable


def generate_degree_timetables(degree_plan, section_data):
    timetables = []

    for semester_number, semester_courses in enumerate(
        degree_plan,
        start=1
    ):
        solution, stats, neighbors = generate_timetable(
            section_data,
            list(semester_courses)
        )

        if solution is None:
            raise ValueError(
                f"No valid timetable found for semester "
                f"{semester_number}"
            )

        timetables.append({
            "semester": semester_number,
            "courses": semester_courses,
            "timetable": solution,
            "stats": stats
        })

    return timetables