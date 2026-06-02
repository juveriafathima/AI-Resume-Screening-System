import re

# Bigger skills database
skills_database = [
    "python", "java", "c", "c++", "sql",
    "mysql", "html", "css", "javascript",
    "react", "flask", "aws", "cloud",
    "machine learning", "artificial intelligence",
    "ai", "nlp", "git", "github",
    "docker", "data structures",
    "algorithms", "problem solving",
    "communication", "teamwork",
    "leadership", "excel",
    "power bi", "tableau"
]


def extract_skills(text):

    detected_skills = []

    text = text.lower()

    for skill in skills_database:

        if re.search(r'\b' + re.escape(skill) + r'\b', text):

            detected_skills.append(skill)

    return list(set(detected_skills))