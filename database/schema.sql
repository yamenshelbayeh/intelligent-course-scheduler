-- ============================================================
-- Intelligent Course Scheduler
-- University of Debrecen
-- Computer Science Engineering BSc - 2024 Curriculum
-- ============================================================


-- ============================================================
-- CLEAN OLD TABLES
-- ============================================================

-- Tables from the original version of the project
DROP TABLE IF EXISTS section_meetings CASCADE;
DROP TABLE IF EXISTS course_sections CASCADE;
DROP TABLE IF EXISTS prerequisites CASCADE;

-- Current schema
DROP TABLE IF EXISTS prerequisite_options CASCADE;
DROP TABLE IF EXISTS prerequisite_groups CASCADE;
DROP TABLE IF EXISTS course_rules CASCADE;
DROP TABLE IF EXISTS degree_requirements CASCADE;
DROP TABLE IF EXISTS courses CASCADE;


-- ============================================================
-- COURSES
-- ============================================================

CREATE TABLE courses (
    id SERIAL PRIMARY KEY,

    code VARCHAR(20) UNIQUE NOT NULL,

    name VARCHAR(150) NOT NULL,

    credits INTEGER NOT NULL
        CHECK (credits > 0),

    category VARCHAR(40) NOT NULL
        CHECK (
            category IN (
                'NATURAL_SCIENCE',
                'HUMAN_ECONOMIC',
                'COMPULSORY',
                'DIFFERENTIATED',
                'PROFESSIONAL_TRAINING',
                'THESIS',
                'FREE_CHOICE',
                'EXTRA'
            )
        ),

    -- Recommended semester from the curriculum.
    -- NULL is allowed for courses without a fixed
    -- recommended semester.
    recommended_semester INTEGER
        CHECK (
            recommended_semester IS NULL
            OR recommended_semester BETWEEN 1 AND 7
        ),

    -- Examples:
    -- 1 = first-period course
    -- 2 = second-period course
    -- I = occasionally announced / special period
    period VARCHAR(5),

    -- E  = exam
    -- S  = sign
    -- PM = practical mark
    assessment VARCHAR(20),

    -- TRUE:
    -- this exact course must be completed.
    --
    -- FALSE:
    -- course is optional and may instead contribute
    -- toward a category credit requirement.
    is_required BOOLEAN NOT NULL DEFAULT TRUE
);


-- ============================================================
-- PREREQUISITE GROUPS
-- ============================================================

-- A course may have multiple prerequisite groups.
--
-- ALL groups must be satisfied.
--
-- Multiple options inside ONE group represent OR.
--
-- Example:
--
-- Development of Embedded Systems requires:
--
-- Embedded Systems
-- AND
-- (Microcontrollers OR Programmable Logic Devices)
--
-- Group 1:
--     Embedded Systems
--
-- Group 2:
--     Microcontrollers
--     Programmable Logic Devices

CREATE TABLE prerequisite_groups (
    id SERIAL PRIMARY KEY,

    course_id INTEGER NOT NULL
        REFERENCES courses(id)
        ON DELETE CASCADE,

    group_number INTEGER NOT NULL
        CHECK (group_number > 0),

    UNIQUE (course_id, group_number)
);


-- ============================================================
-- PREREQUISITE OPTIONS
-- ============================================================

-- Options belonging to the same prerequisite group
-- represent alternatives.
--
-- Example:
--
-- Group 2:
--     Microcontrollers
--     Programmable Logic Devices
--
-- means:
--
-- Microcontrollers OR Programmable Logic Devices

CREATE TABLE prerequisite_options (
    group_id INTEGER NOT NULL
        REFERENCES prerequisite_groups(id)
        ON DELETE CASCADE,

    prerequisite_course_id INTEGER NOT NULL
        REFERENCES courses(id)
        ON DELETE CASCADE,

    PRIMARY KEY (
        group_id,
        prerequisite_course_id
    )
);


-- ============================================================
-- COURSE RULES
-- ============================================================

-- Used for requirements which cannot be represented
-- as normal course prerequisites.
--
-- Example:
-- Thesis 1 requires at least 100 completed credits.

CREATE TABLE course_rules (
    course_id INTEGER PRIMARY KEY
        REFERENCES courses(id)
        ON DELETE CASCADE,

    minimum_completed_credits INTEGER NOT NULL DEFAULT 0
        CHECK (minimum_completed_credits >= 0)
);


-- ============================================================
-- DEGREE REQUIREMENTS
-- ============================================================

-- Stores the credit requirement for each curriculum category.

CREATE TABLE degree_requirements (
    category VARCHAR(40) PRIMARY KEY
        CHECK (
            category IN (
                'NATURAL_SCIENCE',
                'HUMAN_ECONOMIC',
                'COMPULSORY',
                'DIFFERENTIATED',
                'PROFESSIONAL_TRAINING',
                'THESIS',
                'FREE_CHOICE',
                'EXTRA'
            )
        ),

    required_credits INTEGER NOT NULL
        CHECK (required_credits >= 0),

    -- TRUE:
    -- this category is added independently toward
    -- the 210-credit degree total.
    --
    -- FALSE:
    -- the requirement is mandatory, but its credits
    -- are already included inside another category.
    --
    -- Example:
    -- Professional Training is mandatory but its
    -- 12 credits are counted inside the
    -- Differentiated Knowledge requirement.
    counts_toward_degree BOOLEAN NOT NULL DEFAULT TRUE
);


-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX idx_courses_category
    ON courses(category);

CREATE INDEX idx_courses_semester
    ON courses(recommended_semester);

CREATE INDEX idx_courses_period
    ON courses(period);

CREATE INDEX idx_courses_required
    ON courses(is_required);

CREATE INDEX idx_prerequisite_groups_course
    ON prerequisite_groups(course_id);

CREATE INDEX idx_prerequisite_options_prerequisite
    ON prerequisite_options(prerequisite_course_id);