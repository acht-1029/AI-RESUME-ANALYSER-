"""
Skill Extractor
================
Extracts skills from resume text or JD text by fuzzy-matching against the
curated skills database. Handles common variations:
    - "UI / UX" → matches "UI/UX"
    - "React JS" → matches "React.js"
    - "machine learning" → matches "Machine Learning"
    - "AWS (Amazon Web Services)" → matches both "AWS" and "Amazon Web Services"

Uses rapidfuzz for fuzzy string matching + additional normalization heuristics.
"""

import re
import logging
from typing import Dict, List, Set

from rapidfuzz import fuzz, process

from data.skills_db import SKILLS_DB, SKILLS_DB_LOWER, get_category

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
FUZZY_THRESHOLD = 85          # Minimum similarity score (0–100) to accept a match
EXACT_BONUS_THRESHOLD = 95    # Above this, we consider it a near-exact match
MIN_SKILL_LENGTH = 2          # Ignore tokens shorter than this (avoids "C" matching "CI/CD" noise)
MIN_LENGTH_RATIO = 0.6        # Candidate must be at least 60% as long as the DB skill

# Common English words that should NEVER be matched as skills.
# These cause false positives like "in" → "Gin", "using" → "Nursing", etc.
STOP_WORDS: set[str] = {
    # Articles, prepositions, conjunctions
    "a", "an", "the", "in", "on", "at", "to", "for", "of", "with", "by",
    "from", "up", "as", "is", "it", "or", "and", "but", "not", "no", "so",
    "if", "do", "be", "we", "he", "me", "my", "am", "vs",
    # Common verbs / words that cause false positives
    "using", "used", "use", "open", "flow", "design", "building",
    "development", "developed", "developing", "learning", "based",
    "management", "managing", "manager", "technology", "systems",
    "system", "data", "analysis", "evaluation", "testing", "platform",
    "service", "services", "application", "applications", "engineering",
    "working", "experience", "strategic", "waiting", "making",
    "planning", "solutions", "optimization", "processing",
    "intelligence", "network", "model", "models", "tools",
    "strong", "focus", "team", "project", "projects", "solid",
}


# ---------------------------------------------------------------------------
# Text normalization — bridges the gap between resume text and DB entries
# ---------------------------------------------------------------------------

def _normalize(text: str) -> str:
    """
    Normalize text for better fuzzy matching.
    
    Handles:
        "UI / UX"       → "ui/ux"
        "React.JS"      → "react.js"
        "  Docker  "    → "docker"
        "Node .js"      → "node.js"
        "C ++"          → "c++"
    """
    t = text.strip().lower()
    # Collapse spaces around slashes:  "UI / UX" → "UI/UX"
    t = re.sub(r'\s*/\s*', '/', t)
    # Collapse spaces around dots:     "Node .js" → "Node.js"
    t = re.sub(r'\s*\.\s*', '.', t)
    # Collapse spaces around plus:     "C ++" → "C++"
    t = re.sub(r'\s*\+\s*', '+', t)
    # Collapse spaces around hyphens:  "e - commerce" → "e-commerce"
    t = re.sub(r'\s*-\s*', '-', t)
    # Collapse multiple spaces
    t = re.sub(r'\s+', ' ', t)
    return t


# Regex to detect parenthesized content: captures "before", "inside", and full text
_PAREN_PATTERN = re.compile(r'^(.+?)\s*[\(\[]+\s*(.+?)\s*[\)\]]+\s*$')


# ---------------------------------------------------------------------------
# Alias / Synonym map — maps abbreviations ↔ full forms
# Both directions are registered so "ML" matches "Machine Learning" and vice versa
# Keys MUST be lowercase
# ---------------------------------------------------------------------------

