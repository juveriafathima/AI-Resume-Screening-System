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

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze_resume():

    if "resume" not in request.files:
        return "No file uploaded"

    file = request.files["resume"]

    if file.filename == "":
        return "Please upload a resume"

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    resume_text = extract_resume_text(
        filepath
    )

    skills = extract_skills(
        resume_text
    )

    predicted_role = predict_role(
        skills
    )

    resume_score = calculate_resume_score(
        skills
    )

    missing = missing_skills(
        skills
    )

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

    return f"""
    <html>

    <head>
        <title>Resume Analysis</title>

        <style>
            body {{
                font-family: Arial;
                background: #f4f4f4;
                padding: 30px;
            }}

            .container {{
                background: white;
                padding: 30px;
                border-radius: 12px;
                max-width: 800px;
                margin: auto;
                box-shadow: 0 0 15px rgba(0,0,0,0.1);
            }}

            .score {{
                font-size: 28px;
                color: green;
                font-weight: bold;
            }}

            .skill {{
                display: inline-block;
                background: #007bff;
                color: white;
                padding: 8px 15px;
                border-radius: 20px;
                margin: 5px;
            }}

            .missing {{
                background: red;
            }}

            h2 {{
                color: #333;
            }}
        </style>
    </head>

    <body>

    <div class="container">

        <h2>Resume Analysis Complete 🚀</h2>

        <h3>ATS Resume Score</h3>
        <p class="score">{resume_score}/100</p>

        <h3>Detected Skills</h3>

        {
            ''.join([
                f'<span class="skill">{skill}</span>'
                for skill in skills
            ])
        }

        <h3>Missing Skills</h3>

        {
            ''.join([
                f'<span class="skill missing">{skill}</span>'
                for skill in missing
            ])
        }

        <h3>Recommended Role</h3>
        <p><b>{predicted_role}</b></p>

        <h3>AI Suggestions</h3>
        <pre>{ai_suggestions}</pre>

        <br><br>

        <a href="/">Analyze Another Resume</a>

    </div>

    </body>
    </html>
    """


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)