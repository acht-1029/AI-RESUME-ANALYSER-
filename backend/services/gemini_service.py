import os
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-1.5-flash")


class GeminiService:

    @staticmethod
    def analyze_resume(
        resume_text: str,
        job_description: str
    ):

        prompt = f"""
You are an expert ATS Resume Analyzer.

Compare the following resume with the given job description.

Resume:

{resume_text}

Job Description:

{job_description}

Return your response in this format:

ATS Score:
Matched Skills:
Missing Skills:
Strengths:
Weaknesses:
Resume Improvement Suggestions:
Interview Questions:
"""

        response = model.generate_content(prompt)

        return response.text
