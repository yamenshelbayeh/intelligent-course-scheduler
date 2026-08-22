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
