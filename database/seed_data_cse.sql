-- ============================================================
-- Computer Science Engineering BSc
-- University of Debrecen - 2024 Curriculum
-- ============================================================


-- ------------------------------------------------------------
-- DEGREE REQUIREMENTS
-- ------------------------------------------------------------

INSERT INTO degree_requirements
(category, required_credits, counts_toward_degree)
VALUES
('NATURAL_SCIENCE',        45, TRUE),
('HUMAN_ECONOMIC',         15, TRUE),python -m pytest -q
('COMPULSORY',             93, TRUE),
('DIFFERENTIATED',         30, TRUE),
('PROFESSIONAL_TRAINING',  12, FALSE),
('THESIS',                 15, TRUE),
('FREE_CHOICE',            12, TRUE);


-- ------------------------------------------------------------
-- NATURAL SCIENCE COURSES
-- ------------------------------------------------------------

INSERT INTO courses
(code, name, credits, category, recommended_semester, period, assessment, is_required)
VALUES

('INBMA0101-24',
 'Algorithms and Basics of Programming',
 3,
 'NATURAL_SCIENCE',
 1,
 '1',
 'PM',
 TRUE),

('INBMA0102-24',
 'Electronics',
 6,
 'NATURAL_SCIENCE',
 1,
 '1',
 'E',
 TRUE),

('INBMA0104-24',
 'Calculus',
 6,
 'NATURAL_SCIENCE',
 1,
 '1',
 'E',
 TRUE),

('INBMA0105-24',
 'Mathematics for Engineers 1',
 6,
 'NATURAL_SCIENCE',
 1,
 '1',
 'PM',
 TRUE),

('INBMA0203-24',
 'Physics',
 6,
 'NATURAL_SCIENCE',
 2,
 '2',
 'E',
 TRUE),

('INBMA0207-17',
 'Data Structures and Algorithms',
 6,
 'NATURAL_SCIENCE',
 2,
 '2',
 'E',
 TRUE),

('INBMA0208-24',
 'Mathematics for Engineers 2',
 6,
 'NATURAL_SCIENCE',
 2,
 '2',
 'E',
 TRUE),

('INBMA0313-17',
 'Probability Theory and Mathematical Statistics',
 6,
 'NATURAL_SCIENCE',
 3,
 '1',
 'PM',
 TRUE);


-- ------------------------------------------------------------
-- HUMAN AND ECONOMIC KNOWLEDGE
-- ------------------------------------------------------------

INSERT INTO courses
(code, name, credits, category, recommended_semester, period, assessment, is_required)
VALUES

('INBMA0314-17',
 'Economics',
 6,
 'HUMAN_ECONOMIC',
 3,
 '1',
 'E',
 TRUE),

('INBMA0531-21',
 'Fundamentals of Business Law',
 3,
 'HUMAN_ECONOMIC',
 5,
 '1',
 'E',
 TRUE),

('INBMA0632-17',
 'Management Basics for Engineers',
 6,
 'HUMAN_ECONOMIC',
 6,
 '2',
 'E',
 TRUE);


-- ------------------------------------------------------------
-- COMPULSORY TOPICS
-- ------------------------------------------------------------

INSERT INTO courses
(code, name, credits, category, recommended_semester, period, assessment, is_required)
VALUES

('INBMA0106-24',
 'Introduction into Logic and Computer Science',
 6,
 'COMPULSORY',
 1,
 '1',
 'E',
 TRUE),

('INBMA0120-24',
 'Operating Systems',
 3,
 'COMPULSORY',
 1,
 '1',
 'PM',
 TRUE),

('INBMA0209-24',
 'Digital Design',
 6,
 'COMPULSORY',
 2,
 '2',
 'E',
 TRUE),

('INBMA0211-21',
 'Programming Languages 1',
 6,
 'COMPULSORY',
 2,
 '2',
 'E',
 TRUE),

('INBMA0315-17',
 'Signals and Systems',
 3,
 'COMPULSORY',
 3,
 '1',
 'PM',
 TRUE),

('INBMA0316-17',
 'Introduction to Graphical Programming Environment',
 3,
 'COMPULSORY',
 3,
 '1',
 'PM',
 TRUE),

('INBMA0317-21',
 'Programming Languages 2',
 6,
 'COMPULSORY',
 3,
 '1',
 'PM',
 TRUE),

