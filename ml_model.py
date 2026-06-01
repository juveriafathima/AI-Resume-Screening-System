def predict_role(skills):

    developer_skills = [
        "python",
        "java",
        "sql",
        "flask",
        "html",
        "css",
        "javascript"
    ]

    ai_skills = [
        "python",
        "machine learning",
        "aws"
    ]

    developer_score = 0
    ai_score = 0

    for skill in skills:

        if skill in developer_skills:
            developer_score += 1

        if skill in ai_skills:
            ai_score += 1

    if developer_score > ai_score:
        role = "Software Developer"

    elif ai_score > developer_score:
        role = "AI / ML Engineer"

    else:
        role = "General IT Role"

    return role


def calculate_resume_score(skills):

    important_skills = [
        "python",
        "java",
        "sql",
        "aws",
        "flask",
        "html",
        "css",
        "javascript",
        "communication"
    ]

    score = (
        len(skills)
        / len(important_skills)
    ) * 100

    return round(score)


def missing_skills(skills):

    required_skills = [
        "python",
        "sql",
        "aws",
        "git",
        "communication"
    ]

    missing = []

    for skill in required_skills:

        if skill not in skills:
            missing.append(skill)

    return missing