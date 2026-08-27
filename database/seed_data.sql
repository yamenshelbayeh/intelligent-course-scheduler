INSERT INTO courses (course_code, course_name, credits, difficulty)
VALUES
    ('CSE101', 'Programming I', 5, 2),
    ('CSE102', 'Programming II', 5, 3),
    ('CSE201', 'Data Structures', 5, 3),
    ('CSE202', 'Algorithms', 5, 4),
    ('MATH101', 'Calculus I', 5, 3),
    ('MATH201', 'Discrete Mathematics', 5, 3),
    ('STAT201', 'Probability and Statistics', 5, 3),
    ('CSE301', 'Databases', 5, 3),
    ('CSE302', 'Artificial Intelligence', 5, 4),
    ('CSE303', 'Machine Learning', 5, 5);
INSERT INTO prerequisites (course_id, prerequisite_id)
VALUES (
    (SELECT course_id
     FROM courses
     WHERE course_code = 'CSE102'),

    (SELECT course_id
     FROM courses
     WHERE course_code = 'CSE101')
    ),(
    (SELECT course_id
     FROM courses
     WHERE course_code = 'CSE201'),

    (SELECT course_id
     FROM courses
     WHERE course_code = 'CSE102')
    ),(
    (SELECT course_id
     FROM courses
     WHERE course_code = 'CSE301'),

    (SELECT course_id
     FROM courses
     WHERE course_code = 'CSE102')
    ),(
    (SELECT course_id
     FROM courses
     WHERE course_code = 'CSE202'),

    (SELECT course_id
     FROM courses
     WHERE course_code = 'CSE201')
    ),(

       (SELECT course_id
         FROM courses
         WHERE course_code = 'CSE202'),
        (SELECT course_id
         FROM courses
         WHERE course_code = 'MATH201')
    ),(

       (SELECT course_id
         FROM courses
         WHERE course_code = 'CSE302'),
        (SELECT course_id
         FROM courses
         WHERE course_code = 'CSE202')
    ),(

       (SELECT course_id
         FROM courses
         WHERE course_code = 'CSE302'),
        (SELECT course_id
         FROM courses
         WHERE course_code = 'STAT201')
    ),(

       (SELECT course_id
         FROM courses
         WHERE course_code = 'CSE303'),
        (SELECT course_id
         FROM courses
         WHERE course_code = 'CSE302')
    );

INSERT INTO course_sections (course_id, section_code)
SELECT
    c.course_id,
    s.section_code
FROM courses c
CROSS JOIN (
    VALUES ('01'), ('02')
) AS s(section_code)
WHERE c.course_code IN (
    'CSE101',
    'CSE102',
    'CSE201',
    'CSE202',
    'CSE301',
    'CSE302',
    'CSE303',
    'MATH101',
    'MATH201',
    'STAT201'
);

INSERT INTO section_meetings (
    section_id,
    day_of_week,
    start_time,
    end_time
)
SELECT
    cs.section_id,
    m.day_of_week,
    m.start_time::TIME,
    m.end_time::TIME
FROM (
    VALUES
        -- CSE101
        ('CSE101', '01', 1, '09:00', '10:30'),
        ('CSE101', '01', 3, '09:00', '10:30'),
        ('CSE101', '02', 2, '11:00', '12:30'),
        ('CSE101', '02', 4, '11:00', '12:30'),

        -- CSE102
        ('CSE102', '01', 1, '09:00', '10:30'),
        ('CSE102', '01', 3, '09:00', '10:30'),
        ('CSE102', '02', 2, '13:00', '14:30'),
        ('CSE102', '02', 4, '13:00', '14:30'),

        -- CSE201
        ('CSE201', '01', 1, '11:00', '12:30'),
        ('CSE201', '01', 3, '11:00', '12:30'),
        ('CSE201', '02', 2, '09:00', '10:30'),
        ('CSE201', '02', 4, '09:00', '10:30'),

        -- CSE202
        ('CSE202', '01', 1, '13:00', '14:30'),
        ('CSE202', '01', 3, '13:00', '14:30'),
        ('CSE202', '02', 2, '11:00', '12:30'),
        ('CSE202', '02', 4, '11:00', '12:30'),

        -- CSE301
        ('CSE301', '01', 1, '11:00', '12:30'),
        ('CSE301', '01', 3, '11:00', '12:30'),
        ('CSE301', '02', 2, '13:00', '14:30'),
        ('CSE301', '02', 4, '13:00', '14:30'),

        -- CSE302
        ('CSE302', '01', 1, '15:00', '16:30'),
        ('CSE302', '01', 3, '15:00', '16:30'),
        ('CSE302', '02', 2, '09:00', '10:30'),
        ('CSE302', '02', 4, '09:00', '10:30'),

        -- CSE303
        ('CSE303', '01', 1, '15:00', '16:30'),
        ('CSE303', '01', 3, '15:00', '16:30'),
        ('CSE303', '02', 2, '15:00', '16:30'),
        ('CSE303', '02', 4, '15:00', '16:30'),

        -- MATH101
        ('MATH101', '01', 1, '09:00', '10:30'),
        ('MATH101', '01', 3, '09:00', '10:30'),
        ('MATH101', '02', 2, '15:00', '16:30'),
        ('MATH101', '02', 4, '15:00', '16:30'),

        -- MATH201
        ('MATH201', '01', 1, '13:00', '14:30'),
        ('MATH201', '01', 3, '13:00', '14:30'),
        ('MATH201', '02', 2, '09:00', '10:30'),
        ('MATH201', '02', 4, '09:00', '10:30'),

        -- STAT201
        ('STAT201', '01', 1, '11:00', '12:30'),
        ('STAT201', '01', 3, '11:00', '12:30'),
        ('STAT201', '02', 2, '11:00', '12:30'),
        ('STAT201', '02', 4, '11:00', '12:30')
) AS m(
    course_code,
    section_code,
    day_of_week,
    start_time,
    end_time
)
JOIN courses c
    ON c.course_code = m.course_code
JOIN course_sections cs
    ON cs.course_id = c.course_id
    AND cs.section_code = m.section_code;