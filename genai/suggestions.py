import logging
from typing import List
from genai.gemini_client import GeminiClient

logger = logging.getLogger(__name__)

def generate_resume_suggestions(missing_skills: List[str], job_description: str) -> List[str]:
    """
    Generate actionable resume improvement suggestions based on missing skills using Gemini.
    """
    if not missing_skills:
        return ["Your resume perfectly matches all required skills in the job description!"]
        
    client = GeminiClient()
    
    # We only pass top 5 missing skills to not overwhelm the LLM or the user
    top_missing = ", ".join(missing_skills[:5])
    
    if not client.is_configured:
        logger.info("Gemini is not configured. Falling back to NLP-only default suggestions.")
        return [
            f"Consider adding these missing skills to your resume if you have experience with them: {top_missing}",
            "Ensure your bullet points clearly describe the impact of your work."
        ]
        
    
    # Prompt Engineering: We give Gemini a persona, the context, and strict formatting rules
    prompt = f"""
    You are an expert ATS Resume Coach. A candidate is applying for a job, but their resume is missing these crucial skills: {top_missing}.
    
    Here is the job description for context:
    {job_description[:1000]}...
    
    Provide 3 very short, actionable bullet points advising the candidate on how they can improve their resume or what they should learn to pass the ATS filter.
    Keep the tone encouraging but professional. Do not use markdown formatting like asterisks or bolding, just return plain text bullet points separated by newlines. Do not start with a greeting or intro sentence.
    """
    
    try:
        response_text = client.generate_content(prompt)
        if not response_text:
            raise ValueError("Empty response from Gemini")
            
        # Clean up the output into a clean Python list of strings
        bullets = [line.strip().replace("- ", "").replace("* ", "") for line in response_text.split('\n') if line.strip()]
        return bullets
    except Exception as e:
        logger.error(f"Failed to generate suggestions: {e}")
        return [f"Consider adding these missing skills: {top_missing}"]
