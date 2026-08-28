import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


def get_prerequisite_graph():
    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute("""
                           SELECT course_code
                           FROM courses
                           ORDER BY course_code;
                           """)

            courses = cursor.fetchall()

            graph = {}

            for course in courses:
                graph[course[0]] = []

            cursor.execute("""
                           SELECT c.course_code,
                                  p_course.course_code
                           FROM prerequisites p
                                    JOIN courses c
                                         ON c.course_id = p.course_id
                                    JOIN courses p_course
                                         ON p_course.course_id = p.prerequisite_id
                           ORDER BY c.course_code;
                           """)

            prerequisites = cursor.fetchall()

            for course, prerequisite in prerequisites:
                graph[course].append(prerequisite)

            return graph


def get_course_data():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT course_code,
                                     credits,
                                     difficulty
                              FROM courses;
                           """)

            courses = cursor.fetchall()
            course_data = {}
            for course in courses:
                course_data[course[0]] = {"credits": course[1], "difficulty": course[2]}

            return course_data


def get_section_data():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                           SELECT c.course_code,
                                  cs.section_id,
                                  cs.section_code,
                                  sm.day_of_week,
                                  sm.start_time,
                                  sm.end_time
                           FROM courses c
                                    JOIN course_sections cs
                                         ON cs.course_id = c.course_id
                                    JOIN section_meetings sm
                                         ON sm.section_id = cs.section_id
                           ORDER BY c.course_code,
                                    cs.section_code,
                                    sm.day_of_week;
                           """)

            rows = cursor.fetchall()

    section_data = {}

    for row in rows:
        course_code = row[0]
        section_id = row[1]
        section_code = row[2]
        day_of_week = row[3]
        start_time = row[4]
        end_time = row[5]

        # Create the course if we haven't seen it yet
        if course_code not in section_data:
            section_data[course_code] = {}

        # Create the section if we haven't seen it yet
        if section_id not in section_data[course_code]:
            section_data[course_code][section_id] = {
                "section_id": section_id,
                "section_code": section_code,
                "meetings": []
            }

        # Add this meeting to the section
        section_data[course_code][section_id]["meetings"].append({
            "day_of_week": day_of_week,
            "start_time": start_time,
            "end_time": end_time
        })

    # Convert section dictionaries into lists
    result = {}

    for course_code, sections in section_data.items():
        result[course_code] = list(sections.values())

    return result
