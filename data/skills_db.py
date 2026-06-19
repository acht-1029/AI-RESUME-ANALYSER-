"""
Skills Database
===============
Multi-domain curated skills list (400+) for matching against resumes and JDs.
Covers: Tech, Business, Finance, Healthcare, Marketing/Creative, Legal/Education.
Grouped by category for maintainability; flattened into SKILLS_DB at import time.
"""

# ===========================================================================
#  TECHNOLOGY SKILLS
# ===========================================================================

_PROGRAMMING_LANGUAGES = [
    "Python", "Java", "JavaScript", "TypeScript", "C", "C++", "C#", "Go",
    "Rust", "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R", "MATLAB",
    "Perl", "Lua", "Dart", "Shell", "Bash", "PowerShell", "SQL", "Haskell",
    "Elixir", "Clojure", "Julia", "Groovy", "Objective-C",
]

_WEB_FRONTEND = [
    "HTML", "CSS", "React", "React.js", "Angular", "Vue", "Vue.js", "Svelte",
    "Next.js", "Nuxt.js", "jQuery", "Bootstrap", "Tailwind CSS", "SASS",
    "LESS", "Webpack", "Vite", "Redux", "Material UI", "Chakra UI",
    "Styled Components", "GraphQL", "REST API", "WebSocket",
]

_WEB_BACKEND = [
    "Node.js", "Express", "Express.js", "Django", "Flask", "FastAPI",
    "Spring", "Spring Boot", "ASP.NET", ".NET", "Ruby on Rails", "Laravel",
    "NestJS", "Gin", "Fiber", "Actix", "Koa", "Hapi",
]

_DATABASES = [
    "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Redis", "Cassandra",
    "DynamoDB", "Elasticsearch", "Neo4j", "CouchDB", "MariaDB", "Oracle",
    "SQL Server", "Firebase", "Firestore", "Supabase", "InfluxDB",
]

_CLOUD_DEVOPS = [
    "AWS", "Amazon Web Services", "Azure", "Google Cloud", "GCP", "Docker",
    "Kubernetes", "Terraform", "Ansible", "Jenkins", "GitHub Actions",
    "GitLab CI", "CircleCI", "Travis CI", "Nginx", "Apache", "Linux",
    "CI/CD", "Heroku", "Vercel", "Netlify", "CloudFormation", "Pulumi",
    "Helm", "ArgoCD", "Prometheus", "Grafana", "Datadog", "New Relic",
    "ELK Stack", "Vagrant",
]

_DATA_SCIENCE_ML = [
    "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Keras",
    "scikit-learn", "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn",
    "Jupyter", "Notebook", "NLP", "Natural Language Processing",
    "Computer Vision", "OpenCV", "NLTK", "spaCy", "Hugging Face",
    "Transformers", "LLM", "Large Language Models", "GPT", "BERT",
    "Generative AI", "GenAI", "Prompt Engineering", "LangChain",
    "RAG", "Retrieval Augmented Generation", "Fine-tuning",
    "XGBoost", "LightGBM", "Random Forest", "Neural Networks",
    "Reinforcement Learning", "MLOps", "MLflow", "Kubeflow",
    "Feature Engineering", "Data Preprocessing", "Data Cleaning",
    "Exploratory Data Analysis", "EDA", "Statistical Analysis",
]

_DATA_ENGINEERING = [
    "ETL", "Data Pipeline", "Apache Spark", "PySpark", "Hadoop",
    "Apache Kafka", "Airflow", "Apache Beam", "Databricks", "Snowflake",
    "BigQuery", "Redshift", "Data Warehouse", "Data Lake", "dbt",
    "Apache Flink", "Hive", "Presto", "Data Modeling",
]

_MOBILE = [
    "Android", "iOS", "React Native", "Flutter", "SwiftUI", "Jetpack Compose",
    "Xamarin", "Ionic", "Cordova",
]

_TOOLS_PRACTICES = [
    "Git", "GitHub", "GitLab", "Bitbucket", "Jira", "Confluence",
    "Agile", "Scrum", "Kanban", "TDD", "Test Driven Development",
    "BDD", "Unit Testing", "Integration Testing", "Selenium", "Cypress",
    "Jest", "Pytest", "Postman", "Swagger", "OpenAPI",
    "Figma", "Adobe XD", "Microservices", "Monolith", "Event Driven",
    "Message Queue", "RabbitMQ", "gRPC", "Protocol Buffers",
    "Design Patterns", "SOLID", "OOP", "Functional Programming",
    "System Design", "API Design", "Technical Writing",
]

_SECURITY = [
    "Cybersecurity", "OWASP", "Penetration Testing", "Encryption",
    "OAuth", "JWT", "SSO", "SAML", "RBAC", "IAM",
]

# ===========================================================================
#  BUSINESS & MANAGEMENT SKILLS
# ===========================================================================

