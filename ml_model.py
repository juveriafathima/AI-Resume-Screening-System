def calculate_resume_score(skills):

    important_skills = [
        "python",
        "sql",
        "aws",
        "git",
        "communication"
    ]

    score = 0

    # Add score for detected skills
    score += len(skills) * 8

    # Deduct for missing important skills
    for skill in important_skills:

        if skill not in skills:
            score -= 10

    # Keep score between 0–100
    if score > 100:
        score = 100

    if score < 0:
        score = 0

    return score