import sys
from pathlib import Path

# Fix Windows terminal encoding
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, str(Path(__file__).parent.parent))

from genai.suggestions import generate_resume_suggestions

def main():
    print("=====================================================")
    print(" DAY 4: Gemini Resume Coach Test")
    print("=====================================================")
    
    # We simulate a candidate who failed the ATS filter for these skills
    missing_skills = ["Docker", "Kubernetes", "AWS", "CI/CD", "Machine Learning"]
    
    sample_jd = """
    We are looking for a Senior DevOps Engineer with deep experience in cloud infrastructure, 
    container orchestration, and automated deployment pipelines. The ideal candidate will have 
    hands-on experience building CI/CD workflows and deploying machine learning models to production.
    """
    
    print(f"\n[Simulating] Candidate is missing these skills: {', '.join(missing_skills)}")
    print("Requesting personalized AI coaching suggestions from Gemini...\n")
    
    suggestions = generate_resume_suggestions(missing_skills, sample_jd)
    
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion}")
        print()

if __name__ == "__main__":
    main()
