-- Find all direct and indirect prerequisites for a target course.
-- Current test target: CSE303 (Machine Learning)

WITH RECURSIVE h AS (

    SELECT
        c.course_code AS prerequisite_code,
        c.course_name AS prerequisite_name,
        p.prerequisite_id,
        1 AS depth
    FROM prerequisites p
    JOIN courses c
        ON c.course_id = p.prerequisite_id
    WHERE p.course_id = (
        SELECT course_id
        FROM courses
        WHERE course_code = 'CSE303'
    )

    UNION ALL

    SELECT
        c1.course_code,
        c1.course_name,
        p1.prerequisite_id,
        h.depth + 1
    FROM prerequisites p1
    JOIN courses c1
        ON c1.course_id = p1.prerequisite_id
    JOIN h
        ON p1.course_id = h.prerequisite_id
)

SELECT
    prerequisite_code,
    prerequisite_name,
    depth
FROM h
ORDER BY depth, prerequisite_code;