_ALIASES_RAW: dict[str, str] = {
    # --- Data Science & ML ---
    "ml": "Machine Learning",
    "dl": "Deep Learning",
    "ai": "Artificial Intelligence",
    "nlp": "Natural Language Processing",
    "cv": "Computer Vision",
    "rl": "Reinforcement Learning",
    "eda": "Exploratory Data Analysis",
    "genai": "Generative AI",
    "llm": "Large Language Models",
    "rag": "Retrieval Augmented Generation",

    # --- Programming Languages ---
    "js": "JavaScript",
    "ts": "TypeScript",
    "py": "Python",

    # --- Web / Frameworks ---
    "react": "React.js",
    "vue": "Vue.js",
    "next": "Next.js",
    "nuxt": "Nuxt.js",
    "express": "Express.js",
    "node": "Node.js",
    "tailwind": "Tailwind CSS",

    # --- Cloud & DevOps ---
    "aws": "Amazon Web Services",
    "gcp": "Google Cloud",
    "k8s": "Kubernetes",
    "ci/cd": "CI/CD",
    "gh actions": "GitHub Actions",

    # --- Databases ---
    "postgres": "PostgreSQL",
    "mongo": "MongoDB",
    "dynamo": "DynamoDB",
    "es": "Elasticsearch",
    "mssql": "SQL Server",

    # --- Data Engineering ---
    "etl": "ETL",
    "spark": "Apache Spark",
    "kafka": "Apache Kafka",
    "bq": "BigQuery",

    # --- Business & Management ---
    "pm": "Project Management",
    "ba": "Business Analysis",
    "scm": "Supply Chain Management",
    "crm": "CRM",
    "erp": "ERP",
    "okr": "OKR",
    "kpi": "Key Performance Indicators",
    "hr": "Human Resources",
    "hris": "HRIS",
    "biz dev": "Business Development",
    "bi": "Business Intelligence",

    # --- Finance ---
    "m&a": "Mergers and Acquisitions",
    "dcf": "DCF",
    "p&l": "P&L Management",
    "gaap": "GAAP",
    "ifrs": "IFRS",
    "kyc": "KYC",
    "aml": "AML",
    "sox": "SOX Compliance",

    # --- Healthcare ---
    "ehr": "Electronic Health Records",
    "emr": "EMR",
    "hipaa": "HIPAA",
    "gmp": "Good Manufacturing Practices",
    "fda": "FDA Regulations",

    # --- Marketing ---
    "seo": "Search Engine Optimization",
    "sem": "Search Engine Marketing",
    "ppc": "Pay Per Click",
    "cro": "Conversion Rate Optimization",
    "ga4": "GA4",
    "pr": "Public Relations",

    # --- Design ---
    "ui": "UI Design",
    "ux": "UX Design",
    "ui/ux": "UI/UX",

    # --- Security ---
    "iam": "IAM",
    "sso": "SSO",
    "rbac": "RBAC",
    "jwt": "JWT",

    # --- Legal ---
    "ip": "Intellectual Property",
    "gdpr": "GDPR",

    # --- Education ---
    "lms": "LMS",
    "edtech": "EdTech",

    # --- Tools ---
    "tdd": "Test Driven Development",
    "bdd": "BDD",
    "oop": "OOP",
}

# Build bidirectional alias map: abbreviation → canonical, full form → canonical
# This lets us match in BOTH directions
_ALIAS_TO_CANONICAL: dict[str, str] = {}  # lowercase alias → canonical DB skill name

for _abbr, _full in _ALIASES_RAW.items():
    # abbr → the full form (if it's in DB) or the abbr itself (if it's in DB)
    _full_lower = _full.lower()
    _abbr_lower = _abbr.lower()

    # Check which form exists in the skills DB
    if _full_lower in SKILLS_DB_LOWER:
        _ALIAS_TO_CANONICAL[_abbr_lower] = _full
    if _abbr_lower in SKILLS_DB_LOWER:
        # Also map the full form back to the canonical short form if that's what's in DB
        # But prefer the full form as canonical
        if _full_lower not in SKILLS_DB_LOWER:
            _ALIAS_TO_CANONICAL[_full_lower] = _abbr.upper()

    # Both might be in DB (e.g., "AWS" and "Amazon Web Services" are both listed)
    # In that case, map the abbreviation to itself so both get matched
    if _abbr_lower in SKILLS_DB_LOWER and _full_lower in SKILLS_DB_LOWER:
        _ALIAS_TO_CANONICAL[_abbr_lower] = next(
            s for s in SKILLS_DB if s.lower() == _abbr_lower
        )


# Pre-build normalized lookup for the skills DB
_SKILLS_NORMALIZED: dict[str, str] = {}  # normalized_form → original_form
for _skill in SKILLS_DB:
    _norm = _normalize(_skill)
    _SKILLS_NORMALIZED[_norm] = _skill

# Also build a list of (normalized, original) for rapidfuzz process
_SKILLS_NORM_LIST: list[str] = list(_SKILLS_NORMALIZED.keys())
_SKILLS_ORIG_LIST: list[str] = [_SKILLS_NORMALIZED[n] for n in _SKILLS_NORM_LIST]


