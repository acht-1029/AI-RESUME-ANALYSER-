import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

def analyze_gaps(resume_skills: List[Dict], jd_skills: List[Dict]) -> Dict:
    """
    Identify missing skills between the resume and the job description.
    
    Args:
        resume_skills: List of skill dictionaries extracted from the resume.
        jd_skills: List of skill dictionaries extracted from the JD.
        
    Returns:
        Dictionary containing matched skills, missing skills, and a match percentage.
    """
    try:
        # We use the canonical "skill" name, converted to lowercase for robust matching
        resume_skill_names = {s["skill"].lower() for s in resume_skills}
        jd_skill_names = {s["skill"].lower(): s["skill"] for s in jd_skills}
        
        matching_skills = []
        missing_skills = []
        
        for jd_skill_lower, jd_skill_original in jd_skill_names.items():
            if jd_skill_lower in resume_skill_names:
                matching_skills.append(jd_skill_original)
            else:
                missing_skills.append(jd_skill_original)
                
        match_percentage = 0.0
        if len(jd_skill_names) > 0:
            match_percentage = (len(matching_skills) / len(jd_skill_names)) * 100
            
        return {
            "matching_skills": sorted(matching_skills),
            "missing_skills": sorted(missing_skills),
            "match_percentage": round(match_percentage, 2)
        }
    except Exception as e:
        logger.error(f"Gap analysis failed: {e}")
        return {
            "matching_skills": [],
            "missing_skills": [],
            "match_percentage": 0.0,
            "error": str(e)
        }
