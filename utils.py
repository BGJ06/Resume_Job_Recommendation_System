import re
import pdfplumber
from docx import Document


# ----------------------------
# Clean text for NLP processing
# ----------------------------
def clean_text(text):
    if text is None:
        return ""

    text = str(text).lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove Emails
    text = re.sub(r"\S+@\S+", "", text)

    # Remove Numbers
    text = re.sub(r"\d+", " ", text)

    # Remove Special Characters
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # Remove Extra Spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# ----------------------------
# Extract text from PDF
# ----------------------------
def extract_text_from_pdf(pdf_file):
    text = ""

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


# ----------------------------
# Extract text from DOCX
# ----------------------------
def extract_text_from_docx(docx_file):
    document = Document(docx_file)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


# ----------------------------
# Extract Skills
# ----------------------------
def extract_skills(text):

    skill_list = [

        # Programming
        "python",
        "java",
        "c",
        "c++",
        "sql",
        "mysql",

        # AI / ML
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "data science",
        "tensorflow",
        "pytorch",
        "opencv",
        "nlp",

        # Data Analytics
        "pandas",
        "numpy",
        "excel",
        "power bi",
        "tableau",

        # Web
        "html",
        "css",
        "javascript",
        "react",
        "nodejs",
        "django",
        "flask",

        # Cloud
        "aws",
        "azure",
        "docker",

        # Tools
        "git",
        "github",
        "linux",

        # Soft Skills
        "communication",
        "leadership",
        "teamwork",
        "problem solving"
    ]

    text = clean_text(text)

    found_skills = []

    for skill in skill_list:
        if skill in text:
            found_skills.append(skill.title())

    return sorted(list(set(found_skills)))


# ----------------------------
# Resume Score
# ----------------------------
def calculate_resume_score(skills):

    total_skills = 20

    score = min((len(skills) / total_skills) * 100, 100)

    return round(score, 2)


# ----------------------------
# Missing Skills
# ----------------------------
def missing_skills(user_skills, required_skills):

    user = set([s.lower() for s in user_skills])

    required = set([s.lower() for s in required_skills])

    missing = required - user

    return sorted(list(missing))