# ---------------------------------------------------------------------------
# Candidate extraction — pulls potential skill phrases from text
# ---------------------------------------------------------------------------

def _extract_candidates(text: str) -> List[str]:
    """
    Extract candidate skill phrases from text.
    
    Strategy:
        1. Split by common delimiters: commas, pipes, semicolons, bullet points, newlines
        2. Handle parenthesized text: "AWS(AMAZON)" → candidates: ["AWS(AMAZON)", "AWS", "AMAZON"]
        3. Also generate n-grams (1, 2, 3 word) from each chunk for multi-word skills
           like "Machine Learning" or "Project Management"
        4. Return all candidates for fuzzy matching
    """
    # Split on common resume/JD delimiters
    chunks = re.split(r'[,;|•●◦▪▸►\n\r\t]+', text)
    
    candidates: List[str] = []
    
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
        
        # The chunk itself is a candidate (handles "Machine Learning", "UI/UX", etc.)
        candidates.append(chunk)
        
        # --- Handle parenthesized text ---
        # "AWS(AMAZON)"           → also try "AWS" and "AMAZON"
        # "ML(Machine Learning)"  → also try "ML" and "Machine Learning"
        # "React (JS)"            → also try "React" and "JS"
        paren_match = _PAREN_PATTERN.match(chunk.strip())
        if paren_match:
            before = paren_match.group(1).strip()
            inside = paren_match.group(2).strip()
            if before:
                candidates.append(before)
            if inside:
                candidates.append(inside)
        
        # Also split by spaces and generate n-grams for multi-word skills
        # Strip parenthesized content first so n-grams are clean
        clean_chunk = re.sub(r'[\(\[].+?[\)\]]', ' ', chunk).strip()
        words = clean_chunk.split()
        for n in range(1, 4):  # 1-grams, 2-grams, 3-grams
            for i in range(len(words) - n + 1):
                ngram = " ".join(words[i:i + n])
                candidates.append(ngram)
    
    # Deduplicate while preserving order
    seen: Set[str] = set()
    unique: List[str] = []
    for c in candidates:
        c_norm = _normalize(c)
        if c_norm not in seen and len(c_norm) >= MIN_SKILL_LENGTH:
            seen.add(c_norm)
            unique.append(c)
    
    return unique


# ---------------------------------------------------------------------------
# Main extraction function
# ---------------------------------------------------------------------------

