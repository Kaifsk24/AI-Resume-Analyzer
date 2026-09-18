import streamlit as st
from resume_parser import extract_text_from_pdf
from analyzer import find_skills, calculate_score, match_job_description

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #f7f9fc;
    }

    /* Main title */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 18px;
        margin-bottom: 35px;
    }

    /* Cards */
    .card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #e5e7eb;
        margin-bottom: 20px;
    }

    /* Metric cards */
    .metric-card {
        background: white;
        padding: 22px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #e5e7eb;
    }

    .metric-number {
        font-size: 32px;
        font-weight: 800;
    }

    .metric-label {
        color: #6b7280;
        font-size: 15px;
    }

    /* Skill badge */
    .skill {
        display: inline-block;
        padding: 7px 13px;
        margin: 5px;
        background: #eef2ff;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 600;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:

    st.markdown("## 📄 AI Resume Analyzer")

    st.markdown("---")

    st.markdown("### 🚀 Features")

    st.markdown("""
    📑 Resume PDF Analysis  

    🧠 Skill Detection  

    📊 Resume Scoring  

    🎯 Job Matching  

    ❌ Missing Skills  

    💡 Improvement Suggestions
    """)

    st.markdown("---")

    st.markdown("### 🛠️ Technologies")

    st.markdown("""
    🐍 Python  
    🤖 AI / NLP  
    🎈 Streamlit  
    📄 PDF Parser
    """)

    st.markdown("---")

    st.caption("AI Resume Analyzer • 2026")


# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    '<div class="main-title">🤖 AI Resume Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Analyze your resume and discover how well it matches your dream job.</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# UPLOAD SECTION
# --------------------------------------------------
st.markdown("## 📤 Upload Your Resume")

st.write("Upload your resume in PDF format.")

uploaded_file = st.file_uploader(
    "Choose your resume",
    type=["pdf"],
    label_visibility="collapsed"
)


# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------
if uploaded_file is not None:

    st.success("✅ Resume uploaded successfully!")

    # Extract text
    resume_text = extract_text_from_pdf(uploaded_file)

    if resume_text.strip():

        # --------------------------------------------------
        # EXTRACTED TEXT
        # --------------------------------------------------
        with st.expander("📑 View Extracted Resume Text"):

            st.text_area(
                "Resume Content",
                resume_text,
                height=250
            )

        # --------------------------------------------------
        # ANALYZE
        # --------------------------------------------------
        skills = find_skills(resume_text)

        score = calculate_score(
            resume_text,
            skills
        )

        # --------------------------------------------------
        # RESUME ANALYSIS
        # --------------------------------------------------
        st.markdown("## 📊 Resume Analysis")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Resume Score",
                f"{score}/100"
            )

        with col2:
            st.metric(
                "Skills Detected",
                len(skills)
            )

        with col3:
            st.metric(
                "Resume Length",
                f"{len(resume_text.split())} words"
            )

        # --------------------------------------------------
        # SCORE PROGRESS
        # --------------------------------------------------
        st.progress(
            min(score, 100) / 100
        )

        # --------------------------------------------------
        # SKILLS
        # --------------------------------------------------
        st.markdown("## 🛠️ Skills Found")

        if skills:

            skills_html = ""

            for skill in skills:
                skills_html += f"""
                <span class="skill">{skill.title()}</span>
                """

            st.markdown(
                skills_html,
                unsafe_allow_html=True
            )

        else:

            st.warning(
                "No common technical skills detected."
            )

        # --------------------------------------------------
        # JOB DESCRIPTION
        # --------------------------------------------------
        st.markdown("## 🎯 Job Description Matcher")

        job_description = st.text_area(
            "Paste the Job Description here:",
            height=220,
            placeholder="""Example:

We are looking for a Python Developer
with experience in Python, SQL, Git,
Machine Learning and FastAPI.
"""
        )

        # --------------------------------------------------
        # JOB MATCH
        # --------------------------------------------------
        if job_description.strip():

            (
                match_score,
                matching_skills,
                missing_skills
            ) = match_job_description(
                resume_text,
                job_description
            )

            st.markdown("## 📈 Job Match Result")

            # Match score
            st.metric(
                "Job Match Score",
                f"{match_score}%"
            )

            st.progress(
                min(match_score, 100) / 100
            )

            # --------------------------------------------------
            # MATCHING SKILLS
            # --------------------------------------------------
            st.markdown("### ✅ Matching Skills")

            if matching_skills:

                matching_html = ""

                for skill in matching_skills:
                    matching_html += f"""
                    <span class="skill">{skill.title()}</span>
                    """

                st.markdown(
                    matching_html,
                    unsafe_allow_html=True
                )

            else:

                st.info(
                    "No matching skills found."
                )

            # --------------------------------------------------
            # MISSING SKILLS
            # --------------------------------------------------
            st.markdown("### ❌ Missing Skills")

            if missing_skills:

                missing_html = ""

                for skill in missing_skills:
                    missing_html += f"""
                    <span class="skill">{skill.title()}</span>
                    """

                st.markdown(
                    missing_html,
                    unsafe_allow_html=True
                )

            else:

                st.success(
                    "🎉 No major missing skills detected!"
                )

            # --------------------------------------------------
            # IMPROVEMENT SUGGESTIONS
            # --------------------------------------------------
            st.markdown("## 💡 Resume Improvement Suggestions")

            if missing_skills:

                st.write(
                    "Based on the job description, "
                    "consider improving your resume in these areas:"
                )

                for skill in missing_skills:

                    st.warning(
                        f"📌 Consider adding or highlighting: **{skill.title()}**"
                    )

                st.info(
                    "👍 Your resume has a good match. "
                    "Highlight your relevant skills and projects more clearly."
                )

            else:

                st.success(
                    "🎉 Your resume matches the job description very well!"
                )

        else:

            st.info(
                "👆 Paste a job description above to check your job match."
            )

    else:

        st.error(
            "❌ Could not extract text from this PDF."
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("---")

st.markdown(
    "<center>Built with ❤️ using Python, AI & Streamlit</center>",
    unsafe_allow_html=True
)