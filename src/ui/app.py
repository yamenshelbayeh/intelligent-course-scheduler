import pandas as pd
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"
DAY_NAMES = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
    7: "Sunday",
}
COURSES = [
    "CSE101",
    "CSE102",
    "CSE201",
    "CSE202",
    "CSE301",
    "CSE302",
    "CSE303",
    "MATH101",
    "MATH201",
    "STAT201",
]

st.set_page_config(
    page_title="Intelligent Course Scheduler",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>

    /* =========================
       PAGE
       ========================= */

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    /* Reduce default Streamlit top space */
    [data-testid="stMainBlockContainer"] {
        padding-top: 2rem;
    }


    /* =========================
       TYPOGRAPHY
       ========================= */

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


    /* =========================
       INPUTS
       ========================= */

    [data-testid="stMultiSelect"],
    [data-testid="stNumberInput"],
    [data-testid="stSlider"] {
        margin-bottom: 0.4rem;
    }

    label {
        font-weight: 600 !important;
    }


    /* =========================
       GENERATE BUTTON
       ========================= */

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


    /* =========================
       METRIC CARDS
       ========================= */

    [data-testid="stMetric"] {
        background: var(--secondary-background-color);
        border: 1px solid rgba(150, 150, 150, 0.18);
        border-radius: 16px;
        padding: 1.2rem 1.25rem;
        min-height: 120px;
        transition:
            transform 0.15s ease,
            box-shadow 0.15s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        font-weight: 600;
        opacity: 0.75;
    }

    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 800;
    }


    /* =========================
       BORDERED CARDS
       ========================= */

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--secondary-background-color);
        border-radius: 16px !important;
        border-color: rgba(150, 150, 150, 0.18) !important;
        transition:
            transform 0.15s ease,
            box-shadow 0.15s ease;
    }

    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
    }


    /* =========================
       EXPANDERS
       ========================= */

    [data-testid="stExpander"] {
        background: var(--secondary-background-color);
        border: 1px solid rgba(150, 150, 150, 0.18);
        border-radius: 14px;
        margin-bottom: 0.8rem;
        overflow: hidden;
    }

    [data-testid="stExpander"] summary {
        font-weight: 650;
        padding-top: 0.15rem;
        padding-bottom: 0.15rem;
    }

    [data-testid="stExpander"] summary:hover {
        opacity: 0.85;
    }


    /* =========================
       TABLES
       ========================= */

    [data-testid="stDataFrame"] {
        margin-top: 0.8rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(150, 150, 150, 0.15);
        border-radius: 12px;
        overflow: hidden;
    }


    /* =========================
       STATUS MESSAGES
       ========================= */

    [data-testid="stAlert"] {
        border-radius: 12px;
    }


    /* =========================
       DIVIDERS
       ========================= */

    hr {
        margin-top: 2.2rem !important;
        margin-bottom: 2.2rem !important;
        opacity: 0.15;
    }


    /* =========================
       CAPTIONS
       ========================= */

    [data-testid="stCaptionContainer"] {
        opacity: 0.72;
    }


    /* =========================
       MOBILE
       ========================= */

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

st.markdown(
    """
    <h1>🎓 Intelligent Course Scheduler</h1>

    <p style="
        font-size: 1.15rem;
        opacity: 0.68;
        max-width: 760px;
        margin-top: 0;
        margin-bottom: 2.2rem;
    ">
        AI-powered degree planning, academic advising,
        and conflict-free timetable generation using
        graph search, constraint satisfaction, and PostgreSQL.
    </p>
    """,
    unsafe_allow_html=True
)

completed = st.multiselect(
    "Completed courses",
    COURSES
)

input_col1, input_col2 = st.columns(2)

with input_col1:
    max_credits = st.slider(
        "Maximum credits per semester",
        min_value=5,
        max_value=30,
        value=15,
        step=5
    )

with input_col2:
    max_difficulty = st.number_input(
        "Maximum semester difficulty",
        min_value=1,
        value=10,
        step=1
    )