def extract_skills(
    text: str,
    threshold: int = FUZZY_THRESHOLD,
    deduplicate: bool = True,
) -> List[Dict]:
    """
    Extract skills from text by fuzzy-matching against the skills database.
    
    Args:
        text: Resume text, JD text, or a specific section (e.g., skills section).
        threshold: Minimum fuzzy similarity score (0–100). Default: 80.
        deduplicate: If True, return each skill only once (highest confidence).
    
    Returns:
        List of matched skills, each as:
        {
            "skill": "UI/UX",              # Canonical name from DB
            "matched_text": "UI / UX",      # What was found in the text
            "confidence": 87,               # Fuzzy match score (0–100)
            "category": "Design & Creative" # Category from skills_db
        }
        
    Example:
        >>> extract_skills("Python, React JS, UI / UX, machine learning")
        [
            {"skill": "Python", "matched_text": "Python", "confidence": 100, "category": "Programming Languages"},
            {"skill": "React.js", "matched_text": "React JS", "confidence": 82, "category": "Web Frontend"},
            {"skill": "UI/UX", "matched_text": "UI / UX", "confidence": 87, "category": "Design & Creative"},
            {"skill": "Machine Learning", "matched_text": "machine learning", "confidence": 100, "category": "Data Science & ML"},
        ]
    """
    if not text or not text.strip():
        return []
    
    candidates = _extract_candidates(text)
    matches: Dict[str, Dict] = {}  # skill_lower → best match info
    
    for candidate in candidates:
        candidate_norm = _normalize(candidate)
        
        # --- Step 1: Try exact normalized match (fastest) ---
        if candidate_norm in _SKILLS_NORMALIZED:
            skill_original = _SKILLS_NORMALIZED[candidate_norm]
            skill_key = skill_original.lower()
            
            match_info = {
                "skill": skill_original,
                "matched_text": candidate.strip(),
                "confidence": 100,
                "category": get_category(skill_original),
            }
            
            # Keep the highest-confidence match for each skill
            if skill_key not in matches or matches[skill_key]["confidence"] < 100:
                matches[skill_key] = match_info
            continue
        
        # --- Step 2: Try alias/synonym lookup ---
        # "ML" → "Machine Learning", "K8s" → "Kubernetes", etc.
        if candidate_norm in _ALIAS_TO_CANONICAL:
            skill_original = _ALIAS_TO_CANONICAL[candidate_norm]
            skill_key = skill_original.lower()
            
            match_info = {
                "skill": skill_original,
                "matched_text": candidate.strip(),
                "confidence": 100,  # Alias match = deterministic
                "category": get_category(skill_original),
            }
            
            if skill_key not in matches or matches[skill_key]["confidence"] < 100:
                matches[skill_key] = match_info
            continue
        
        # --- Step 3: Fuzzy match against normalized DB ---
        # Only try fuzzy for candidates with reasonable length
        if len(candidate_norm) < MIN_SKILL_LENGTH:
            continue
        
        # Skip common English words — they cause false positives
        if candidate_norm in STOP_WORDS:
            continue
            
        result = process.extractOne(
            candidate_norm,
            _SKILLS_NORM_LIST,
            scorer=fuzz.ratio,
            score_cutoff=threshold,
        )
        
        if result:
            matched_norm, score, idx = result
            skill_original = _SKILLS_ORIG_LIST[idx]
            skill_key = skill_original.lower()
            
            # For short skills (1-2 chars like "C", "R"), require higher threshold
            if len(skill_original) <= 2 and score < 100:
                continue
            
            # Length ratio guard: reject if candidate is much shorter than the skill
            # Prevents: "in" → "Gin", "as" → "AWS", "flow" → "MLflow"
            len_ratio = len(candidate_norm) / len(matched_norm) if matched_norm else 0
            if len_ratio < MIN_LENGTH_RATIO:
                continue
            
            match_info = {
                "skill": skill_original,
                "matched_text": candidate.strip(),
                "confidence": int(score),
                "category": get_category(skill_original),
            }
            
            # Keep the highest-confidence match
            if skill_key not in matches or matches[skill_key]["confidence"] < score:
                matches[skill_key] = match_info
    
    results = list(matches.values())
    
    # Sort by confidence (highest first), then alphabetically
    results.sort(key=lambda x: (-x["confidence"], x["skill"]))
    
    logger.info(f"Extracted {len(results)} skills from text ({len(candidates)} candidates checked).")
    return results


def extract_skill_names(text: str, threshold: int = FUZZY_THRESHOLD) -> List[str]:
    """
    Convenience wrapper: returns just the skill names (no metadata).
    
    Args:
        text: Resume or JD text.
        threshold: Minimum fuzzy match score.
    
    Returns:
        Sorted list of canonical skill names.
        
    Example:
        >>> extract_skill_names("Python, React JS, UI / UX")
        ["Python", "React.js", "UI/UX"]
    """
    matches = extract_skills(text, threshold=threshold)
    return [m["skill"] for m in matches]


def compare_skills(
    resume_text: str,
    jd_text: str,
    threshold: int = FUZZY_THRESHOLD,
) -> Dict:
    """
    Compare skills found in resume vs. JD.
    
    Args:
        resume_text: Full resume text or skills section.
        jd_text: Job description text.
        threshold: Minimum fuzzy match score.
    
    Returns:
        {
            "resume_skills": ["Python", "Docker", ...],
            "jd_skills": ["Python", "Docker", "Kubernetes", ...],
            "matching_skills": ["Python", "Docker"],
            "missing_skills": ["Kubernetes"],
            "extra_skills": ["React"],            # In resume but not in JD
            "match_percentage": 66.7              # matching / jd_skills × 100
        }
    """
    resume_skills = set(extract_skill_names(resume_text, threshold))
    jd_skills = set(extract_skill_names(jd_text, threshold))
    
    matching = resume_skills & jd_skills
    missing = jd_skills - resume_skills
    extra = resume_skills - jd_skills
    
    match_pct = (len(matching) / len(jd_skills) * 100) if jd_skills else 0.0
    
    return {
        "resume_skills": sorted(resume_skills),
        "jd_skills": sorted(jd_skills),
        "matching_skills": sorted(matching),
        "missing_skills": sorted(missing),
        "extra_skills": sorted(extra),
        "match_percentage": round(match_pct, 1),
    }
