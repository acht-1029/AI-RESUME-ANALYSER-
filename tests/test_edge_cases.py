import sys
import json
from pathlib import Path

# Fix Windows terminal encoding
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.analyzer import ResumeAnalyzer

def print_result(title, result):
    print(f"\n{'='*60}")
    print(f" TEST: {title}")
    print(f"{'='*60}")
    
    if not result.get("success"):
        print(f"❌ FAILED SAFELY: {result.get('error')}")
        return
        
    scores = result.get("scores", {})
    skills = result.get("skills_analysis", {})
    
    print(f"Overall ATS Score: {scores.get('overall_score')}/100")
    print(f"Skills Match: {skills.get('resume_total_skills')} resume skills vs {skills.get('jd_total_skills')} JD skills")
    print(f"Matching: {len(skills.get('matching_skills', []))} | Missing: {len(skills.get('missing_skills', []))}")


def main():
    analyzer = ResumeAnalyzer()
    
    # We will use the existing test sample for the resume
    pdf_path = "tests/test_samples/10624813.pdf"
    
    if not Path(pdf_path).exists():
        print(f"[ERROR] Test PDF not found at {pdf_path}")
        return
        
    # --- TEST 1: Completely Unrelated Job Description ---
    nurse_jd = """
    Registered Nurse needed. Must have an active RN license, CPR certification, 
    and experience in patient care, IV administration, and electronic health records (EHR).
    Knowledge of HIPAA regulations and bedside manner is required.
    """
    result_unrelated = analyzer.analyze(pdf_path, nurse_jd)
    print_result("Completely Unrelated JD (Nurse vs Engineer)", result_unrelated)

    # --- TEST 2: Empty / Corrupt PDF Handling ---
    result_corrupt = analyzer.analyze("tests/test_samples/does_not_exist.pdf", nurse_jd)
    print_result("Corrupt / Missing PDF Handling", result_corrupt)
    
    # --- TEST 3: Extreme Minimum JD ---
    min_jd = "Agile Python"
    result_min = analyzer.analyze(pdf_path, min_jd)
    print_result("Extremely Short JD (2 skills)", result_min)

if __name__ == "__main__":
    main()