if st.button(
        "Generate Plan",
        type="primary",
        use_container_width=True
):
    payload = {
        "completed": completed,
        "max_credits": max_credits,
        "max_difficulty": max_difficulty,
    }

    try:
        response = requests.post(
            f"{API_URL}/full-plan",
            json=payload,
            timeout=30
        )

        if response.status_code == 200:

            data = response.json()

            advisor = data["advisor"]
            degree_plan = data["degree_plan"]
            degree_timetables = data["degree_timetables"]
            degree_plan_details = data["degree_plan_details"]

            st.success("Plan generated successfully!")

            completed_col, semesters_col, states_col, recommendation_col = st.columns(4)

            completed_col.metric(
                "Completed Courses",
                len(advisor["completed"])
            )

            semesters_col.metric(
                "Remaining Semesters",
                len(degree_plan)
            )

            states_col.metric(
                "A* Expanded States",
                data["expanded_states"]
            )

            top_recommendation = (
                advisor["recommendations"][0]["course"]
                if advisor["recommendations"]
                else "None"
            )

            recommendation_col.metric(
                "Top Recommendation",
                top_recommendation
            )

            st.divider()

            st.subheader("Recommended Courses")

            if advisor["recommendations"]:
                for rank, recommendation in enumerate(
                        advisor["recommendations"],
                        start=1
                ):
                    with st.container(border=True):

                        title_col, difficulty_col = st.columns([4, 1])

                        with title_col:
                            if rank == 1:
                                st.markdown(
                                    f"### ⭐ {rank}. {recommendation['course']}"
                                )
                                st.caption("Top recommendation")
                            else:
                                st.markdown(
                                    f"### {rank}. {recommendation['course']}"
                                )

                            st.caption(
                                f"{recommendation['credits']} credits"
                            )

                        with difficulty_col:
                            st.metric(
                                "Difficulty",
                                f"{recommendation['difficulty']}/5"
                            )

                        direct_unlocks = (
                            ", ".join(recommendation["unlocks"])
                            if recommendation["unlocks"]
                            else "None"
                        )

                        future_unlocks = (
                            ", ".join(recommendation["future_unlocks"])
                            if recommendation["future_unlocks"]
                            else "None"
                        )

                        unlock_col1, unlock_col2 = st.columns(2)

                        with unlock_col1:
                            st.markdown("**Direct Unlocks**")
                            st.write(direct_unlocks)

                        with unlock_col2:
                            st.markdown("**Future Impact**")
                            st.write(future_unlocks)

                        with st.expander("Why is this recommended?"):
                            st.write(
                                recommendation["explanation"]
                            )

            else:
                st.info("No remaining course recommendations.")

            st.divider()

            st.subheader("Blocked Courses")

            if advisor["blocked"]:
                for course in sorted(advisor["blocked"]):
                    details = advisor["blocked"][course]

                    missing_prereqs = sorted(
                        details["missing_prerequisites"]
                    )

                    prerequisite_chain = sorted(
                        details["prerequisite_chain"]
                    )

                    blocked_label = (
                        f"🔒 {course} — "
                        f"{len(missing_prereqs)} prerequisite(s) missing"
                    )

                    with st.expander(blocked_label):
                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown("**Missing Direct Prerequisites**")

                            if missing_prereqs:
                                for prerequisite in missing_prereqs:
                                    st.write(f"• {prerequisite}")
                            else:
                                st.write("None")

                        with col2:
                            st.markdown("**Remaining Prerequisite Chain**")

                            if prerequisite_chain:
                                for prerequisite in prerequisite_chain:
                                    st.write(f"• {prerequisite}")
                            else:
                                st.write("None")

                        st.divider()

                        st.markdown("**Advisor Explanation**")
                        st.write(details["explanation"])

            else:
                st.success("No blocked courses.")

            st.divider()

            st.subheader("Degree Plan")
            if degree_plan_details:
                for semester in degree_plan_details:
                    with st.container(border=True):
                        st.markdown(
                            f"### Semester {semester['semester']}"
                        )

                        st.write(
                            " • ".join(semester["courses"])
                        )

                        credits_col, difficulty_col = st.columns(2)

                        credits_col.metric(
                            "Credits",
                            semester["total_credits"]
                        )

                        difficulty_col.metric(
                            "Difficulty Load",
                            f"{semester['total_difficulty']} / {max_difficulty}"
                        )
            else:
                st.success("Degree requirements completed.")

            st.divider()

            st.subheader("Semester Timetables")
            if degree_timetables:
                for semester in degree_timetables:
                    semester_number = semester["semester"]
                    timetable = semester["timetable"]
                    stats = semester["stats"]

                    semester_courses = ", ".join(
                        semester["courses"]
                    )

                    with st.expander(
                            f"📅 Semester {semester_number} — {semester_courses}"
                    ):
                        rows = []

                        for course, section in timetable.items():
                            for meeting in section["meetings"]:
                                rows.append({
                                    "Course": course,
                                    "Section": section["section_code"],
                                    "Day": DAY_NAMES[meeting["day_of_week"]],
                                    "Start": meeting["start_time"],
                                    "End": meeting["end_time"],
                                })

                        df = pd.DataFrame(rows)

                        st.dataframe(
                            df,
                            use_container_width=True,
                            hide_index=True
                        )

                        stat_col1, stat_col2 = st.columns(2)

                        stat_col1.metric(
                            "CSP Calls",
                            stats["calls"]
                        )

                        stat_col2.metric(
                            "Backtracks",
                            stats["backtracks"]
                        )

            else:
                st.info("No remaining semester timetables.")

            st.divider()

            st.subheader("Search Statistics")
            search_col1, search_col2 = st.columns(2)

            search_col1.metric(
                "A* Expanded States",
                data["expanded_states"]
            )

            search_col2.metric(
                "Planned Semesters",
                len(degree_plan)
            )





        else:
            try:
                error = response.json()
                message = error.get(
                    "detail",
                    "Something went wrong while generating the plan."
                )
            except ValueError:
                message = "The server returned an unexpected response."

            st.error(message)

    except requests.RequestException as error:
        st.error(
            "Could not connect to the FastAPI server."
        )
