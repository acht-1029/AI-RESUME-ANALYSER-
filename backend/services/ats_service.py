from core.analyzer import ResumeAnalyzer


class ATSService:

    analyzer = ResumeAnalyzer()

    @classmethod
    def analyze_resume(
        cls,
        file_path: str,
        job_description: str
    ):

        result = cls.analyzer.full_analysis(
            resume_pdf_path=file_path,
            jd_text=job_description
        )

        if not result["success"]:

            raise Exception(
                result["error"]
            )

        return {

            "ats_score": result["scores"]["overall_ats_score"],

            "matched_skills": result["skills_analysis"]["matching_skills"],

            "missing_skills": result["skills_analysis"]["missing_skills"],

            "suggestions":
                result["genai_coach"]["resume_improvement_suggestions"],

            "interview_questions":
                result["genai_coach"]["mock_interview_questions"],

            "raw_result": result

        }
