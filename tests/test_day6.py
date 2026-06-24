import sys
import json
from pathlib import Path

# Fix Windows terminal encoding
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.analyzer import ResumeAnalyzer

def main():
    print("=====================================================")
    print(" DAY 6: Unified Pipeline Test (NLP + GenAI)")
    print("=====================================================")
    
    # We will test using the actual sample PDFs
    sample_pdf_path = Path(__file__).parent / "test_samples" / "Tech" / "10089434.pdf"
    
    # Check if the file exists to avoid confusing errors
    if not sample_pdf_path.exists():
        print(f"[Error] Test file not found: {sample_pdf_path}")
        return
        
    sample_jd = """
    We are looking for a Software Engineer with experience in building web applications.
    Requirements:
    - Experience with frontend frameworks.
    - Solid understanding of backend development and REST APIs.
    - Familiarity with SQL or NoSQL databases.
    - Cloud deployment experience is a plus.
    - Strong problem-solving and communication skills.
    """
    
    print(f"Testing FULL Analysis on: {sample_pdf_path.name}")
    print("This runs the TF-IDF scoring, gap analysis, and Gemini AI features in one call...\n")
    
    analyzer = ResumeAnalyzer()
    
    # Run the full unified method
    result = analyzer.full_analysis(str(sample_pdf_path), sample_jd)
    
    if not result["success"]:
        print(f"Analysis Failed: {result['error']}")
        return
        
    print("--- 1. NLP ATS SCORING ---")
    print(f"Final Score: {result['scores']['overall_score']} / 100")
    print(f"Skills Found in Resume: {result['skills_analysis']['resume_total_skills']}")
    print(f"Missing JD Skills: {', '.join(result['skills_analysis']['missing_skills'])}")
    
    print("\n--- 2. GEN AI RESUME COACH ---")
    for i, suggestion in enumerate(result['genai_coach']['resume_improvement_suggestions'], 1):
        print(f"{i}. {suggestion}")
        
    print("\n--- 3. GEN AI MOCK INTERVIEW QUESTIONS ---")
    for i, question in enumerate(result['genai_coach']['mock_interview_questions'], 1):
        print(f"Q{i}: {question}")
        
    print("\n[Analysis Complete]")

if __name__ == "__main__":
    main()
