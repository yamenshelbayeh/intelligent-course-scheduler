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


def main():
    with get_connection() as connection:

        with connection.cursor() as cursor:

            # Get every course
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
                SELECT
                    c.course_code,
                    p_course.course_code
                FROM prerequisites p
                JOIN courses c
                    ON c.course_id = p.course_id
                JOIN courses p_course
                    ON p_course.course_id = p.prerequisite_id
                ORDER BY c.course_code;
            """)

            prerequisites = cursor.fetchall()

            # Add prerequisites to graph
            for course, prerequisite in prerequisites:
                graph[course].append(prerequisite)

            print(graph)

if __name__ == "__main__":
    main()