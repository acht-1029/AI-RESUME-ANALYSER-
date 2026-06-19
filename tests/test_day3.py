import sys
import json
from pathlib import Path

# Fix Windows terminal encoding
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.analyzer import ResumeAnalyzer

def main():
    analyzer = ResumeAnalyzer()
    
    samples_dir = Path(__file__).parent / "test_samples"
    pdfs = list(samples_dir.rglob("*.pdf"))
    
    if not pdfs:
        print(f"[FAIL] No PDF files found in: {samples_dir}")
        print(f"       Drop some resume PDFs there and run again!")
        return
        
    sample_jd = """
    We are looking for a Software Engineer with experience in Python, Java, 
    Docker, Kubernetes, AWS, CI/CD, React, PostgreSQL, Git, Agile, 
    Machine Learning, and REST API development. Strong communication 
    and problem solving skills required.
    """
    
    print(f"Found {len(pdfs)} PDF(s) to analyze.\n")
    
    for pdf_path in pdfs:
        # Show which folder the PDF came from
        print(f"[{pdf_path.parent.name}] Running full unified NLP Pipeline on {pdf_path.name}...")
        
        result = analyzer.analyze(str(pdf_path), sample_jd)
        
        # Print the output in a nice JSON format so the backend team can see the structure
        print("\n=== UNIFIED API RESPONSE ===")
        print(json.dumps(result, indent=2))
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()
