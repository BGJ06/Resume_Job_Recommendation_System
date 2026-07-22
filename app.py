import streamlit as st
import pandas as pd

from recommender import JobRecommender
from utils import (
    extract_skills,
    calculate_resume_score,
    extract_text_from_pdf,
    extract_text_from_docx,
)

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI Career Navigator",
    page_icon="💼",
    layout="wide"
)

# ---------------- LOAD MODEL ---------------- #

@st.cache_resource
def load_recommender():
    model = JobRecommender()
    model.load_data()
    return model

recommender = load_recommender()

# ---------------- HEADER ---------------- #

st.title("💼 AI Career Navigator")
st.subheader("Intelligent Resume Analysis & Job Recommendation System")

st.markdown("---")

st.write("""
Paste your resume below and our AI will:

✅ Analyze your resume

✅ Calculate Resume Score

✅ Extract Skills

✅ Recommend Top Matching Jobs

✅ Help improve your resume
""")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx", "txt"]
)

resume = ""

if uploaded_file is not None:

    if uploaded_file.type == "application/pdf":
        resume = extract_text_from_pdf(uploaded_file)

    elif uploaded_file.type in [
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]:
        resume = extract_text_from_docx(uploaded_file)

    elif uploaded_file.type == "text/plain":
        resume = uploaded_file.read().decode("utf-8")

    st.success("Resume uploaded successfully!")

    with st.expander("Preview Resume"):
        st.text(resume[:3000])

analyze = st.button("🚀 Analyze Resume")

# ---------------- ANALYSIS ---------------- #

if analyze:

    if resume.strip() == "":
        st.error("Please paste your resume.")
        st.stop()

    skills = extract_skills(resume)

    score = calculate_resume_score(skills)

    st.success("Resume analyzed successfully!")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Resume Score", f"{score}/100")

    with col2:
        st.metric("Skills Found", len(skills))

    st.markdown("---")

    st.subheader("🛠 Skills Detected")

    if skills:

        cols = st.columns(4)

        for i, skill in enumerate(skills):
            cols[i % 4].success(skill)

    else:

        st.warning("No predefined skills detected.")

    st.markdown("---")

    st.subheader("💼 Recommended Jobs")

    recommendations = recommender.recommend_jobs(resume)

    if len(recommendations) == 0:

        st.warning("No matching jobs found.")

    else:

        for i, job in enumerate(recommendations):

            with st.container():

                st.markdown("### 🏆 Recommendation {}".format(i + 1))

                c1, c2 = st.columns(2)

                with c1:
                    st.write("### 💼 Job Title")
                    st.write(job["title"])

                    st.write("### 🏢 Company")
                    st.write(job["company"])

                    st.write("### 📍 Location")
                    st.write(job["location"])

                with c2:
                    st.write("### ⭐ Match")
                    st.progress(min(job["score"] / 100, 1.0))
                    st.write(f"**{job['score']}% Match**")

                    st.write("### 💰 Salary")
                    st.write(job["salary"])

                    st.write("### 👨‍💻 Experience")
                    st.write(job["experience"])

                st.write("### 🛠 Required Skills")

                if str(job["skills"]).strip() != "":
                    st.info(job["skills"])
                else:
                    st.info("Not Available")

                st.divider()

                st.markdown("---")

st.markdown(
    """
    <center>
    <h4>💙 AI Career Navigator</h4>
    <p>Built using Streamlit • Scikit-Learn • TF-IDF • Cosine Similarity</p>
    </center>
    """,
    unsafe_allow_html=True,
)