('INBMA0318-17',
 'Computer Networks',
 6,
 'COMPULSORY',
 3,
 '1',
 'E',
 TRUE),

('INBMA0412-21',
 'Computer Architectures',
 3,
 'COMPULSORY',
 4,
 '2',
 'E',
 TRUE),

('INBMA0419-17',
 'Management of Data Network Systems',
 3,
 'COMPULSORY',
 4,
 '2',
 'E',
 TRUE),

('INBMA0421-24',
 'System Programming',
 3,
 'COMPULSORY',
 4,
 '2',
 'PM',
 TRUE),

('INBMA0422-21',
 'Control Systems',
 3,
 'COMPULSORY',
 4,
 '2',
 'PM',
 TRUE),

('INBMA0424-17',
 'Enterprise Information Systems',
 3,
 'COMPULSORY',
 4,
 '2',
 'E',
 TRUE),

('INBMA0425-17',
 'Web Solutions',
 3,
 'COMPULSORY',
 4,
 '2',
 'PM',
 TRUE),

('INBMA0433-21',
 'Database Systems and Knowledge Representation',
 6,
 'COMPULSORY',
 4,
 '2',
 'PM',
 TRUE),

('INBMA0434-24',
 'IT Security',
 3,
 'COMPULSORY',
 4,
 '2',
 'PM',
 TRUE),

('INBMA0435-24',
 'Computer Graphics',
 3,
 'COMPULSORY',
 4,
 '2',
 'PM',
 TRUE),

('INBMA0523-21',
 'Software Development for Engineers',
 6,
 'COMPULSORY',
 5,
 '1',
 'E',
 TRUE),

('INBMA0526-24',
 'Introduction into Artificial Intelligence',
 6,
 'COMPULSORY',
 5,
 '1',
 'E',
 TRUE),

('INBMA0527-17',
 'Assembly Programming',
 3,
 'COMPULSORY',
 5,
 '1',
 'PM',
 TRUE),

('INBMA0528-17',
 'Embedded Systems',
 6,
 'COMPULSORY',
 5,
 '1',
 'E',
 TRUE),

('INBMA0630-21',
 'Mobile Solutions',
 3,
 'COMPULSORY',
 6,
 '2',
 'PM',
 TRUE);

-- ------------------------------------------------------------
-- THESIS
-- ------------------------------------------------------------

INSERT INTO courses
(code, name, credits, category, recommended_semester, period, assessment, is_required)
VALUES

('INBMA0636-21',
 'Thesis 1',
 6,
 'THESIS',
 6,
 '2',
 'PM',
 TRUE),

('INBMA0736-21',
 'Thesis 2',
 9,
 'THESIS',
 7,
 '1',
 'PM',
 TRUE);


-- ------------------------------------------------------------
-- PROFESSIONAL TRAINING
-- ------------------------------------------------------------

INSERT INTO courses
(code, name, credits, category, recommended_semester, period, assessment, is_required)
VALUES

('INBMA9997-21',
 'Professional Training',
 12,
 'PROFESSIONAL_TRAINING',
 6,
 'I',
 'PM',
 TRUE);


-- ------------------------------------------------------------
-- DIFFERENTIATED KNOWLEDGE TOPICS
--
-- Only 30 credits are required from this category,
-- so these are NOT individually required.
-- ------------------------------------------------------------

INSERT INTO courses
(code, name, credits, category, recommended_semester, period, assessment, is_required)
VALUES

('INBMA9937-17',
 'Microcontrollers',
 6,
 'DIFFERENTIATED',
 4,
 '2',
 'PM',
 FALSE),

('INBMA9946-17',
 'Fundamentals of Information and Coding Theory',
 3,
 'DIFFERENTIATED',
 4,
 '2',
 'E',
 FALSE),

('INBMA9929-24',
 'Modeling and Analysis of Information Technology Systems',
 3,
 'DIFFERENTIATED',
 5,
 '1',
 'PM',
 FALSE),

('INBMA9938-21',
 'Programming Network Devices 1',
 6,
 'DIFFERENTIATED',
 5,
 '1',
 'PM',
 FALSE),

('INBMA9939-17',
 'Programmable Logic Devices',
 6,
 'DIFFERENTIATED',
 5,
 '1',
 'PM',
 FALSE),

