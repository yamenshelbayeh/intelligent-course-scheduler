import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

from collections import defaultdict


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


def get_course_data():
    """
    Load all courses from the database.

    Returns:
        {
            "INBMA0101-24": {
                "name": "Algorithms and Basics of Programming",
                "credits": 3,
                "category": "NATURAL_SCIENCE",
                "recommended_semester": 1,
                "period": "1",
                "assessment": "PM",
                "is_required": True
            },
            ...
        }
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            code,
            name,
            credits,
            category,
            recommended_semester,
            period,
            assessment,
            is_required
        FROM courses
        ORDER BY code;
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    course_data = {}

    for row in rows:
        code = row[0]

        course_data[code] = {
            "name": row[1],
            "credits": row[2],
            "category": row[3],
            "recommended_semester": row[4],
            "period": row[5],
            "assessment": row[6],
            "is_required": row[7]
        }

    return course_data


def get_prerequisite_groups():
    """
    Load prerequisite rules.

    Different groups mean AND.
    Multiple courses inside one group mean OR.

    Example:

    Development of Embedded Systems:

    [
        {"INBMA0528-17"},
        {"INBMA9937-17", "INBMA9939-17"}
    ]

    means:

    Embedded Systems
    AND
    (Microcontrollers OR Programmable Logic Devices)
    """

    conn = get_connection()
    cursor = conn.cursor()

    # Get every course first so courses without prerequisites
    # also appear in the result.
    cursor.execute("""
        SELECT code
        FROM courses
        ORDER BY code;
    """)

    course_codes = [row[0] for row in cursor.fetchall()]

    cursor.execute("""
        SELECT
            c.code,
            pg.group_number,
            p.code
        FROM prerequisite_groups pg

        JOIN courses c
            ON c.id = pg.course_id

        JOIN prerequisite_options po
            ON po.group_id = pg.id

        JOIN courses p
            ON p.id = po.prerequisite_course_id

        ORDER BY
            c.code,
            pg.group_number,
            p.code;
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    temp = defaultdict(lambda: defaultdict(set))

    for course_code, group_number, prerequisite_code in rows:
        temp[course_code][group_number].add(prerequisite_code)

    prerequisite_groups = {}

    for code in course_codes:
        groups = temp.get(code, {})

        prerequisite_groups[code] = [
            groups[group_number]
            for group_number in sorted(groups)
        ]

    return prerequisite_groups


def get_degree_requirements():
    """
    Load degree credit requirements.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            category,
            required_credits,
            counts_toward_degree
        FROM degree_requirements
        ORDER BY category;
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    requirements = {}

    for category, required_credits, counts_toward_degree in rows:
        requirements[category] = {
            "required_credits": required_credits,
            "counts_toward_degree": counts_toward_degree
        }

    return requirements


def get_course_rules():
    """
    Load special rules which are not normal prerequisites.

    Example:
    Thesis 1 requires at least 100 completed credits.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.code,
            cr.minimum_completed_credits
        FROM course_rules cr

        JOIN courses c
            ON c.id = cr.course_id;
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    rules = {}

    for course_code, minimum_credits in rows:
        rules[course_code] = {
            "minimum_completed_credits": minimum_credits
        }

    return rules


def load_curriculum():
    """
    Load everything needed by the planner.
    """

    return {
        "courses": get_course_data(),
        "prerequisites": get_prerequisite_groups(),
        "degree_requirements": get_degree_requirements(),
        "course_rules": get_course_rules()
    }


# ------------------------------------------------------------
# Quick database test
# ------------------------------------------------------------

if __name__ == "__main__":

    curriculum = load_curriculum()

    courses = curriculum["courses"]
    prerequisites = curriculum["prerequisites"]
    requirements = curriculum["degree_requirements"]
    rules = curriculum["course_rules"]

    print("Courses:", len(courses))

    print("\nDegree Requirements:")
    for category, data in requirements.items():
        print(category, data)

    print("\nAI Prerequisites:")
    for group in prerequisites["INBMA0526-24"]:
        print(group)

    print("\nDevelopment of Embedded Systems Prerequisites:")
    for group in prerequisites["INBMA9940-17"]:
        print(group)

    print("\nSpecial Rules:")
    print(rules)