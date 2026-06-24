import logging
from typing import List
from genai.gemini_client import GeminiClient

logger = logging.getLogger(__name__)

def generate_interview_questions(resume_skills: List[str], job_description: str) -> List[str]:
    """
    Generate tailored interview questions based on the JD and the candidate's actual skills.
    Returns a list of 5 questions (3 technical, 2 behavioral).
    """
    client = GeminiClient()
    
    if not client.is_configured:
        logger.info("Gemini not configured. Falling back to default interview questions.")
        return [
            "Tell me about your background and experience.",
            "Describe a challenging project you worked on.",
            "How do you handle disagreements within a team?",
            "What are your strengths and weaknesses?",
            "Why do you want this job?"
        ]
        
    skills_context = ", ".join(resume_skills[:10]) if resume_skills else "General Experience"
    
    prompt = f"""
    You are an expert Technical Interviewer. 
    You are interviewing a candidate who has these skills: {skills_context}.
    
    Here is the job description they are applying for:
    {job_description[:1000]}...
    
    Generate exactly 5 interview questions for this candidate:
    - 3 technical questions that test their stated skills in the context of the job description.
    - 2 behavioral questions related to the challenges mentioned in the job description.
    
    Rules:
    - Return ONLY the questions, separated by newlines.
    - Do not number the questions (e.g. no "1.").
    - Do not include introductory or concluding text.
    - Do not use markdown formatting like bolding or asterisks.
    """
    
    try:
        response_text = client.generate_content(prompt)
        if not response_text:
            raise ValueError("Empty response from Gemini")
            
        # Clean the output into a python list
        questions = [q.strip().replace("- ", "").replace("* ", "") for q in response_text.split('\n') if q.strip()]
        
        # Strip numbering if the LLM ignored our rules (e.g. "1. Question")
        cleaned_questions = []
        for q in questions:
            if q[0].isdigit() and q[1] in ['.', ')']:
                cleaned_questions.append(q[2:].strip())
            else:
                cleaned_questions.append(q)
                
        return cleaned_questions[:5]
    except Exception as e:
        logger.error(f"Failed to generate questions: {e}")
        return [
            "Tell me about a challenging technical project.",
            "How do you approach solving a difficult problem?",
            "Describe a time you had to learn a new technology quickly."
        ]