_BUSINESS_MANAGEMENT = [
    "Strategic Planning", "Business Development", "Business Analysis",
    "Operations Management", "Supply Chain Management", "Logistics",
    "Procurement", "Vendor Management", "Stakeholder Management",
    "Change Management", "Risk Management", "Quality Assurance",
    "Process Improvement", "Six Sigma", "Lean Management", "Lean Six Sigma",
    "KPI", "Key Performance Indicators", "OKR", "Business Intelligence",
    "CRM", "Salesforce", "HubSpot", "SAP", "ERP",
    "Product Management", "Product Strategy", "Roadmap Planning",
    "Market Research", "Competitive Analysis", "SWOT Analysis",
    "P&L Management", "Budget Management", "Revenue Growth",
    "Client Relations", "Account Management", "Negotiation",
    "Consulting", "Management Consulting", "Strategy Consulting",
]

_HUMAN_RESOURCES = [
    "Talent Acquisition", "Recruitment", "Onboarding", "Employee Relations",
    "Performance Management", "Compensation and Benefits", "HRIS",
    "Workday", "ADP", "BambooHR", "Payroll", "Labor Law",
    "Diversity and Inclusion", "Employee Engagement", "Training and Development",
    "Organizational Development", "Succession Planning", "HR Analytics",
]

# ===========================================================================
#  FINANCE & ACCOUNTING SKILLS
# ===========================================================================

_FINANCE_ACCOUNTING = [
    "Financial Analysis", "Financial Modeling", "Financial Reporting",
    "Budgeting", "Forecasting", "Variance Analysis",
    "Accounting", "GAAP", "IFRS", "Bookkeeping", "Accounts Payable",
    "Accounts Receivable", "General Ledger", "Journal Entries",
    "Tax Preparation", "Tax Planning", "Auditing", "Internal Audit",
    "Cost Accounting", "Management Accounting", "Forensic Accounting",
    "Investment Banking", "Equity Research", "Portfolio Management",
    "Risk Assessment", "Credit Analysis", "Due Diligence",
    "Mergers and Acquisitions", "M&A", "Valuation", "DCF",
    "Bloomberg Terminal", "Capital Markets", "Fixed Income", "Derivatives",
    "QuickBooks", "Tally", "Xero", "SAP FICO", "Excel",
    "Advanced Excel", "Pivot Tables", "VLOOKUP", "VBA", "Macros",
    "Financial Planning", "Wealth Management", "Insurance",
    "Mutual Funds", "Stocks", "Bonds", "Cryptocurrency",
    "Compliance", "Regulatory Compliance", "SOX Compliance", "KYC", "AML",
]

# ===========================================================================
#  HEALTHCARE & LIFE SCIENCES SKILLS
# ===========================================================================

_HEALTHCARE = [
    "Patient Care", "Clinical Research", "Clinical Trials",
    "Electronic Health Records", "EHR", "EMR", "Epic", "Cerner",
    "Medical Terminology", "HIPAA", "Healthcare Compliance",
    "Pharmacology", "Drug Development", "FDA Regulations",
    "Medical Coding", "ICD-10", "CPT Coding", "Medical Billing",
    "Nursing", "Patient Assessment", "Vital Signs", "Triage",
    "Phlebotomy", "Laboratory Skills", "Microscopy",
    "Public Health", "Epidemiology", "Biostatistics",
    "Health Informatics", "Telemedicine", "Healthcare Administration",
    "Mental Health", "Counseling", "Psychology",
    "Nutrition", "Dietetics", "Physical Therapy", "Rehabilitation",
    "Biotechnology", "Genomics", "Bioinformatics", "Molecular Biology",
    "GMP", "Good Manufacturing Practices", "Quality Control",
    "Medical Devices", "Regulatory Affairs", "Clinical Documentation",
]

# ===========================================================================
#  MARKETING, CREATIVE & DESIGN SKILLS
# ===========================================================================

_MARKETING = [
    "Digital Marketing", "Content Marketing", "Content Strategy",
    "SEO", "Search Engine Optimization", "SEM", "Search Engine Marketing",
    "Google Ads", "Google Analytics", "GA4", "Facebook Ads", "Meta Ads",
    "PPC", "Pay Per Click", "Social Media Marketing", "Social Media Management",
    "Email Marketing", "Mailchimp", "Marketing Automation",
    "Inbound Marketing", "Outbound Marketing", "Lead Generation",
    "Conversion Rate Optimization", "CRO", "A/B Testing",
    "Brand Management", "Brand Strategy", "Public Relations", "PR",
    "Copywriting", "Content Writing", "Blog Writing", "Technical Writing",
    "Marketing Analytics", "Campaign Management", "Influencer Marketing",
    "Affiliate Marketing", "Video Marketing", "YouTube Marketing",
    "TikTok Marketing", "Instagram Marketing", "LinkedIn Marketing",
    "Hootsuite", "Buffer", "Sprout Social", "Canva",
]

