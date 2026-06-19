import logging
from typing import Dict, Any

from extractors.pdf_parser import extract_text_safe
from extractors.section_splitter import split_sections
from extractors.skill_extractor import extract_skills
from scoring.similarity import calculate_similarity
from analysis.gap_analyzer import analyze_gaps
from scoring.ats_engine import calculate_ats_score

logger = logging.getLogger(__name__)

class ResumeAnalyzer:
    """
    Main orchestrator for the ATS Resume Analyzer NLP pipeline.
    This class ties together PDF extraction, section splitting, skill matching,
    and scoring to provide a unified analysis of a resume against a Job Description.
    """
    def __init__(self):
        pass

    def analyze(self, resume_pdf_path: str, jd_text: str) -> Dict[str, Any]:
        """
        Run the full NLP pipeline on a resume PDF and a Job Description text.
        
        Args:
            resume_pdf_path: Path to the candidate's PDF resume.
            jd_text: The full text of the Job Description.
            
        Returns:
            A dictionary containing the full analysis results.
        """
        logger.info(f"Starting analysis for {resume_pdf_path}")
        
        # 1. Extract text from PDF safely
        pdf_result = extract_text_safe(resume_pdf_path)
        if not pdf_result["success"]:
            logger.error(f"Analysis aborted. PDF Error: {pdf_result['error']}")
            return {
                "success": False, 
                "error": f"Failed to extract text from PDF: {pdf_result['error']}"
            }
            
        resume_text = pdf_result["text"]
        
        # 2. Split resume into logical sections
        sections = split_sections(resume_text)
        
        # 3. Extract skills from Resume and JD
        # Since we added strict false-positive guards (stop words, length ratio) to skill_extractor in Day 1,
        # it is now perfectly safe (and better for multi-column PDFs) to scan the entire resume text.
        resume_skills = extract_skills(resume_text)
        
        # For JD, we always scan the full text because JDs rarely have standard sections
        jd_skills = extract_skills(jd_text)
        
        # 4. Analyze the skills gap
        gap_analysis = analyze_gaps(resume_skills, jd_skills)
        
        # 5. Calculate contextual text similarity (TF-IDF)
        similarity_score = calculate_similarity(resume_text, jd_text)
        
        # 6. Calculate the final weighted ATS score
        ats_result = calculate_ats_score(
            skills_match_percentage=gap_analysis["match_percentage"],
            text_similarity_score=similarity_score
        )
        
        # 7. Package everything into a clean API contract for the backend
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
                "missing_skills": gap_analysis["missing_skills"]
            },
            "scores": ats_result
        }
