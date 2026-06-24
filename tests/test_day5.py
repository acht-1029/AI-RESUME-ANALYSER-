import sys
from pathlib import Path

# Fix Windows terminal encoding
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, str(Path(__file__).parent.parent))

from genai.interview_generator import generate_interview_questions
from genai.interview_evaluator import evaluate_answer

def main():
    print("=====================================================")
    print(" DAY 5: Gemini Interview System Test")
    print("=====================================================")
    
    resume_skills = ["Python", "AWS", "Machine Learning", "Docker", "REST API"]
    sample_jd = """
    We are looking for a Backend Engineer. Must have experience building scalable REST APIs 
    in Python and deploying them to AWS using Docker. Bonus if you have experience integrating 
    Machine Learning models into backend services.
    """
    
    print("\n--- PHASE 1: GENERATING QUESTIONS ---")
    print(f"Candidate Skills: {', '.join(resume_skills)}")
    print("Generating tailored questions...\n")
    
    questions = generate_interview_questions(resume_skills, sample_jd)
    
    if not questions:
        print("[Error] Failed to generate questions.")
        return
        
    for i, q in enumerate(questions, 1):
        print(f"Q{i}: {q}")
        
    print("\n--- PHASE 2: EVALUATING AN ANSWER ---")
    
    # We will test the evaluator on the first generated question
    test_question = questions[0]
    
    # Simulating a mediocre, vague answer from the candidate
    bad_answer = "Yeah, I use Python a lot. I built some APIs and put them on a server. It worked pretty well."
    
    print(f"Interviewer: {test_question}")
    print(f"Candidate: {bad_answer}\n")
    
    print("Evaluating answer...\n")
    evaluation = evaluate_answer(test_question, bad_answer)
    
    print(f"SCORE: {evaluation['score']} / 10")
    print(f"FEEDBACK: {evaluation['feedback']}")
    print(f"IDEAL ANSWER: {evaluation['ideal_answer']}")

if __name__ == "__main__":
    main()