_DESIGN_CREATIVE = [
    "Graphic Design", "UI Design", "UX Design", "UI/UX", "User Research",
    "Wireframing", "Prototyping", "Interaction Design", "Visual Design",
    "Adobe Photoshop", "Adobe Illustrator", "Adobe InDesign",
    "Adobe Premiere Pro", "Adobe After Effects", "Adobe Creative Suite",
    "Sketch", "InVision", "Zeplin",
    "Typography", "Color Theory", "Layout Design", "Branding",
    "Motion Graphics", "Video Editing", "Animation", "3D Modeling",
    "Blender", "Maya", "Cinema 4D", "AutoCAD", "SolidWorks",
    "Photography", "Photo Editing", "Lightroom",
    "Responsive Design", "Accessibility", "WCAG",
    "Design Thinking", "User Persona", "Journey Mapping",
    "Usability Testing", "Information Architecture",
]

# ===========================================================================
#  LEGAL & EDUCATION SKILLS
# ===========================================================================

_LEGAL = [
    "Legal Research", "Legal Writing", "Contract Law", "Contract Drafting",
    "Contract Review", "Intellectual Property", "Patent Law", "Trademark",
    "Copyright", "Corporate Law", "Civil Litigation", "Criminal Law",
    "Employment Law", "Real Estate Law", "Immigration Law",
    "Regulatory Compliance", "Legal Compliance", "Due Diligence",
    "Case Management", "Legal Documentation", "LexisNexis", "Westlaw",
    "Mergers and Acquisitions", "Arbitration", "Mediation",
    "Privacy Law", "GDPR", "Data Privacy",
]

_EDUCATION = [
    "Curriculum Development", "Lesson Planning", "Instructional Design",
    "E-Learning", "LMS", "Moodle", "Canvas", "Blackboard",
    "Classroom Management", "Student Assessment", "Differentiated Instruction",
    "Special Education", "Educational Technology", "EdTech",
    "Tutoring", "Academic Advising", "Research Methodology",
    "Grant Writing", "Academic Writing", "Peer Review",
    "STEM Education", "Online Teaching", "Blended Learning",
]

# ===========================================================================
#  CROSS-DOMAIN SOFT SKILLS
# ===========================================================================

_SOFT_SKILLS = [
    "Leadership", "Communication", "Problem Solving", "Teamwork",
    "Time Management", "Critical Thinking", "Project Management",
    "Mentoring", "Cross-functional Collaboration",
    "Presentation Skills", "Public Speaking", "Stakeholder Communication",
    "Conflict Resolution", "Decision Making", "Adaptability",
    "Emotional Intelligence", "Analytical Thinking", "Attention to Detail",
    "Customer Service", "Client Management", "Interpersonal Skills",
    "Creative Thinking", "Innovation", "Strategic Thinking",
    "Multitasking", "Prioritization", "Delegation",
    "Remote Work", "Virtual Collaboration", "Self-Motivation",
]

# ===========================================================================
#  Flattened master list — this is what skill_extractor imports
# ===========================================================================

SKILLS_DB: list[str] = sorted(set(
    _PROGRAMMING_LANGUAGES
    + _WEB_FRONTEND
    + _WEB_BACKEND
    + _DATABASES
    + _DATA_SCIENCE_ML
    + _DATA_ENGINEERING
    + _MOBILE
    + _CLOUD_DEVOPS
    + _TOOLS_PRACTICES
    + _SECURITY
    + _BUSINESS_MANAGEMENT
    + _HUMAN_RESOURCES
    + _FINANCE_ACCOUNTING
    + _HEALTHCARE
    + _MARKETING
    + _DESIGN_CREATIVE
    + _LEGAL
    + _EDUCATION
    + _SOFT_SKILLS
))

# Pre-build a lowercase lookup set for quick membership checks
SKILLS_DB_LOWER: set[str] = {s.lower() for s in SKILLS_DB}

# Category map — useful if frontend wants to group matched skills
SKILL_CATEGORIES: dict[str, list[str]] = {
    # Tech
    "Programming Languages": _PROGRAMMING_LANGUAGES,
    "Web Frontend": _WEB_FRONTEND,
    "Web Backend": _WEB_BACKEND,
    "Databases": _DATABASES,
    "Cloud & DevOps": _CLOUD_DEVOPS,
    "Data Science & ML": _DATA_SCIENCE_ML,
    "Data Engineering": _DATA_ENGINEERING,
    "Mobile": _MOBILE,
    "Tools & Practices": _TOOLS_PRACTICES,
    "Security": _SECURITY,
    # Business
    "Business & Management": _BUSINESS_MANAGEMENT,
    "Human Resources": _HUMAN_RESOURCES,
    # Finance
    "Finance & Accounting": _FINANCE_ACCOUNTING,
    # Healthcare
    "Healthcare & Life Sciences": _HEALTHCARE,
    # Marketing & Creative
    "Marketing": _MARKETING,
    "Design & Creative": _DESIGN_CREATIVE,
    # Legal & Education
    "Legal": _LEGAL,
    "Education": _EDUCATION,
    # Cross-domain
    "Soft Skills": _SOFT_SKILLS,
}


def get_category(skill: str) -> str:
    """Return the category a skill belongs to, or 'Other'."""
    skill_lower = skill.lower()
    for category, skills in SKILL_CATEGORIES.items():
        if skill_lower in {s.lower() for s in skills}:
            return category
    return "Other"
