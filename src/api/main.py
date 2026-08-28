from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.ai.degree_scheduler import generate_degree_timetables
from src.ai.scheduler import generate_timetable
from src.db import (
    get_prerequisite_graph,
    get_course_data,
    get_section_data
)
from src.ai.advisor import build_advisor_report
from src.ai.pathfinder import a_star_degree_plan

app = FastAPI()


class AdvisorRequest(BaseModel):
    completed: list[str]


class DegreePlanRequest(BaseModel):
    completed: list[str]
    max_credits: int = Field(default=15, ge=1, le=30)
    max_difficulty: int = Field(default=10, ge=1)


class TimetableRequest(BaseModel):
    courses: list[str]


class FullPlanRequest(BaseModel):
    completed: list[str]
    max_credits: int = Field(default=15, ge=1, le=30)
    max_difficulty: int = Field(default=10, ge=1)


def validate_courses(courses, valid_courses):
    invalid_courses = [
        course
        for course in courses
        if course not in valid_courses
    ]

    if invalid_courses:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown courses: {', '.join(invalid_courses)}"
        )


@app.get("/")
def home():
    return {
        "message": "Course Scheduler API is running"
    }


@app.post("/advisor")
def advisor(data: AdvisorRequest):
    graph = get_prerequisite_graph()
    course_data = get_course_data()

    completed = set(data.completed)

    validate_courses(completed, graph)

    return build_advisor_report(
        graph,
        completed,
        course_data
    )


@app.post("/degree-plan")
def degree_plan(data: DegreePlanRequest):
    graph = get_prerequisite_graph()
    course_data = get_course_data()

    completed = set(data.completed)

    validate_courses(completed, graph)

    try:
        plan, expanded_states = a_star_degree_plan(
            graph=graph,
            completed=frozenset(completed),
            course_data=course_data,
            max_credits=data.max_credits,
            max_difficulty=data.max_difficulty
        )

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error)
        )

    return {
        "plan": plan,
        "expanded_states": expanded_states
    }


@app.post("/timetable")
def timetable(data: TimetableRequest):
    if not data.courses:
        raise HTTPException(
            status_code=400,
            detail="At least one course must be selected."
        )

    if len(data.courses) != len(set(data.courses)):
        raise HTTPException(
            status_code=400,
            detail="Duplicate courses are not allowed."
        )

    section_data = get_section_data()

    validate_courses(data.courses, section_data)

    solution, stats, _ = generate_timetable(section_data, data.courses)

    if solution is None:
        raise HTTPException(
            status_code=422,
            detail="No conflict-free timetable could be generated for the selected courses."
        )

    return {
        "timetable": solution,
        "stats": stats
    }


@app.post("/full-plan")
def full_plan(data: FullPlanRequest):
    graph = get_prerequisite_graph()
    course_data = get_course_data()
    section_data = get_section_data()

    completed = set(data.completed)

    validate_courses(completed, graph)

    advisor_report = build_advisor_report(
        graph,
        completed,
        course_data
    )

    try:
        plan, expanded_states = a_star_degree_plan(
            graph=graph,
            completed=frozenset(completed),
            course_data=course_data,
            max_credits=data.max_credits,
            max_difficulty=data.max_difficulty
        )

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error)
        )

    try:
        degree_timetables = generate_degree_timetables(
            plan,
            section_data
        )

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error)
        )

    degree_plan_details = []

    for semester_number, courses in enumerate(plan, start=1):
        total_credits = sum(
            course_data[course]["credits"]
            for course in courses
        )

        total_difficulty = sum(
            course_data[course]["difficulty"]
            for course in courses
        )

        degree_plan_details.append({
            "semester": semester_number,
            "courses": list(courses),
            "total_credits": total_credits,
            "total_difficulty": total_difficulty
        })

    return {
        "advisor": advisor_report,
        "degree_plan": plan,
        "degree_plan_details": degree_plan_details,
        "degree_timetables": degree_timetables,
        "expanded_states": expanded_states
    }