('INBMA9945-17',
 'Scripting Languages',
 3,
 'DIFFERENTIATED',
 5,
 '1',
 'PM',
 FALSE),

('INBMA9940-17',
 'Development of Embedded Systems',
 6,
 'DIFFERENTIATED',
 6,
 '2',
 'PM',
 FALSE),

('INBMA9941-21',
 'Programming Network Devices 2',
 6,
 'DIFFERENTIATED',
 6,
 '2',
 'PM',
 FALSE),

('INBMA9942-17',
 'Modeling and Performance Evaluation of Networks',
 6,
 'DIFFERENTIATED',
 6,
 '2',
 'PM',
 FALSE),

('INBMA9943-17',
 'Telecommunication Systems',
 6,
 'DIFFERENTIATED',
 6,
 '2',
 'PM',
 FALSE),

('INBMA9947-17',
 'Introduction to Cloud Technologies',
 3,
 'DIFFERENTIATED',
 6,
 '2',
 'PM',
 FALSE),

('INBMA9944-17',
 'Sensors and Actuators Network',
 6,
 'DIFFERENTIATED',
 7,
 '1',
 'PM',
 FALSE),

('INBMA9951-17',
 'Basics of Autonomous Vehicles Development',
 6,
 'DIFFERENTIATED',
 NULL,
 'I',
 'PM',
 FALSE),

('INBMA9952-17',
 'Ethical Hacking I',
 3,
 'DIFFERENTIATED',
 NULL,
 'I',
 'PM',
 FALSE),

('INBMA9953-17',
 'Blockchain Technology',
 3,
 'DIFFERENTIATED',
 NULL,
 'I',
 'E',
 FALSE),

('INBMA9958-17',
 'Introduction to the AWS Cloud',
 3,
 'DIFFERENTIATED',
 NULL,
 'I',
 'PM',
 FALSE),

('INBMA9959-21',
 'Network and System Security',
 3,
 'DIFFERENTIATED',
 NULL,
 'I',
 'PM',
 FALSE),

('INBMA9960-21',
 'Ethical Hacking 2',
 3,
 'DIFFERENTIATED',
 NULL,
 'I',
 'PM',
 FALSE),

('INBMA9961-21',
 'DevSecOps',
 3,
 'DIFFERENTIATED',
 NULL,
 'I',
 'PM',
 FALSE),

('INBMA9962-21',
 'Bioinformatics for Engineers',
 3,
 'DIFFERENTIATED',
 NULL,
 'I',
 'PM',
 FALSE),

('INBMA9963-21',
 'Introduction to Quantum Computing',
 3,
 'DIFFERENTIATED',
 NULL,
 'I',
 'PM',
 FALSE),

('INBMA9964-21',
 'Introduction to Generative AI',
 3,
 'DIFFERENTIATED',
 NULL,
 'I',
 'PM',
 FALSE);

-- ============================================================
-- PREREQUISITES
-- ============================================================

-- ------------------------------------------------------------
-- REQUIRED / CORE COURSE PREREQUISITES
--
-- Different group numbers = AND
-- Same group number = OR
-- ------------------------------------------------------------


-- ============================================================
-- STEP 1: CREATE PREREQUISITE GROUPS
-- ============================================================

WITH prerequisite_data(course_code, group_number) AS (
    VALUES

    -- Natural Science

    -- Mathematics for Engineers 2
    ('INBMA0208-24', 1),
    ('INBMA0208-24', 2),

    -- Probability Theory and Mathematical Statistics
    ('INBMA0313-17', 1),
    ('INBMA0313-17', 2),


    -- Compulsory Courses

    -- Digital Design
    ('INBMA0209-24', 1),

    -- Programming Languages 1
    ('INBMA0211-21', 1),

    -- Signals and Systems
    ('INBMA0315-17', 1),
    ('INBMA0315-17', 2),

    -- Introduction to Graphical Programming Environment
    ('INBMA0316-17', 1),

    -- Programming Languages 2
    ('INBMA0317-21', 1),

    -- Computer Networks
    ('INBMA0318-17', 1),

    -- Computer Architectures
    ('INBMA0412-21', 1),

    -- Management of Data Network Systems
    ('INBMA0419-17', 1),

    -- System Programming
    ('INBMA0421-24', 1),

    -- Control Systems
    ('INBMA0422-21', 1),

    -- Web Solutions
    ('INBMA0425-17', 1),

    -- Database Systems and Knowledge Representation
    ('INBMA0433-21', 1),

    -- IT Security
    ('INBMA0434-24', 1),

    -- Computer Graphics
    ('INBMA0435-24', 1),

    -- Software Development for Engineers
    ('INBMA0523-21', 1),

    -- Assembly Programming
    ('INBMA0527-17', 1),
    ('INBMA0527-17', 2),

    -- Embedded Systems
    ('INBMA0528-17', 1),
    ('INBMA0528-17', 2),

    -- Introduction into Artificial Intelligence
    ('INBMA0526-24', 1),
    ('INBMA0526-24', 2),
    ('INBMA0526-24', 3),

    -- Mobile Solutions
    ('INBMA0630-21', 1)
)

