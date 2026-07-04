from services.resume_parser import extract_resume_text
from services.skill_extractor import compare_skills


class ATSService:

    @staticmethod
    def analyze_resume(file_path , job_description):

        resume_text = extract_resume_text(file_path)

        result = compare_skills(

            resume_text,

            job_description

        )

        result["suggestions"] = [

            f"Learn {skill}"

            for skill in result["missing_skills"]

        ]

        result["interview_questions"] = [

            f"Explain your experience with {skill}"

            for skill in result["matched_skills"]

        ]

        return result
