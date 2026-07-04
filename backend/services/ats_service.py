from services.resume_parser import extract_resume_text


class ATSService:
    """
    Service layer for connecting the web application
    with the ATS/NLP engine.
    """

    @staticmethod
    def analyze_resume(file_path: str, job_description: str):

        # Extract resume text
        resume_text = extract_resume_text(file_path)

        # ======================================================
        # TODO:
        # Replace these placeholders with Keshav's functions
        # ======================================================

        ats_score = 0

        matched_skills = []

        missing_skills = []

        suggestions = []

        interview_questions = []

        result = {
            "resume_text": resume_text,
            "ats_score": ats_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "suggestions": suggestions,
            "interview_questions": interview_questions
        }

        return result