INSERT INTO prerequisite_groups (
    course_id,
    group_number
)

SELECT DISTINCT
    c.id,
    p.group_number

FROM prerequisite_data p

JOIN courses c
    ON c.code = p.course_code

ON CONFLICT (course_id, group_number)
DO NOTHING;



-- ============================================================
-- STEP 2: INSERT PREREQUISITE OPTIONS
-- ============================================================

WITH prerequisite_data(course_code, group_number, prerequisite_code) AS (
    VALUES

    -- Natural Science

    -- Mathematics for Engineers 2
    ('INBMA0208-24', 1, 'INBMA0104-24'),
    ('INBMA0208-24', 2, 'INBMA0105-24'),

    -- Probability Theory and Mathematical Statistics
    ('INBMA0313-17', 1, 'INBMA0104-24'),
    ('INBMA0313-17', 2, 'INBMA0105-24'),


    -- Compulsory Courses

    -- Digital Design
    ('INBMA0209-24', 1, 'INBMA0102-24'),

    -- Programming Languages 1
    ('INBMA0211-21', 1, 'INBMA0101-24'),

    -- Signals and Systems
    ('INBMA0315-17', 1, 'INBMA0102-24'),
    ('INBMA0315-17', 2, 'INBMA0208-24'),

    -- Introduction to Graphical Programming Environment
    ('INBMA0316-17', 1, 'INBMA0101-24'),

    -- Programming Languages 2
    ('INBMA0317-21', 1, 'INBMA0211-21'),

    -- Computer Networks
    ('INBMA0318-17', 1, 'INBMA0120-24'),

    -- Computer Architectures
    ('INBMA0412-21', 1, 'INBMA0209-24'),

    -- Management of Data Network Systems
    ('INBMA0419-17', 1, 'INBMA0318-17'),

    -- System Programming
    ('INBMA0421-24', 1, 'INBMA0211-21'),

    -- Control Systems
    ('INBMA0422-21', 1, 'INBMA0315-17'),

    -- Web Solutions
    ('INBMA0425-17', 1, 'INBMA0211-21'),

    -- Database Systems and Knowledge Representation
    ('INBMA0433-21', 1, 'INBMA0211-21'),

    -- IT Security
    ('INBMA0434-24', 1, 'INBMA0120-24'),

    -- Computer Graphics
    ('INBMA0435-24', 1, 'INBMA0211-21'),

    -- Software Development for Engineers
    ('INBMA0523-21', 1, 'INBMA0317-21'),

    -- Assembly Programming
    ('INBMA0527-17', 1, 'INBMA0211-21'),
    ('INBMA0527-17', 2, 'INBMA0412-21'),

    -- Embedded Systems
    ('INBMA0528-17', 1, 'INBMA0211-21'),
    ('INBMA0528-17', 2, 'INBMA0412-21'),

    -- Introduction into Artificial Intelligence
    ('INBMA0526-24', 1, 'INBMA0106-24'),
    ('INBMA0526-24', 2, 'INBMA0207-17'),
    ('INBMA0526-24', 3, 'INBMA0211-21'),

    -- Mobile Solutions
    ('INBMA0630-21', 1, 'INBMA0317-21')
)

INSERT INTO prerequisite_options (
    group_id,
    prerequisite_course_id
)

SELECT
    pg.id,
    prereq.id

FROM prerequisite_data p

JOIN courses course
    ON course.code = p.course_code

JOIN prerequisite_groups pg
    ON pg.course_id = course.id
   AND pg.group_number = p.group_number

