def predict_role(skills):

    skills = [skill.lower() for skill in skills]

    if "python" in skills and "machine learning" in skills:
        return "AI / ML Engineer"

    elif "html" in skills and "css" in skills and "javascript" in skills:
        return "Frontend Developer"

    elif "python" in skills and "flask" in skills:
        return "Backend Developer"

    elif "sql" in skills and "aws" in skills:
        return "Cloud / Database Engineer"

    elif "java" in skills:
        return "Software Developer"

    else:
        return "General IT Role"


def calculate_resume_score(skills):

    score = len(skills) * 10

    if score > 100:
        score = 100

    return score


def missing_skills(skills):

    important_skills = [
        "python",
        "sql",
        "aws",
        "git",
        "communication"
    ]

    missing = []

    for skill in important_skills:

        if skill not in skills:
            missing.append(skill)

    return missing