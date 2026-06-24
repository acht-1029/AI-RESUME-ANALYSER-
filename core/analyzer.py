import logging
from typing import Dict, Any

from extractors.pdf_parser import extract_text_safe
from extractors.section_splitter import split_sections
from extractors.skill_extractor import extract_skills
from scoring.similarity import calculate_similarity
from analysis.gap_analyzer import analyze_gaps
from scoring.ats_engine import calculate_ats_score

from genai.suggestions import generate_resume_suggestions
from genai.interview_generator import generate_interview_questions

logger = logging.getLogger(__name__)

class ResumeAnalyzer:
    """
    Main orchestrator for the ATS Resume Analyzer NLP + GenAI pipeline.
    """
    def __init__(self):
        pass

    def nlp_analysis(self, resume_pdf_path: str, jd_text: str) -> Dict[str, Any]:
        """
        Run only the deterministic NLP pipeline (No API keys needed).
        """
        logger.info(f"Starting NLP analysis for {resume_pdf_path}")
        
        pdf_result = extract_text_safe(resume_pdf_path)
        if not pdf_result["success"]:
            logger.error(f"Analysis aborted. PDF Error: {pdf_result['error']}")
            return {
                "success": False, 
                "error": f"Failed to extract text from PDF: {pdf_result['error']}"
            }
            
        resume_text = pdf_result["text"]
        sections = split_sections(resume_text)
        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(jd_text)
        gap_analysis = analyze_gaps(resume_skills, jd_skills)
        similarity_score = calculate_similarity(resume_text, jd_text)
        ats_result = calculate_ats_score(
            skills_match_percentage=gap_analysis["match_percentage"],
            text_similarity_score=similarity_score
        )
        
        # We also want to pass resume_skills list up for GenAI
        resume_skill_names = [s["skill"] for s in resume_skills]
        
        return {
            "success": True,
            "metadata": {
                "pages_parsed": pdf_result.get("page_count", 0),
                "sections_found": list(sections.keys())
            },
            "skills_analysis": {
                "resume_total_skills": len(resume_skills),
                "jd_total_skills": len(jd_skills),
                "matching_skills": gap_analysis["matching_skills"],
                "missing_skills": gap_analysis["missing_skills"],
                "resume_skill_names": resume_skill_names # Internal field for GenAI layer
            },
            "scores": ats_result
        }

    def full_analysis(self, resume_pdf_path: str, jd_text: str) -> Dict[str, Any]:
        """
        Run the complete pipeline: NLP scoring + GenAI suggestions & interview questions.
        If GenAI fails or limits are hit, it gracefully falls back to returning just NLP results.
        """
        logger.info(f"Starting FULL analysis for {resume_pdf_path}")
        
        # 1. Run the base NLP pipeline
        nlp_result = self.nlp_analysis(resume_pdf_path, jd_text)
        
        if not nlp_result["success"]:
            return nlp_result
            
        # Extract data needed for GenAI
        missing_skills = nlp_result["skills_analysis"]["missing_skills"]
        resume_skill_names = nlp_result["skills_analysis"].pop("resume_skill_names", [])
        
        # 2. Run GenAI layer with safe try/except fallbacks
        try:
            suggestions = generate_resume_suggestions(missing_skills, jd_text)
        except Exception as e:
            logger.error(f"GenAI Suggestions failed: {e}")
            suggestions = ["GenAI service unavailable. Try adding the missing skills listed above."]
            
        try:
            questions = generate_interview_questions(resume_skill_names, jd_text)
        except Exception as e:
            logger.error(f"GenAI Interview failed: {e}")
            questions = ["GenAI service unavailable. Prepare to discuss your core skills in depth."]
            
        # 3. Combine results into a single payload for the backend
        nlp_result["genai_coach"] = {
            "resume_improvement_suggestions": suggestions,
            "mock_interview_questions": questions
        }
        
        return nlp_result
