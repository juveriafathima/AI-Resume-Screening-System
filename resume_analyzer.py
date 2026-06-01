import PyPDF2
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="YOUR_API_KEY"
)


def extract_resume_text(file_path):

    text = ""

    with open(file_path, "rb") as file:

        pdf_reader = PyPDF2.PdfReader(file)

        for page in pdf_reader.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted

    return text


def get_resume_suggestions(text):

    try:

        completion = client.chat.completions.create(
            model="meta-llama/llama-3.2-3b-instruct:free",
            messages=[
                {
                    "role": "system",
                    "content":
                    """
You are a simple AI resume assistant.

Give only 3 short resume suggestions.

Rules:
- Use simple English
- No tables
- No rewriting
- No fake percentages
- Keep it short

Example:
- Add more technical projects
- Improve skills section
- Add certifications
"""
                },
                {
                    "role": "user",
                    "content":
                    f"Give simple resume improvement suggestions for this resume:\n{text}"
                }
            ],
            max_tokens=80
        )

        return completion.choices[0].message.content

    except Exception as e:

        print("AI Error:", e)

        return """
- Improve technical skills section
- Add more projects
- Make resume ATS friendly
"""