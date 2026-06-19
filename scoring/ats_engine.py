import logging
from typing import Dict

logger = logging.getLogger(__name__)

def calculate_ats_score(
    skills_match_percentage: float, 
    text_similarity_score: float,
) -> Dict:
    """
    Calculate the overall ATS score based on multiple factors.
    
    Weights (adjustable based on testing):
    - 60% based on direct extracted skills matching (the most critical factor)
    - 40% based on full-text TF-IDF similarity (catches contextual similarities)
    """
    try:
        # Ensure values are floats
        skills_score = float(skills_match_percentage)
        sim_score = float(text_similarity_score)
        
        # Apply weights
        weighted_skills = skills_score * 0.60
        weighted_sim = sim_score * 0.40
        
        total_score = round(weighted_skills + weighted_sim, 2)
        
        return {
            "overall_score": total_score,
            "skills_score_component": round(weighted_skills, 2),
            "similarity_score_component": round(weighted_sim, 2),
            "skills_match_percentage": round(skills_score, 2),
            "text_similarity_percentage": round(sim_score, 2)
        }
    except Exception as e:
        logger.error(f"ATS scoring failed: {e}")
        return {
            "overall_score": 0.0,
            "error": str(e)
        }
