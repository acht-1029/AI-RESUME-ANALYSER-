"""
Quick test script for Day 1 modules.
Drop your resume PDFs into the tests/test_samples/ folder, then run:

    cd c:\\Projects\\resume_analyzer
    python tests/test_day1.py

"""

import sys
import os
from pathlib import Path

# Fix Windows terminal encoding
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Add parent dir to path so imports work
sys.path.insert(0, str(Path(__file__).parent.parent))

from extractors.pdf_parser import extract_text, extract_text_safe
from extractors.section_splitter import split_sections
from extractors.skill_extractor import extract_skills, extract_skill_names, compare_skills


def test_pdf(pdf_path: str):
    """Run the full Day 1 pipeline on a single PDF."""
    print(f"\n{'='*70}")
    print(f"  TESTING: {os.path.basename(pdf_path)}")
    print(f"{'='*70}")

    # --- Step 1: Extract text ---
    print("\n[1] Step 1: PDF Text Extraction")
    result = extract_text_safe(pdf_path)
    if not result["success"]:
        print(f"   [FAIL] {result['error']}")
        return
    
    text = result["text"]
    print(f"   [OK] Extracted {len(text)} characters from {result['page_count']} page(s)")
    print(f"   Preview: {text[:150]}...")

    # --- Step 2: Split sections ---
    print("\n[2] Step 2: Section Splitting")
    sections = split_sections(text)
    for section_name, content in sections.items():
        preview = content[:80].replace('\n', ' ')
        print(f"   [{section_name}] ({len(content)} chars): {preview}...")

    # --- Step 3: Extract skills ---
    print("\n[3] Step 3: Skill Extraction")
    skills = extract_skills(text)
    print(f"   Found {len(skills)} skills:")
    for s in skills[:20]:  # Show top 20
        print(f"   - {s['skill']} (confidence: {s['confidence']}%, matched: \"{s['matched_text']}\", category: {s['category']})")
    if len(skills) > 20:
        print(f"   ... and {len(skills) - 20} more")

    # --- Step 4: Compare with a sample JD ---
    print("\n[4] Step 4: Skill Comparison (vs sample JD)")
    sample_jd = """
    We are looking for a Software Engineer with experience in Python, Java, 
    Docker, Kubernetes, AWS, CI/CD, React, PostgreSQL, Git, Agile, 
    Machine Learning, and REST API development. Strong communication 
    and problem solving skills required.
    """
    comparison = compare_skills(text, sample_jd)
    print(f"   Resume skills: {len(comparison['resume_skills'])}")
    print(f"   JD skills:     {len(comparison['jd_skills'])}")
    print(f"   Matching:      {comparison['matching_skills']}")
    print(f"   Missing:       {comparison['missing_skills']}")
    print(f"   Match %:       {comparison['match_percentage']}%")


def main():
    samples_dir = Path(__file__).parent / "test_samples"
    
    if not samples_dir.exists():
        print(f"[FAIL] Folder not found: {samples_dir}")
        print(f"       Create it and add some resume PDFs!")
        return

    pdfs = list(samples_dir.glob("*.pdf"))
    
    if not pdfs:
        print(f"[FAIL] No PDF files found in: {samples_dir}")
        print(f"       Drop some resume PDFs there and run again!")
        return

    print(f"Found {len(pdfs)} PDF(s) in {samples_dir}")
    
    for pdf in pdfs:
        test_pdf(str(pdf))

    print(f"\n{'='*70}")
    print(f"  DONE — Tested {len(pdfs)} resume(s)")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
