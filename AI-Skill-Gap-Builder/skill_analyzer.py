import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CAREER_DATA_PATH = BASE_DIR / "data" / "career_skills.json"

skills_database = [
    "Python",
    "Machine Learning",
    "Deep Learning",
    "TensorFlow",
    "SQL",
    "Docker",
    "AWS",
    "Statistics",
    "Pandas",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Git",
    "Networking",
    "Linux",
    "Wireshark",
    "Nmap",
    "SIEM",
    "Incident Response"
]

def extract_skills(text):

    found_skills = []

    for skill in skills_database:

        if skill.lower() in text.lower():

            found_skills.append(skill)
    print("Found skills:", found_skills)
    return found_skills


def analyze_resume(goal, resume_skills):

    with CAREER_DATA_PATH.open("r", encoding="utf-8") as f:

        career_data = json.load(f)

    required_skills = career_data[goal]

    matched = []

    missing = []

    for skill in required_skills:

        if skill in resume_skills:

            matched.append(skill)

        else:

            missing.append(skill)

    score = round(
        (len(matched) / len(required_skills)) * 100,
        2
    )

    return score, matched, missing
