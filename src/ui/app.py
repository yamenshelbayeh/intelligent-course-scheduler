from pathlib import Path
import sys

import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from src.db import load_curriculum

from src.ai.advisor import build_advisor_report

from src.ai.pathfinder import (
    a_star_degree_plan,
    validate_plan,
    course_available_in_semester,
    differentiated_credits
)


st.set_page_config(
    page_title="Intelligent Degree Planner",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)


st.markdown(
    """
    <style>

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    [data-testid="stMainBlockContainer"] {
        padding-top: 2rem;
    }

    h1 {
        font-size: 3rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.04em;
        margin-bottom: 0.25rem !important;
    }

    h2 {
        font-size: 1.65rem !important;
        font-weight: 750 !important;
        letter-spacing: -0.02em;
        margin-top: 2.5rem !important;
        margin-bottom: 1rem !important;
    }

    h3 {
        font-weight: 700 !important;
        letter-spacing: -0.015em;
    }

    p {
        line-height: 1.6;
    }

    label {
        font-weight: 600 !important;
    }

    .stButton > button {
        width: 100%;
        min-height: 3rem;
        border-radius: 12px;
        font-size: 1rem;
        font-weight: 700;
        padding: 0.7rem 1rem;
        transition:
            transform 0.15s ease,
            box-shadow 0.15s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.12);
    }

    [data-testid="stMetric"] {
        background: var(--secondary-background-color);
        border: 1px solid rgba(150, 150, 150, 0.18);
        border-radius: 16px;
        padding: 1.2rem 1.25rem;
        min-height: 120px;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--secondary-background-color);
        border-radius: 16px !important;
        border-color: rgba(150, 150, 150, 0.18) !important;
    }

    [data-testid="stExpander"] {
        background: var(--secondary-background-color);
        border: 1px solid rgba(150, 150, 150, 0.18);
        border-radius: 14px;
        margin-bottom: 0.8rem;
        overflow: hidden;
    }

    [data-testid="stDataFrame"] {
        margin-top: 0.8rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(150, 150, 150, 0.15);
        border-radius: 12px;
        overflow: hidden;
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    hr {
        margin-top: 2.2rem !important;
        margin-bottom: 2.2rem !important;
        opacity: 0.15;
    }

    @media (max-width: 768px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        h1 {
            font-size: 2.2rem !important;
        }

        h2 {
            font-size: 1.4rem !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


@st.cache_data
def get_curriculum():
    return load_curriculum()


try:
    curriculum = get_curriculum()

except Exception as error:

    st.error(
        "Could not load the curriculum from PostgreSQL."
    )

    st.code(str(error))

    st.stop()


course_data = curriculum["courses"]
prerequisites = curriculum["prerequisites"]
degree_requirements = curriculum["degree_requirements"]
course_rules = curriculum["course_rules"]


def course_label(code):

    data = course_data[code]

    return (
        f"{code} — {data['name']} "
        f"({data['credits']} credits)"
    )


def completed_credit_total(completed):

    return sum(
        course_data[code]["credits"]
        for code in completed
        if code in course_data
    )


course_codes = sorted(
    course_data,
    key=lambda code: (
        course_data[code]["recommended_semester"]
        if course_data[code]["recommended_semester"] is not None
        else 99,
        code
    )
)


st.markdown(
    """
    <h1>🎓 Intelligent Degree Planner</h1>

    <p style="
        font-size: 1.15rem;
        opacity: 0.68;
        max-width: 800px;
        margin-top: 0;
        margin-bottom: 2.2rem;
    ">
        AI-powered degree pathway planning for the
        University of Debrecen Computer Science Engineering BSc.
        The system uses A* search, curriculum constraints,
        prerequisite reasoning and PostgreSQL.
    </p>
    """,
    unsafe_allow_html=True
)


completed = st.multiselect(
    "Completed courses",
    options=course_codes,
    format_func=course_label,
    help=(
        "Select courses already completed. "
        "They will not appear again in the generated plan."
    )
)


input_col1, input_col2 = st.columns(2)


with input_col1:

    start_semester = st.selectbox(
        "Next curriculum semester",
        options=list(range(1, 8)),
        index=0,
        help=(
            "Semester 1 means planning from the beginning "
            "of the degree."
        )
    )


with input_col2:

    max_credits = st.number_input(
        "Planning credit cap per semester",
        min_value=1,
        value=30,
        step=1,
        help=(
            "Choose the maximum number of credits the planner "
            "should place in one semester. Values above 30 are allowed."
        )
    )


generate = st.button(
    "Generate AI Degree Plan",
    type="primary",
    use_container_width=True
)


# ============================================================
# GENERATE PLAN
# ============================================================

if generate:

    completed_snapshot = list(completed)

    with st.spinner(
        "Searching for a valid degree pathway..."
    ):

        plan, expanded_states, initial_h = (
            a_star_degree_plan(
                prerequisite_groups=prerequisites,
                course_data=course_data,
                course_rules=course_rules,
                degree_requirements=degree_requirements,
                completed=set(completed_snapshot),
                start_semester=start_semester,
                max_credits=max_credits
            )
        )


        if plan is None:

            st.error(
                "No valid degree plan could be generated "
                "with these settings."
            )

            st.stop()


        valid, validation_errors = validate_plan(
            plan=plan,
            prerequisite_groups=prerequisites,
            course_data=course_data,
            course_rules=course_rules,
            degree_requirements=degree_requirements,
            completed=set(completed_snapshot),
            start_semester=start_semester,
            max_credits=max_credits
        )


        advisor = build_advisor_report(
            prerequisites,
            set(completed_snapshot),
            course_data,
            course_rules
        )


        planned_courses = {
            code
            for semester in plan
            for code in semester
        }


        planned_credits = sum(
            course_data[code]["credits"]
            for code in planned_courses
        )


        final_state = (
            set(completed_snapshot)
            | planned_courses
        )


        final_differentiated_credits = (
            differentiated_credits(
                final_state,
                course_data
            )
        )


        current_recommendations = [
            recommendation
            for recommendation
            in advisor["recommendations"]
            if course_available_in_semester(
                recommendation["course"],
                course_data,
                start_semester
            )
        ]


        st.session_state["planner_result"] = {
            "plan": plan,
            "expanded_states": expanded_states,
            "initial_h": initial_h,
            "valid": valid,
            "validation_errors": validation_errors,
            "advisor": advisor,
            "current_recommendations":
                current_recommendations,
            "planned_credits": planned_credits,
            "completed": completed_snapshot,
            "completed_credits":
                completed_credit_total(
                    completed_snapshot
                ),
            "final_differentiated_credits":
                final_differentiated_credits,
            "start_semester": start_semester,
            "max_credits": max_credits
        }


# ============================================================
# RESULTS
# ============================================================

if "planner_result" in st.session_state:

    result = st.session_state["planner_result"]

    plan = result["plan"]
    advisor = result["advisor"]

    current_recommendations = result[
        "current_recommendations"
    ]

    start_semester = result["start_semester"]
    max_credits = result["max_credits"]

    generated_completed = result["completed"]


    st.success(
        "Valid degree plan generated successfully."
    )


    # ========================================================
    # MAIN METRICS
    # ========================================================

    metric1, metric2, metric3, metric4 = (
        st.columns(4)
    )


    metric1.metric(
        "Completed Courses",
        len(generated_completed)
    )


    metric2.metric(
        "Remaining Semesters",
        len(plan)
    )


    metric3.metric(
        "Credits Planned",
        result["planned_credits"]
    )


    metric4.metric(
        "A* Expanded States",
        result["expanded_states"]
    )


    st.caption(
        f"{len(course_data)} curriculum courses "
        "loaded from PostgreSQL."
    )


    st.divider()


    # ========================================================
    # ACADEMIC ADVISOR
    # ========================================================

    st.subheader("🧭 Academic Advisor")

    st.write(
        f"Courses below are currently eligible by "
        f"prerequisites and available in Semester "
        f"{start_semester}."
    )


    if current_recommendations:

        for rank, recommendation in enumerate(
            current_recommendations[:5],
            start=1
        ):

            with st.container(border=True):

                title_col, credits_col = (
                    st.columns([4, 1])
                )


                with title_col:

                    if rank == 1:

                        st.markdown(
                            f"### ⭐ "
                            f"{recommendation['course']} "
                            f"— {recommendation['name']}"
                        )

                        st.caption(
                            "Top prerequisite-impact "
                            "recommendation"
                        )

                    else:

                        st.markdown(
                            f"### "
                            f"{recommendation['course']} "
                            f"— {recommendation['name']}"
                        )


                    st.caption(
                        recommendation["category"]
                        .replace("_", " ")
                        .title()
                    )


                with credits_col:

                    st.metric(
                        "Credits",
                        recommendation["credits"]
                    )


                unlock_col1, unlock_col2 = (
                    st.columns(2)
                )


                with unlock_col1:

                    st.markdown(
                        "**Direct Unlocks**"
                    )


                    if recommendation["unlocks"]:

                        for code in recommendation[
                            "unlocks"
                        ]:

                            st.write(
                                f"• {code} — "
                                f"{course_data[code]['name']}"
                            )

                    else:

                        st.write("None")


                with unlock_col2:

                    st.markdown(
                        "**Downstream Courses**"
                    )

                    st.write(
                        f"{recommendation['future_unlock_count']} "
                        "unfinished course(s) depend "
                        "on this prerequisite path."
                    )


                with st.expander(
                    "Why is this recommended?"
                ):

                    st.write(
                        recommendation[
                            "explanation"
                        ]
                    )


    else:

        st.info(
            "No advisor recommendations are "
            "available for this semester."
        )


    st.divider()


    # ========================================================
    # DEGREE PLAN
    # ========================================================

    st.subheader(
        "🗺️ AI-Generated Degree Plan"
    )


    for offset, semester_courses in enumerate(
        plan
    ):

        semester_number = (
            start_semester + offset
        )


        semester_credits = sum(
            course_data[code]["credits"]
            for code in semester_courses
        )


        with st.expander(
            (
                f"Semester {semester_number} "
                f"— {semester_credits} credits"
            ),
            expanded=(offset == 0)
        ):


            if not semester_courses:

                st.info(
                    "No curriculum courses planned "
                    "for this semester."
                )

                continue


            rows = []


            for code in semester_courses:

                info = course_data[code]

                rows.append({
                    "Code": code,
                    "Course": info["name"],
                    "Credits": info["credits"],
                    "Category": (
                        info["category"]
                        .replace("_", " ")
                        .title()
                    )
                })


            st.dataframe(
                rows,
                use_container_width=True,
                hide_index=True
            )


    st.divider()


    # ========================================================
    # DEGREE PROGRESS
    # ========================================================

    st.subheader("📊 Degree Progress")


    progress1, progress2, progress3, progress4 = (
        st.columns(4)
    )


    progress1.metric(
        "Already Completed",
        f"{result['completed_credits']} credits"
    )


    progress2.metric(
        "Remaining Plan",
        f"{result['planned_credits']} credits"
    )


    progress3.metric(
        "Differentiated Block",
        (
            f"{result['final_differentiated_credits']}"
            " / 30 credits"
        )
    )


    progress4.metric(
        "Free Choice",
        "12 credits"
    )


    st.caption(
        "The curriculum defines 12 free-choice credits "
        "without prescribing fixed courses. "
        "They are therefore reported separately "
        "instead of being selected automatically."
    )


    st.divider()


    # ========================================================
    # BLOCKED COURSE EXPLAINER
    # ========================================================

    st.subheader(
        "🔒 Why Is a Course Blocked?"
    )


    blocked = advisor["blocked"]


    if blocked:

        blocked_course = st.selectbox(
            "Select a blocked course",
            options=sorted(blocked),
            format_func=course_label
        )


        details = blocked[blocked_course]


        with st.container(border=True):

            st.markdown(
                f"### {course_label(blocked_course)}"
            )


            missing_groups = details[
                "missing_prerequisite_groups"
            ]


            if missing_groups:

                st.markdown(
                    "**Missing prerequisite requirements**"
                )


                for group in missing_groups:

                    if len(group) == 1:

                        code = group[0]

                        st.write(
                            f"• {course_label(code)}"
                        )

                    else:

                        options = " OR ".join(
                            course_label(code)
                            for code in group
                        )

                        st.write(
                            f"• One of: {options}"
                        )


            minimum_credits = details.get(
                "minimum_completed_credits"
            )


            if minimum_credits is not None:

                st.write(
                    f"• Requires at least "
                    f"{minimum_credits} "
                    "completed credits."
                )


            if details["prerequisite_chain"]:

                with st.expander(
                    "Remaining prerequisite chain"
                ):

                    for code in details[
                        "prerequisite_chain"
                    ]:

                        st.write(
                            f"• {course_label(code)}"
                        )


            st.markdown(
                "**Advisor explanation**"
            )

            st.write(
                details["explanation"]
            )


    else:

        st.success(
            "There are currently no blocked courses."
        )


    st.divider()


    # ========================================================
    # AI SEARCH STATISTICS
    # ========================================================

    st.subheader(
        "🧠 AI Search Statistics"
    )


    search1, search2, search3 = (
        st.columns(3)
    )


    search1.metric(
        "Initial Heuristic",
        result["initial_h"]
    )


    search2.metric(
        "Expanded States",
        result["expanded_states"]
    )


    search3.metric(
        "Plan Validation",
        (
            "Passed"
            if result["valid"]
            else "Failed"
        )
    )


    st.caption(
        "A* searches curriculum states where each "
        "state represents the set of courses already "
        "completed. The heuristic estimates a lower "
        "bound on the number of semesters required "
        "from the remaining structured credits."
    )


    if result["valid"]:

        st.success(
            "The generated plan satisfies the encoded "
            "prerequisites, special course rules, "
            "semester availability and the selected "
            "semester credit limit."
        )

    else:

        st.error(
            "The generated plan failed validation."
        )

        for error in result[
            "validation_errors"
        ]:

            st.write(
                f"• {error}"
            )