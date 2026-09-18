import re


SKILLS = [
    "python",
    "java",
    "c++",
    "javascript",
    "html",
    "css",
    "react",
    "node.js",
    "sql",
    "mysql",
    "mongodb",
    "git",
    "github",
    "docker",
    "aws",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "generative ai",
    "data science",
    "fastapi",
    "flask",
]


def find_skills(resume_text):
    text = resume_text.lower()
    found_skills = []

    for skill in SKILLS:
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            found_skills.append(skill.title())

    return found_skills


def calculate_score(resume_text, skills):
    score = 0

    if len(resume_text) > 500:
        score += 20

    if "education" in resume_text.lower():
        score += 20

    if "experience" in resume_text.lower():
        score += 20

    if "project" in resume_text.lower():
        score += 20

    if len(skills) >= 3:
        score += 20

    return score


def match_job_description(resume_text, job_description):
    resume_skills = set(find_skills(resume_text))
    job_skills = set(find_skills(job_description))

    if not job_skills:
        return 0, [], []

    matching_skills = sorted(resume_skills.intersection(job_skills))
    missing_skills = sorted(job_skills - resume_skills)

    match_score = int(
        (len(matching_skills) / len(job_skills)) * 100
    )

    return match_score, matching_skills, missing_skills