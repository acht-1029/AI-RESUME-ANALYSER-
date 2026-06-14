# ATS Resume Analyzer + Interview Prep Coach
## Complete Project Planning Document
**NextGen Data Minds — Summer Project Program 2026**
**Problem Statement 5 | Team Duration: 14 June – 28 June 2026**

---

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Team Members & Roles](#2-team-members--roles)
3. [Tech Stack](#3-tech-stack)
4. [Complete Project Flow](#4-complete-project-flow)
5. [File Structure](#5-file-structure)
6. [API Endpoints](#6-api-endpoints)
7. [Database Schema](#7-database-schema)
8. [Work Distribution](#8-work-distribution)
9. [15-Day Timeline](#9-15-day-timeline)
10. [Feature Coverage Checklist](#10-feature-coverage-checklist)
11. [CORS — How React Talks to FastAPI](#11-cors--how-react-talks-to-fastapi)
12. [Git Workflow](#12-git-workflow)
13. [Submission Requirements](#13-submission-requirements)
14. [Team Rules](#14-team-rules)

---

## 1. Project Overview

### Problem Being Solved
Students apply to jobs with poor resume-JD alignment and enter interviews underprepared.
Existing tools are expensive and generic.

### Our Solution
An AI + NLP powered tool that:
- Analyzes a resume PDF against any job description
- Gives an ATS compatibility score using real NLP (cosine similarity)
- Identifies matched and missing keywords
- Suggests resume improvements using Gemini AI
- Generates role-specific interview questions
- Enables mock interview practice with AI evaluation
- Tracks progress across multiple job applications

### Resume Impact Line
> *"Developed an AI-powered ATS resume analyzer and interview prep assistant that matches resumes
> with job descriptions using NLP, identifies skill gaps, and generates role-specific interview questions."*

---

## 2. Team Members & Roles

| Member | Role | Core Responsibility |
|---|---|---|
| **Ansh Chaturvedi** | Leader + AI/Backend | FastAPI, Gemini API, PDF parsing, Integration |
| **MERN Stack Dev** | Frontend Lead | React UI — all 4 pages, Axios API calls |
| **Docker/DevOps Guy** | Database + Testing + Git + Deploy | SQLite, test_api.py, Render deployment |
| **NLP/ML Guy** | NLP Engine + Prompts | ml_utils.py, prompts.py |
| **UI/UX Guy** | Content + Docs + Demo | README, PPT, demo video, submission |

---

## 3. Tech Stack

### Backend
| Tool | Purpose |
|---|---|
| Python 3.11 | Core language |
| FastAPI | REST API framework |
| pdfplumber | Extract text from resume PDF |
| Gemini API (gemini-1.5-flash) | AI suggestions, interview Qs, mock eval |
| SQLite | Store analyses and mock sessions |
| spaCy / NLTK | NLP keyword extraction |
| scikit-learn | TF-IDF + cosine similarity for ATS score |

### Frontend
| Tool | Purpose |
|---|---|
| React 18 | UI framework (MERN guy's strength) |
| Axios | HTTP requests to FastAPI backend |
| React Router | Page navigation (4 pages) |
| CSS / Tailwind | Styling |

### DevOps / Other
| Tool | Purpose |
|---|---|
| Git + GitHub | Version control |
| Render.com | Free backend deployment (live URL) |
| Vercel / Netlify | Free React frontend deployment |
| Postman / test_api.py | API testing |

### Backend Install
```bash
pip install fastapi uvicorn pdfplumber google-generativeai python-multipart
pip install spacy scikit-learn nltk
python -m spacy download en_core_web_sm
```

### Frontend Install
```bash
npx create-react-app frontend
cd frontend
npm install axios react-router-dom
npm start
```

---

## 4. Complete Project Flow

### End-to-End Flow (How Everything Works Together)

```
┌─────────────────────────────────────────────────────┐
│           USER (opens React app on port 3000)       │
└────────────────────────┬────────────────────────────┘
                         │
                         │  Uploads resume PDF
                         │  Pastes job description
                         │  Clicks "Analyze"
                         ▼
┌─────────────────────────────────────────────────────┐
│           REACT FRONTEND (src/App.jsx)              │
│                                                     │
│  Uses Axios to send HTTP POST request:              │
│  POST http://localhost:8000/analyze                 │
│  Body: FormData { resume: file, job_description }   │
└────────────────────────┬────────────────────────────┘
                         │
                         │  HTTP Request (crosses origins)
                         │  CORS middleware allows this
                         ▼
┌─────────────────────────────────────────────────────┐
│          FASTAPI BACKEND (main.py) — port 8000      │
│                                                     │
│  Step 1: Receive PDF file + JD text                 │
│  Step 2: Extract text from PDF using pdfplumber     │
│  Step 3: Send text to ml_utils.py for NLP scoring   │
│  Step 4: Send text to Gemini for suggestions        │
│  Step 5: Save result to SQLite database             │
│  Step 6: Return JSON response to React              │
└──────┬─────────────────┬───────────────────────────┘
       │                 │
       ▼                 ▼
┌─────────────┐   ┌─────────────────────────────────┐
│  ml_utils   │   │         GEMINI API               │
│  (NLP Guy)  │   │                                  │
│             │   │  - Resume improvement suggestions│
│  - spaCy    │   │  - Interview questions            │
│  - TF-IDF   │   │  - Mock answer evaluation        │
│  - Cosine   │   │  - Summary generation            │
│    Similarity│   └─────────────────────────────────┘
│  - ATS Score│
│  - Matched  │
│  - Missing  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────────────┐
│                SQLite DATABASE                      │
│                                                     │
│  Table: analyses       Table: mock_sessions         │
│  - resume_name         - job_role                   │
│  - ats_score           - total_score                │
│  - result_json         - session_json               │
│  - created_at          - created_at                 │
└─────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────┐
│         JSON RESPONSE back to React                 │
│                                                     │
│  {                                                  │
│    "ats_score": 72,                                 │
│    "matched_keywords": ["Python", "FastAPI"],       │
│    "missing_keywords": ["Docker", "PostgreSQL"],    │
│    "suggestions": ["Add Docker to projects..."],    │
│    "verdict": "Moderate Match",                     │
│    "interview_questions": [...],                    │
│    "summary": "Strong Python background but..."    │
│  }                                                  │
└─────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────┐
│         REACT DISPLAYS RESULTS                      │
│                                                     │
│  Page 1: /          → Upload + Analyze              │
│  Page 2: /results   → ATS Score + Keywords          │
│  Page 3: /mock      → Interview Questions + Mock    │
│  Page 4: /history   → Progress Tracking             │
└─────────────────────────────────────────────────────┘
```

### Mock Interview Sub-Flow

```
React shows Question 1
       │
       ▼
User types answer in textarea
       │
       ▼
Axios POST /mock-answer → FastAPI → Gemini evaluates
       │
       ▼
React shows: score, feedback, ideal answer
       │
       ▼
User clicks Next → Question 2 → repeat for all 7
       │
       ▼
After question 7:
Axios POST /mock-session-complete → FastAPI saves to SQLite
       │
       ▼
React shows final scorecard with % and performance grade
```

### NLP Scoring Sub-Flow (ml_utils.py)

```
resume_text + jd_text
       │
       ▼
spaCy extracts named entities + noun chunks (keywords)
       │
       ▼
scikit-learn TF-IDF vectorizes both documents
       │
       ▼
Cosine Similarity calculated → raw score (0.0 to 1.0)
       │
       ▼
Scale to 0-100 → ATS Score integer
       │
       ▼
Python set operations:
  resume_kw = set(extract_keywords(resume_text))
  jd_kw     = set(extract_keywords(jd_text))
  matched   = resume_kw ∩ jd_kw
  missing   = jd_kw - resume_kw
       │
       ▼
Return: ats_score (int), matched (list), missing (list)
```

---

## 5. File Structure

```
ats-resume-analyzer/
│
├── backend/                      ← All Python backend files
│   ├── main.py                   ← Ansh — FastAPI app, all 7 endpoints
│   ├── database.py               ← Ansh + Docker Guy — SQLite logic
│   ├── ml_utils.py               ← NLP Guy — NLP scoring engine
│   ├── prompts.py                ← NLP Guy — All Gemini prompts
│   └── requirements.txt          ← Ansh — All pip dependencies
│
├── frontend/                     ← React app (MERN Guy)
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadPage.jsx    ← Page 1: upload resume + JD
│   │   │   ├── ResultsPage.jsx   ← Page 2: ATS score + keywords
│   │   │   ├── MockTestPage.jsx  ← Page 3: mock interview
│   │   │   └── HistoryPage.jsx   ← Page 4: progress tracking
│   │   ├── App.jsx               ← Router + main layout
│   │   ├── api.js                ← All Axios API calls in one place
│   │   └── index.js
│   └── package.json
│
├── tests/                        ← API testing
│   ├── test_api.py               ← Docker Guy — Tests all 7 endpoints
│   └── test_resume.pdf           ← Docker Guy — Sample PDF for testing
│
├── data/                         ← Dataset files
│   └── skills_data.csv           ← UI/UX Guy — 200+ tech skills
│
├── .env.example                  ← Docker Guy — API key template
├── .gitignore                    ← Ansh — Files not to push to GitHub
└── README.md                     ← UI/UX Guy — Setup + documentation
```

---

## 6. API Endpoints

All endpoints run at `http://localhost:8000`
Interactive docs at `http://localhost:8000/docs`

### GET /
Health check
```json
{ "message": "ATS Resume Analyzer API is running!" }
```

### POST /analyze
Main endpoint — MERN guy's most important call
```
Input (FormData):
  resume          → PDF file
  job_description → string
  job_role        → string (e.g. "Python Backend Developer")

Output:
{
  "status": "success",
  "filename": "resume.pdf",
  "analysis": {
    "ats_score": 72,
    "matched_keywords": ["Python", "FastAPI", "SQL"],
    "missing_keywords": ["Docker", "PostgreSQL"],
    "suggestions": ["Add Docker experience to projects"],
    "verdict": "Moderate Match",
    "summary": "Strong Python background but missing DevOps skills."
  },
  "interview_questions": [
    { "question": "...", "difficulty": "Easy", "topic": "Python" }
  ]
}
```

### GET /history
All past analyses — used in HistoryPage.jsx
```json
{
  "status": "success",
  "total": 5,
  "history": [{ "id", "resume_name", "ats_score", "analysis", "created_at" }]
}
```

### POST /interview-questions
Generate questions for any job role
```
Input: job_role (string), skills (comma separated string)
Output: { "questions": [{ "question", "difficulty", "topic" }] }
```

### POST /mock-answer
Evaluate one mock answer — called for each of 7 questions
```
Input: question (string), user_answer (string), job_role (string)
Output: {
  "evaluation": {
    "score": 7,
    "verdict": "Good",
    "feedback": "Good explanation but missed async support...",
    "ideal_answer": "FastAPI is a modern Python web framework...",
    "missing_points": ["Did not mention async"],
    "strong_points": ["Correctly mentioned speed advantage"]
  }
}
```

### POST /mock-session-complete
Save full session after all 7 answers
```
Input:
  job_role     → string
  session_data → JSON string of array:
    [{ "question", "user_answer", "score" }, ...]

Output: {
  "total_score": 46,
  "out_of": 70,
  "percentage": 65,
  "performance": "Good"
}
```

### GET /mock-history
All past mock sessions — used in HistoryPage.jsx
```json
{ "history": [{ "job_role", "total_score", "percentage", "session", "created_at" }] }
```

---

## 7. Database Schema

### Table: analyses
```sql
CREATE TABLE IF NOT EXISTS analyses (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    resume_name  TEXT,
    ats_score    INTEGER,
    result_json  TEXT,
    created_at   TEXT
);
```

### Table: mock_sessions
```sql
CREATE TABLE IF NOT EXISTS mock_sessions (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    job_role     TEXT,
    total_score  INTEGER,
    session_json TEXT,
    created_at   TEXT
);
```

---

## 8. Work Distribution

---

### Ansh Chaturvedi — Leader + AI/Backend

**Branch:** `backend`
**Files:** `backend/main.py`, `backend/database.py`, `backend/requirements.txt`

**Full task list:**
- Day 1: Create GitHub repo, add all members as collaborators, push planning.md
- Day 2: Setup FastAPI, CORS middleware, health check endpoint working
- Day 3: PDF text extraction with pdfplumber working
- Day 4: Gemini API connected, /analyze endpoint returning data
- Day 5: Import ml_utils.py functions, integrate NLP scoring into /analyze
- Day 6: All 7 endpoints complete and manually tested via /docs
- Day 7: Checkpoint — share Postman collection or /docs URL with team
- Day 8-10: Fix integration bugs as MERN guy connects React
- Day 11-13: Final bug fixes, help teammates
- Day 14: Final merge, submission prep

**Key code — how NLP + Gemini combine in main.py:**
```python
from ml_utils import calculate_ats_score, find_matched_keywords, find_missing_keywords
from prompts import suggestions_prompt, interview_questions_prompt, mock_eval_prompt

@app.post("/analyze")
async def analyze_resume(resume, job_description, job_role):

    resume_text = extract_text_from_pdf(pdf_bytes)

    # NLP Guy's functions handle scoring
    ats_score = calculate_ats_score(resume_text, job_description)
    matched   = find_matched_keywords(resume_text, job_description)
    missing   = find_missing_keywords(resume_text, job_description)

    # Gemini handles language tasks only
    suggestions = call_gemini(suggestions_prompt(resume_text, job_description, missing))
    questions   = call_gemini(interview_questions_prompt(job_role, missing))
    summary     = call_gemini(summary_prompt(resume_text, job_description))

    save_analysis(resume.filename, ats_score, {...})

    return {
        "ats_score": ats_score,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "suggestions": suggestions,
        "interview_questions": questions,
        "summary": summary
    }
```

---

### MERN Stack Developer — React Frontend

**Branch:** `frontend`
**Files:** `frontend/src/` (all React files)

**Important:** React runs on port 3000, FastAPI on port 8000. CORS is already configured in main.py so Axios calls will work.

**api.js — put ALL Axios calls here (not scattered in components):**
```javascript
import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

export const analyzeResume = async (resumeFile, jobDescription, jobRole) => {
  const formData = new FormData();
  formData.append('resume', resumeFile);
  formData.append('job_description', jobDescription);
  formData.append('job_role', jobRole);
  return await axios.post(`${BASE_URL}/analyze`, formData);
};

export const getHistory = async () => {
  return await axios.get(`${BASE_URL}/history`);
};

export const submitMockAnswer = async (question, answer, jobRole) => {
  const formData = new FormData();
  formData.append('question', question);
  formData.append('user_answer', answer);
  formData.append('job_role', jobRole);
  return await axios.post(`${BASE_URL}/mock-answer`, formData);
};

export const completeMockSession = async (jobRole, sessionData) => {
  const formData = new FormData();
  formData.append('job_role', jobRole);
  formData.append('session_data', JSON.stringify(sessionData));
  return await axios.post(`${BASE_URL}/mock-session-complete`, formData);
};
```

**4 Pages to Build:**

**Page 1 — UploadPage.jsx:**
- File input for PDF upload
- Text input for job role
- Textarea for job description
- Analyze button → calls analyzeResume() → stores result in state
- Navigate to /results after response

**Page 2 — ResultsPage.jsx:**
- ATS Score displayed as circular progress or large number
- Green badges for matched keywords
- Red badges for missing keywords
- Suggestions as a bullet list
- Button to start mock interview → navigate to /mock

**Page 3 — MockTestPage.jsx:**
- Show one question at a time
- Textarea for answer
- Submit → calls submitMockAnswer() → show score + feedback
- Next button → next question
- After question 7 → calls completeMockSession() → show final scorecard

**Page 4 — HistoryPage.jsx:**
- Calls getHistory() on mount
- Table showing: resume name, ATS score, date, verdict
- Line chart of ATS scores over time (use any chart library)

**Priority order (build in this order):**
```
1st → UploadPage + ResultsPage  ← most important, get this working first
2nd → HistoryPage               ← uses existing /history endpoint
3rd → MockTestPage              ← build this last, most complex state
```

---

### Docker/DevOps Guy — Database + Testing + Git + Deployment

**Branch:** `testing`
**Files:** `tests/test_api.py`, `.env.example`

**SQLite — work with Ansh on database.py:**
- Design both tables (analyses + mock_sessions)
- Make sure init_db() runs on server startup
- Test inserts and selects manually

**test_api.py — test all 7 endpoints:**
```python
import requests, json

BASE = "http://localhost:8000"

def test_health():
    r = requests.get(f"{BASE}/")
    assert r.status_code == 200
    print("✅ Health check passed")

def test_analyze():
    with open("test_resume.pdf", "rb") as f:
        r = requests.post(f"{BASE}/analyze",
            files={"resume": f},
            data={"job_description": "Python FastAPI developer needed", "job_role": "Backend Dev"}
        )
    assert r.status_code == 200
    assert "ats_score" in r.json()["analysis"]
    print("✅ Analyze endpoint passed")

def test_history():
    r = requests.get(f"{BASE}/history")
    assert r.status_code == 200
    print("✅ History endpoint passed")

def test_mock_answer():
    r = requests.post(f"{BASE}/mock-answer",
        data={"question": "What is FastAPI?",
              "user_answer": "FastAPI is a Python web framework",
              "job_role": "Backend Developer"}
    )
    assert r.status_code == 200
    assert "evaluation" in r.json()
    print("✅ Mock answer endpoint passed")

if __name__ == "__main__":
    test_health()
    test_analyze()
    test_history()
    test_mock_answer()
    print("\n✅ All tests passed!")
```

**Render.com Deployment (backend):**
```
1. Push code to GitHub
2. Go to render.com → New Web Service
3. Connect GitHub repo
4. Root directory: backend
5. Build command: pip install -r requirements.txt
6. Start command: uvicorn main:app --host 0.0.0.0 --port 8000
7. Add environment variable: GEMINI_API_KEY = your_actual_key
8. Deploy → get URL like: https://ats-backend-xxxx.onrender.com
9. Give this URL to MERN guy → he replaces localhost:8000 in api.js
```

**Git Management:**
- Ensure everyone pushes to their own branch
- Nobody touches main directly
- Ping Ansh when a branch is ready to merge

---

### NLP/ML Guy — NLP Engine + Gemini Prompts

**Branch:** `ml-core`
**Files:** `backend/ml_utils.py`, `backend/prompts.py`

**CRITICAL RULE:** Do NOT change these function signatures.
Ansh's main.py imports them directly. Names and return types must match exactly.

**ml_utils.py — your 4 functions:**
```python
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

nlp = spacy.load("en_core_web_sm")

def extract_keywords(text: str) -> list:
    """
    Extract skill/tech keywords from text using spaCy.
    Returns list of strings.
    """
    doc = nlp(text.lower())
    keywords = []
    # Your logic: noun chunks, named entities, skill matching
    return list(set(keywords))   # no duplicates

def calculate_ats_score(resume_text: str, jd_text: str) -> int:
    """
    Calculate ATS score using TF-IDF cosine similarity.
    Returns integer between 0 and 100.
    """
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return int(score * 100)

def find_matched_keywords(resume_text: str, jd_text: str) -> list:
    """
    Find keywords present in both resume and JD.
    Returns list of strings.
    """
    resume_kw = set(extract_keywords(resume_text))
    jd_kw     = set(extract_keywords(jd_text))
    return list(resume_kw & jd_kw)

def find_missing_keywords(resume_text: str, jd_text: str) -> list:
    """
    Find keywords in JD but missing from resume.
    Returns list of strings.
    """
    resume_kw = set(extract_keywords(resume_text))
    jd_kw     = set(extract_keywords(jd_text))
    return list(jd_kw - resume_kw)
```

**Test your functions before handing to Ansh:**
```python
if __name__ == "__main__":
    resume = "Experienced Python developer with FastAPI and SQL skills. Built REST APIs."
    jd = "Looking for Python developer with FastAPI, Docker, PostgreSQL, and REST API experience."

    print("Score:", calculate_ats_score(resume, jd))          # expect ~60-75
    print("Matched:", find_matched_keywords(resume, jd))      # ["Python", "FastAPI", "REST API"]
    print("Missing:", find_missing_keywords(resume, jd))      # ["Docker", "PostgreSQL"]
```

**prompts.py — 3 prompts to own and improve:**
```python
def suggestions_prompt(resume_text: str, jd_text: str, missing_keywords: list) -> str:
    """Gemini gives 3-5 specific resume improvement tips"""
    return f"""..."""

def interview_questions_prompt(job_role: str, missing_skills: list) -> str:
    """Gemini generates exactly 7 interview questions"""
    return f"""..."""

def mock_eval_prompt(question: str, user_answer: str, job_role: str) -> str:
    """Gemini evaluates answer and returns score + feedback"""
    return f"""..."""
```

**Hand ml_utils.py to Ansh by Day 6.**
**Hand improved prompts.py to Ansh by Day 8.**

---

### UI/UX Guy — Content + Documentation + Demo

**Branch:** `docs`
**Files:** `data/skills_data.csv`, `README.md`

**skills_data.csv:**
```csv
skill,category,level
Python,Programming,Core
JavaScript,Programming,Core
FastAPI,Backend,Core
React,Frontend,Core
Docker,DevOps,Core
PostgreSQL,Database,Core
...
```
Build 200+ skills. Use ChatGPT or Claude to generate bulk of this list.
Categories: Programming, Backend, Frontend, Database, AI/ML, DevOps, Cloud, Tools, Testing

**README.md must include:**
- Project title + description
- Team members and roles
- Tech stack table
- Backend setup instructions
- Frontend setup instructions
- All 7 API endpoints with examples
- Screenshots (add after Day 10 when UI is ready)

**Demo Video script (3-5 minutes):**
```
0:00 - "Hi, we're Team [name]. Students struggle with resume alignment..."
0:30 - Show React home page
1:00 - Upload a real resume PDF + paste a real job description
1:30 - Show ATS score, green matched badges, red missing badges
2:00 - Show AI suggestions
2:30 - Click Start Mock Interview
2:45 - Answer 2 questions live, show score + feedback
3:30 - Show final scorecard
3:45 - Show progress tracking / history page
4:15 - "Built with FastAPI, NLP, Gemini AI, and React"
4:30 - Wrap up
```

**PPT Slides (7 slides):**
1. Cover — Project name, team name, program name
2. Problem — Why this matters (students, fake jobs, bad resumes)
3. Our Solution — What we built
4. Tech Stack — Architecture diagram (copy flow diagram from this doc)
5. Key Features — Screenshots from the React app
6. Team & Roles — Who did what
7. Thank You + GitHub link + deployment link

---

## 9. 15-Day Timeline

| Date | Day | Ansh | MERN Guy | Docker Guy | NLP Guy | UI/UX Guy |
|---|---|---|---|---|---|---|
| 14 June | Day 1 | Create GitHub repo, share planning.md | Setup React project, study API endpoints | Setup env, create branches for everyone | Study current prompts in main.py | Start skills_data.csv |
| 15 June | Day 2 | FastAPI running, CORS configured, health check live | Build UploadPage.jsx UI (no API yet) | Write SQLite schema, work on database.py | Start ml_utils.py — extract_keywords() | Continue skills_data.csv (100 skills) |
| 16 June | Day 3 | PDF parsing working with pdfplumber | Connect UploadPage to /analyze endpoint | Write test cases for health + history | calculate_ats_score() function done | Finish skills_data.csv (200+ skills) |
| 17 June | Day 4 | Gemini API integrated, /analyze returning data | Build ResultsPage.jsx — score + badges | Write test for /analyze endpoint | find_matched + find_missing done | Start README draft |
| 18 June | Day 5 | Import ml_utils, NLP scoring in /analyze | UploadPage → ResultsPage flow working | All 7 test cases written | Test ml_utils with 5 real resumes | README setup instructions done |
| 19 June | Day 6 | All 7 endpoints complete, tested via /docs | Build HistoryPage.jsx | Run all tests, report bugs to Ansh | **Hand ml_utils.py to Ansh** | README API section done |
| 20 June | Day 7 | **CHECKPOINT — Everyone shows one working thing** | **CHECKPOINT** | **CHECKPOINT** | **CHECKPOINT** | **CHECKPOINT** |
| 21 June | Day 8 | Fix integration bugs with MERN guy | Build MockTestPage.jsx — question flow | Deploy backend on Render.com | Improve ATS prompt quality | Collect screenshots for README |
| 22 June | Day 9 | Final endpoint testing + bug fixes | Mock test evaluation + feedback display | Share live Render URL with team | Improve mock eval prompt | Record demo video |
| 23 June | Day 10 | Help MERN guy with any API issues | Final score display + progress chart | Final testing on live deployment | **Hand improved prompts.py to Ansh** | Edit demo video |
| 24 June | Day 11 | Full integration test — all pages working | UI polish — colors, layout, UX | Final test run on complete project | Documentation help | Make PPT presentation |
| 25 June | Day 12 | Fix any remaining bugs | Final UI polish | Git cleanup — merge all branches | Review final output quality | Finalize PPT |
| 26 June | Day 13 | Code review + README final check | Final React build | Prepare submission ZIP | Final review | Final PPT + submission ZIP |
| 27 June | Day 14 | **TARGET: Submit today** | Final check | Submit ZIP via Google Form | Done | Submit |
| 28 June | Day 15 | **HARD DEADLINE** | Emergency fixes only | Emergency only | Done | Done |

---

## 10. Feature Coverage Checklist

| Feature from Problem Statement | Status | Who |
|---|---|---|
| Resume PDF upload | ✅ Complete | Ansh (pdfplumber) |
| ATS compatibility score with detailed breakdown | ✅ Complete | NLP Guy (cosine similarity) + Ansh |
| Missing keywords and skills gap analysis | ✅ Complete | NLP Guy (set operations) + Ansh |
| AI-powered resume improvement suggestions | ✅ Complete | NLP Guy (prompts) + Gemini API |
| Role-based interview question generation | ✅ Complete | NLP Guy (prompts) + Gemini API |
| Mock interview Q&A practice (text) | ✅ Complete | Ansh (backend) + MERN Guy (UI) |
| Progress tracking across multiple applications | ✅ Complete | Ansh (SQLite /history) + MERN Guy (UI) |
| Voice mock interview | ❌ Officially skipped | Too complex for 15 days. Text is sufficient. |

---

## 11. CORS — How React Talks to FastAPI

This is the most common issue in MERN + FastAPI projects.

**What is CORS?**
React runs on `localhost:3000`. FastAPI runs on `localhost:8000`.
Browser blocks requests between different ports by default.
CORS middleware in FastAPI tells the browser "it's okay, allow this."

**Already handled in main.py:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**After deployment — MERN guy updates api.js:**
```javascript
// During development
const BASE_URL = 'http://localhost:8000';

// After Docker guy shares Render URL → change to:
const BASE_URL = 'https://ats-backend-xxxx.onrender.com';
```

**And Ansh updates CORS in main.py:**
```python
allow_origins=["http://localhost:3000", "https://your-react-app.vercel.app"]
```

---

## 12. Git Workflow

### Repository Setup (Ansh — Day 1)
```bash
git init
git add .
git commit -m "initial commit — project structure + planning.md"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ats-resume-analyzer.git
git push -u origin main
```

### Add Teammates as Collaborators
```
GitHub → Settings → Collaborators → Add each member's GitHub username
```

### Each Member Creates Their Branch (Day 1)
```bash
# MERN Guy
git checkout -b frontend

# NLP Guy
git checkout -b ml-core

# Docker Guy
git checkout -b testing

# UI/UX Guy
git checkout -b docs
```

### Daily Commands for Everyone
```bash
git pull origin main          # get latest every morning
git add .
git commit -m "what you built"
git push origin your-branch
```

### Merging — Only Ansh Does This
```bash
git checkout main
git pull origin main
git merge ml-core      # NLP guy's files
git merge frontend     # MERN guy's files
git merge testing      # Docker guy's files
git merge docs         # UI/UX guy's files
git push origin main
```

### Branch Ownership
| Branch | Owner | Files Owned |
|---|---|---|
| `main` | Ansh (merge only) | Final project |
| `backend` | Ansh | main.py, database.py, requirements.txt |
| `ml-core` | NLP Guy | ml_utils.py, prompts.py |
| `frontend` | MERN Guy | frontend/src/ (all React files) |
| `testing` | Docker Guy | tests/, .env.example |
| `docs` | UI/UX Guy | README.md, data/skills_data.csv |

---

## 13. Submission Requirements

| Deliverable | Who | Target Date |
|---|---|---|
| Project Source Code — GitHub repo link | Ansh | Day 13 |
| README / Documentation | UI/UX Guy | Day 13 |
| Presentation PPT/PDF | UI/UX Guy | Day 13 |
| Demo Video (Mandatory, 3-5 mins) | UI/UX Guy | Day 12 |
| Deployment Link (backend on Render) | Docker Guy | Day 8 |
| ZIP file with all deliverables | UI/UX Guy | Day 14 |

**Submit via:** Official Google Form only
**Submission opens:** Day 8 (21 June) — based on original schedule
**Hard deadline:** 28 June 2026 (Day 15) — strictly enforced
**Target: submit on Day 14 (27 June). Day 15 is emergency only.**

---

## 14. Team Rules

1. **Nobody pushes directly to main.** Always your own branch.

2. **Daily WhatsApp update (mandatory every evening):**
   ```
   ✅ Done today:
   🔨 Working on next:
   ❌ Blocked on:
   ```

3. **Blocked more than 1 day? Tell Ansh immediately.** Silence = project risk.

4. **Day 7 (20 June) checkpoint is non-negotiable.** Everyone shows something working.

5. **NLP Guy deadline: ml_utils.py to Ansh by Day 6 (19 June).** This blocks the backend.

6. **MERN Guy deadline: UploadPage + ResultsPage working by Day 5 (18 June).** So integration can start.

7. **Docker Guy deadline: Render.com deployment live by Day 8 (21 June).** Team needs live URL.

8. **Voice mock interview is dropped.** Text mock interview is complete and sufficient for full marks.

9. **Gemini API key only in .env file.** Never hardcode. Never commit to GitHub.

10. **MERN guy — when switching from localhost to Render URL, update api.js AND tell Ansh to update CORS.**

11. **Submit on Day 14, not Day 15.** Day 15 exists for emergencies only.

12. **One person reviews every merge to main.** That person is Ansh.

---

*Document prepared by Ansh Chaturvedi — Team Leader*
*NextGen Data Minds Summer Project Program 2026*
*Last updated: 14 June 2026*