JOIN courses prereq
    ON prereq.code = p.prerequisite_code

ON CONFLICT DO NOTHING;

-- ============================================================
-- DIFFERENTIATED / PROFESSIONAL PREREQUISITES
-- ============================================================

-- ------------------------------------------------------------
-- STEP 1: CREATE PREREQUISITE GROUPS
-- ------------------------------------------------------------

WITH prerequisite_data(course_code, group_number) AS (
    VALUES

    -- Microcontrollers
    ('INBMA9937-17', 1),
    ('INBMA9937-17', 2),

    -- Fundamentals of Information and Coding Theory
    ('INBMA9946-17', 1),

    -- Modeling and Analysis of Information Technology Systems
    ('INBMA9929-24', 1),

    -- Programming Network Devices 1
    ('INBMA9938-21', 1),

    -- Programmable Logic Devices
    ('INBMA9939-17', 1),
    ('INBMA9939-17', 2),

    -- Scripting Languages
    ('INBMA9945-17', 1),

    -- Development of Embedded Systems
    ('INBMA9940-17', 1),
    ('INBMA9940-17', 2),

    -- Programming Network Devices 2
    ('INBMA9941-21', 1),

    -- Modeling and Performance Evaluation of Networks
    ('INBMA9942-17', 1),

    -- Telecommunication Systems
    ('INBMA9943-17', 1),

    -- Introduction to Cloud Technologies
    ('INBMA9947-17', 1),

    -- Professional Training
    ('INBMA9997-21', 1),
    ('INBMA9997-21', 2),

    -- Sensors and Actuators Network
    ('INBMA9944-17', 1),
    ('INBMA9944-17', 2),

    -- Basics of Autonomous Vehicles Development
    ('INBMA9951-17', 1),

    -- Ethical Hacking I
    ('INBMA9952-17', 1),

    -- Network and System Security
    ('INBMA9959-21', 1),

    -- Ethical Hacking 2
    ('INBMA9960-21', 1),

    -- DevSecOps
    ('INBMA9961-21', 1),

    -- Introduction to Quantum Computing
    ('INBMA9963-21', 1),
    ('INBMA9963-21', 2),
    ('INBMA9963-21', 3)
)

INSERT INTO prerequisite_groups (
    course_id,
    group_number
)

SELECT
    c.id,
    p.group_number

FROM prerequisite_data p

JOIN courses c
    ON c.code = p.course_code

ON CONFLICT (course_id, group_number)
DO NOTHING;

-- ============================================================
-- DIFFERENTIATED / PROFESSIONAL PREREQUISITES
-- ============================================================

-- ------------------------------------------------------------
-- STEP 1: CREATE PREREQUISITE GROUPS
-- ------------------------------------------------------------

WITH prerequisite_data(course_code, group_number) AS (
    VALUES

    -- Microcontrollers
    ('INBMA9937-17', 1),
    ('INBMA9937-17', 2),

    -- Fundamentals of Information and Coding Theory
    ('INBMA9946-17', 1),

    -- Modeling and Analysis of Information Technology Systems
    ('INBMA9929-24', 1),

    -- Programming Network Devices 1
    ('INBMA9938-21', 1),

    -- Programmable Logic Devices
    ('INBMA9939-17', 1),
    ('INBMA9939-17', 2),

    -- Scripting Languages
    ('INBMA9945-17', 1),

    -- Development of Embedded Systems
    ('INBMA9940-17', 1),
    ('INBMA9940-17', 2),

    -- Programming Network Devices 2
    ('INBMA9941-21', 1),

    -- Modeling and Performance Evaluation of Networks
    ('INBMA9942-17', 1),

    -- Telecommunication Systems
    ('INBMA9943-17', 1),

    -- Introduction to Cloud Technologies
    ('INBMA9947-17', 1),

    -- Professional Training
    ('INBMA9997-21', 1),
    ('INBMA9997-21', 2),

    -- Sensors and Actuators Network
    ('INBMA9944-17', 1),
    ('INBMA9944-17', 2),

    -- Basics of Autonomous Vehicles Development
    ('INBMA9951-17', 1),

    -- Ethical Hacking I
    ('INBMA9952-17', 1),

    -- Network and System Security
    ('INBMA9959-21', 1),

    -- Ethical Hacking 2
    ('INBMA9960-21', 1),

    -- DevSecOps
    ('INBMA9961-21', 1),

    -- Introduction to Quantum Computing
    ('INBMA9963-21', 1),
    ('INBMA9963-21', 2),
    ('INBMA9963-21', 3)
)

