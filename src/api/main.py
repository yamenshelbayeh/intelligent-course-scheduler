from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.db import load_curriculum

from src.ai.pathfinder import (
    a_star_degree_plan,
    validate_plan,
    differentiated_credits
)


app = FastAPI(
    title="Intelligent Course Scheduler API",
    description=(
        "AI-based degree planner for the University of Debrecen "
        "Computer Science Engineering BSc curriculum."
    ),
    version="2.0"
)


class DegreePlanRequest(BaseModel):
    completed: list[str] = Field(default_factory=list)

    max_credits: int = Field(
        default=30,
        ge=1,
        le=30
    )

    start_semester: int = Field(
        default=1,
        ge=1,
        le=7
    )


def validate_courses(courses, valid_courses):

    invalid_courses = [
        course
        for course in courses
        if course not in valid_courses
    ]

    if invalid_courses:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unknown courses: "
                + ", ".join(invalid_courses)
            )
        )


@app.get("/")
def home():
    return {
        "message": "Intelligent Course Scheduler API is running",
        "curriculum": "University of Debrecen - Computer Science Engineering BSc"
    }


@app.get("/curriculum")
def curriculum():

    data = load_curriculum()

    course_data = data["courses"]
    degree_requirements = data["degree_requirements"]

    return {
        "course_count": len(course_data),
        "courses": course_data,
        "degree_requirements": degree_requirements
    }


@app.post("/degree-plan")
def degree_plan(data: DegreePlanRequest):

    curriculum = load_curriculum()

    course_data = curriculum["courses"]
    prerequisites = curriculum["prerequisites"]
    degree_requirements = curriculum["degree_requirements"]
    course_rules = curriculum["course_rules"]

    completed = set(data.completed)

    validate_courses(
        completed,
        course_data
    )

    plan, expanded_states, initial_heuristic = (
        a_star_degree_plan(
            prerequisite_groups=prerequisites,
            course_data=course_data,
            course_rules=course_rules,
            degree_requirements=degree_requirements,
            completed=completed,
            start_semester=data.start_semester,
            max_credits=data.max_credits
        )
    )

    if plan is None:
        raise HTTPException(
            status_code=422,
            detail="No valid degree plan could be generated."
        )

    valid, errors = validate_plan(
        plan=plan,
        prerequisite_groups=prerequisites,
        course_data=course_data,
        course_rules=course_rules,
        degree_requirements=degree_requirements,
        completed=completed,
        start_semester=data.start_semester,
        max_credits=data.max_credits
    )

    if not valid:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Generated plan failed validation.",
                "errors": errors
            }
        )


    degree_plan = []

    total_planned_credits = 0

    for offset, courses in enumerate(plan):

        semester_number = (
            data.start_semester + offset
        )

        semester_credits = sum(
            course_data[course]["credits"]
            for course in courses
        )

        total_planned_credits += semester_credits

        course_details = []

        for course in courses:

            info = course_data[course]

            course_details.append({
                "code": course,
                "name": info["name"],
                "credits": info["credits"],
                "category": info["category"]
            })

        degree_plan.append({
            "semester": semester_number,
            "courses": course_details,
            "total_credits": semester_credits
        })


    planned_courses = {
        course
        for semester in plan
        for course in semester
    }

    final_state = completed | planned_courses

    diff_credits = differentiated_credits(
        final_state,
        course_data
    )

    return {
        "degree_plan": degree_plan,

        "statistics": {
            "total_semesters": len(plan),
            "planned_credits": total_planned_credits,
            "free_choice_credits_remaining": 12,
            "differentiated_credits": diff_credits,
            "expanded_states": expanded_states,
            "initial_heuristic": initial_heuristic
        },

        "validation": {
            "valid": valid,
            "errors": errors
        }
    }