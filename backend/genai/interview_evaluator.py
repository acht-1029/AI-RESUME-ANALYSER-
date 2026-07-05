import logging
from typing import Dict
from genai.gemini_client import GeminiClient

logger = logging.getLogger(__name__)

def evaluate_answer(question: str, answer: str) -> Dict:
    """
    Evaluate an interview answer.
    Returns a dictionary with a score (0-10), feedback, and an ideal answer.
    """
    client = GeminiClient()
    
    if not client.is_configured:
        return {
            "score": 5,
            "feedback": "Gemini API not configured. NLP fallback cannot properly grade qualitative answers.",
            "ideal_answer": "Try to use the STAR method (Situation, Task, Action, Result) when answering."
        }
        
    prompt = f"""
    You are an expert Technical Interviewer evaluating a candidate's answer.
    
    Question asked: "{question}"
    Candidate's answer: "{answer}"
    
    Evaluate the answer and provide your response strictly in the following format. 
    Do not use JSON formatting tags, just return the raw text exactly as structured below:
    
    SCORE: [Give a number from 0 to 10]
    FEEDBACK: [1 to 2 sentences explaining why they got this score and what they missed]
    IDEAL: [A concise, strong example answer using the STAR method]
    """
    
    try:
        response_text = client.generate_content(prompt)
        if not response_text:
            raise ValueError("Empty response from Gemini")
            
        lines = response_text.split('\n')
        result = {"score": 0, "feedback": "", "ideal_answer": ""}
        
        # Parse the structured response
        for line in lines:
            line = line.strip()
            if line.startswith("SCORE:"):
                try:
                    # Handle "SCORE: 8" or "SCORE: 8/10"
                    score_str = line.replace("SCORE:", "").strip().split('/')[0]
                    result["score"] = int(score_str)
                except ValueError:
                    result["score"] = 5
            elif line.startswith("FEEDBACK:"):
                result["feedback"] = line.replace("FEEDBACK:", "").strip()
            elif line.startswith("IDEAL:"):
                result["ideal_answer"] = line.replace("IDEAL:", "").strip()
                
        # If parsing failed but we got text, dump it into feedback so it's not lost
        if not result["feedback"]:
            result["feedback"] = response_text
            
        return result
    except Exception as e:
        logger.error(f"Evaluation failed: {e}")
        return {
            "score": 0,
            "feedback": "Error parsing evaluation from LLM.",
            "ideal_answer": "Use the STAR method."
        }
