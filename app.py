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

    resume_text = extract_resume_text(filepath)

    skills = extract_skills(resume_text)

    predicted_role = predict_role(skills)

    resume_score = calculate_resume_score(skills)

    missing = missing_skills(skills)

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
    <title>AI Resume Analyzer</title>

    <style>

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Arial, sans-serif;
        }}

        body {{
            background: #eef2f7;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 40px;
        }}

        .container {{
            background: white;
            width: 90%;
            max-width: 850px;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0px 8px 25px rgba(0,0,0,0.15);
            border: 1px solid #ddd;
        }}

        h1 {{
            text-align: center;
            color: #222;
            margin-bottom: 25px;
        }}

        h2 {{
            color: #333;
            margin-top: 25px;
            margin-bottom: 15px;
        }}

        .score-box {{
            background: linear-gradient(135deg, #4CAF50, #2E7D32);
            color: white;
            padding: 25px;
            text-align: center;
            border-radius: 15px;
            font-size: 35px;
            font-weight: bold;
            margin-bottom: 25px;
        }}

        .skills-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}

        .skill {{
            background: #007bff;
            color: white;
            padding: 10px 18px;
            border-radius: 25px;
            font-size: 15px;
        }}

        .missing {{
            background: #ff4d4d;
        }}

        .role-box {{
            background: #f4f6f9;
            border-left: 6px solid #007bff;
            padding: 20px;
            border-radius: 10px;
            font-size: 22px;
            font-weight: bold;
        }}

        .suggestions {{
            background: #f8f9fa;
            border: 1px solid #ddd;
            padding: 20px;
            border-radius: 12px;
            line-height: 1.8;
            white-space: pre-wrap;
        }}

        .btn {{
            display: inline-block;
            margin-top: 30px;
            background: #007bff;
            color: white;
            padding: 14px 25px;
            text-decoration: none;
            border-radius: 10px;
        }}

        .btn:hover {{
            background: #0056b3;
        }}

    </style>
</head>

<body>

<div class="container">

    <h1>🚀 AI Resume Analysis</h1>

    <h2>ATS Resume Score</h2>

    <div class="score-box">
        {resume_score}/100
    </div>

    <h2>Detected Skills</h2>

    <div class="skills-container">
        {''.join([f'<span class="skill">{skill}</span>' for skill in skills])}
    </div>

    <h2>Missing Skills</h2>

    <div class="skills-container">
        {''.join([f'<span class="skill missing">{skill}</span>' for skill in missing])}
    </div>

    <h2>Recommended Role</h2>

    <div class="role-box">
        {predicted_role}
    </div>

    <h2>AI Suggestions</h2>

    <div class="suggestions">
        {ai_suggestions}
    </div>

    <center>
        <a href="/" class="btn">
            Analyze Another Resume
        </a>
    </center>

</div>

</body>
</html>
"""


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)