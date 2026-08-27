CREATE TABLE courses (
    course_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    course_code VARCHAR(20) NOT NULL UNIQUE,

    course_name VARCHAR(120) NOT NULL,

    credits INTEGER NOT NULL
        CHECK (credits > 0),

    difficulty SMALLINT NOT NULL
        CHECK (difficulty BETWEEN 1 AND 5)
);


CREATE TABLE prerequisites (
    course_id INTEGER NOT NULL,

    prerequisite_id INTEGER NOT NULL,

    PRIMARY KEY (course_id, prerequisite_id),

    FOREIGN KEY (course_id)
        REFERENCES courses(course_id)
        ON DELETE CASCADE,

    FOREIGN KEY (prerequisite_id)
        REFERENCES courses(course_id)
        ON DELETE CASCADE,

    CHECK (course_id <> prerequisite_id)
);


CREATE TABLE course_sections (
    section_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    course_id INTEGER NOT NULL,

    section_code VARCHAR(20) NOT NULL,

    FOREIGN KEY (course_id)
        REFERENCES courses(course_id)
        ON DELETE CASCADE,

    UNIQUE (course_id, section_code)
);

CREATE TABLE section_meetings (
    meeting_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    section_id INTEGER NOT NULL,

    day_of_week SMALLINT NOT NULL,

    start_time TIME NOT NULL,

    end_time TIME NOT NULL,

    FOREIGN KEY (section_id)
        REFERENCES course_sections(section_id)
        ON DELETE CASCADE,

    CHECK(start_time<end_time),
    CHECK (day_of_week BETWEEN 1 AND 7)

);