def extract_skills(text):

    skills = [
        "python",
        "java",
        "sql",
        "aws",
        "machine learning",
        "flask",
        "html",
        "css",
        "javascript",
        "communication"
    ]

    found_skills = []

    text = text.lower()

    for skill in skills:

        if skill in text:
            found_skills.append(skill)

    return found_skills