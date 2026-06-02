from flask import Flask, render_template, request
import os

from resume_analyzer import (
    extract_resume_text,
    get_resume_suggestions
)

from nlp_processor import (
    extract_skills
)

from ml_model import (
    predict_role,
    calculate_resume_score,
    missing_skills
)

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = "uploads"

# Create uploads folder automatically
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze_resume():

    # Check if file uploaded
    if "resume" not in request.files:
        return "No file uploaded"

    file = request.files["resume"]

    # Check empty file
    if file.filename == "":
        return "Please upload a resume"

    # Save uploaded file
    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    # Extract resume text
    resume_text = extract_resume_text(
        filepath
    )

    # Extract skills
    skills = extract_skills(
        resume_text
    )

    # Predict role
    predicted_role = predict_role(
        skills
    )

    # Resume score
    resume_score = calculate_resume_score(
        skills
    )

    # Missing skills
    missing = missing_skills(
        skills
    )

    # AI Suggestions (safe for Render free plan)
    try:
        ai_suggestions = get_resume_suggestions(
            resume_text[:2000]
        )

    except:
        ai_suggestions = """
- Add more technical skills
- Improve project descriptions
- Make resume ATS friendly
"""

    # Result page
    return f"""
    <html>
    <head>
        <title>Resume Analysis</title>
    </head>

    <body style="font-family: Arial; padding: 30px;">

        <h2>Resume Analysis Complete</h2>

        <h3>Resume Score:</h3>
        <p>{resume_score}/100</p>

        <h3>Detected Skills:</h3>
        <ul>
            {''.join([f'<li>{skill}</li>' for skill in skills])}
        </ul>

        <h3>Missing Skills:</h3>
        <ul>
            {''.join([f'<li>{skill}</li>' for skill in missing])}
        </ul>

        <h3>Recommended Role:</h3>
        <p>{predicted_role}</p>

        <h3>AI Suggestions:</h3>
        <pre>{ai_suggestions}</pre>

        <br>
        <a href="/">Analyze Another Resume</a>

    </body>
    </html>
    """


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)