INSERT INTO prerequisite_groups (
    course_id,
    group_number
)

SELECT
    c.id,
    p.group_number

FROM prerequisite_data p

JOIN courses c
    ON c.code = p.course_code

ON CONFLICT (course_id, group_number)
DO NOTHING;


-- ------------------------------------------------------------
-- STEP 2: INSERT PREREQUISITE OPTIONS
-- ------------------------------------------------------------

WITH prerequisite_data(course_code, group_number, prerequisite_code) AS (
    VALUES

    -- Microcontrollers
    ('INBMA9937-17', 1, 'INBMA0209-24'),
    ('INBMA9937-17', 2, 'INBMA0211-21'),

    -- Fundamentals of Information and Coding Theory
    ('INBMA9946-17', 1, 'INBMA0313-17'),

    -- Modeling and Analysis of Information Technology Systems
    ('INBMA9929-24', 1, 'INBMA0313-17'),

    -- Programming Network Devices 1
    ('INBMA9938-21', 1, 'INBMA0318-17'),

    -- Programmable Logic Devices
    ('INBMA9939-17', 1, 'INBMA0209-24'),
    ('INBMA9939-17', 2, 'INBMA0211-21'),

    -- Scripting Languages
    ('INBMA9945-17', 1, 'INBMA0211-21'),

    -- Development of Embedded Systems
    -- Must have Embedded Systems
    ('INBMA9940-17', 1, 'INBMA0528-17'),

    -- AND either Microcontrollers OR Programmable Logic Devices
    ('INBMA9940-17', 2, 'INBMA9937-17'),
    ('INBMA9940-17', 2, 'INBMA9939-17'),

    -- Programming Network Devices 2
    ('INBMA9941-21', 1, 'INBMA9938-21'),

    -- Modeling and Performance Evaluation of Networks
    ('INBMA9942-17', 1, 'INBMA9929-24'),

    -- Telecommunication Systems
    ('INBMA9943-17', 1, 'INBMA0318-17'),

    -- Introduction to Cloud Technologies
    ('INBMA9947-17', 1, 'INBMA0211-21'),

    -- Professional Training
    ('INBMA9997-21', 1, 'INBMA0317-21'),
    ('INBMA9997-21', 2, 'INBMA0318-17'),

    -- Sensors and Actuators Network
    ('INBMA9944-17', 1, 'INBMA0318-17'),
    ('INBMA9944-17', 2, 'INBMA9937-17'),

    -- Basics of Autonomous Vehicles Development
    ('INBMA9951-17', 1, 'INBMA0211-21'),

    -- Ethical Hacking I
    ('INBMA9952-17', 1, 'INBMA0211-21'),

    -- Network and System Security
    ('INBMA9959-21', 1, 'INBMA0120-24'),

    -- Ethical Hacking 2
    ('INBMA9960-21', 1, 'INBMA9952-17'),

    -- DevSecOps
    ('INBMA9961-21', 1, 'INBMA0120-24'),

    -- Introduction to Quantum Computing
    ('INBMA9963-21', 1, 'INBMA0104-24'),
    ('INBMA9963-21', 2, 'INBMA0208-24'),
    ('INBMA9963-21', 3, 'INBMA0211-21')
)

INSERT INTO prerequisite_options (
    group_id,
    prerequisite_course_id
)

SELECT
    pg.id,
    prereq.id

FROM prerequisite_data p

JOIN courses course
    ON course.code = p.course_code

JOIN prerequisite_groups pg
    ON pg.course_id = course.id
   AND pg.group_number = p.group_number

JOIN courses prereq
    ON prereq.code = p.prerequisite_code

ON CONFLICT DO NOTHING;

-- ============================================================
-- SPECIAL COURSE RULES
-- ============================================================

-- Thesis 1 requires at least 100 completed credits.

INSERT INTO course_rules (
    course_id,
    minimum_completed_credits
)

SELECT
    id,
    100

FROM courses

WHERE code = 'INBMA0636-21'

ON CONFLICT (course_id)
DO UPDATE SET
    minimum_completed_credits = EXCLUDED.minimum_completed_credits;

