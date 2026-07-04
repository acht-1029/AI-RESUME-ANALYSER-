import re

COMMON_SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "javascript",
    "typescript",
    "react",
    "nextjs",
    "nodejs",
    "express",
    "fastapi",
    "flask",
    "django",
    "html",
    "css",
    "bootstrap",
    "tailwind",
    "mysql",
    "postgresql",
    "mongodb",
    "sqlite",
    "firebase",
    "docker",
    "kubernetes",
    "git",
    "github",
    "linux",
    "aws",
    "azure",
    "gcp",
    "tensorflow",
    "pytorch",
    "machine learning",
    "deep learning",
    "nlp",
    "langchain",
    "opencv",
    "pandas",
    "numpy",
    "scikit-learn",
    "rest api",
    "graphql"
]


def clean_text(text: str):

    text = text.lower()

    text = re.sub(r'[^a-z0-9+# ]', ' ', text)

    return text


def extract_skills(text: str):

    text = clean_text(text)

    skills = []

    for skill in COMMON_SKILLS:

        if skill in text:

            skills.append(skill)

    return sorted(list(set(skills)))


def compare_skills(resume_text, job_description):

    resume_skills = extract_skills(resume_text)

    jd_skills = extract_skills(job_description)

    matched = []

    missing = []

    for skill in jd_skills:

        if skill in resume_skills:

            matched.append(skill)

        else:

            missing.append(skill)

    if len(jd_skills) == 0:

        score = 0

    else:

        score = round(

            (len(matched) / len(jd_skills)) * 100,

            2

        )

    return {

        "ats_score": score,

        "resume_skills": resume_skills,

        "matched_skills": matched,

        "missing_skills": missing

    }
