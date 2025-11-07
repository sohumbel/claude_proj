"""Configuration file for Resume Roaster."""

# Buzzword library
BUZZWORDS = [
    "results-oriented",
    "team player",
    "hard worker",
    "detail-oriented",
    "excellent communication skills",
    "go-getter",
    "think outside the box",
    "synergy",
    "leverage",
    "paradigm shift",
    "strategic thinker",
    "self-starter",
    "proactive",
    "dynamic",
    "innovative",
    "passionate",
    "motivated",
    "dedicated",
    "driven",
    "fast-paced environment",
    "wear many hats",
    "hit the ground running",
    "work well under pressure",
    "team-oriented",
    "people person",
    "out-of-the-box thinker",
    "customer-focused",
    "best practices",
    "value-add",
    "action-oriented"
]

# Weak verbs
WEAK_VERBS = [
    "responsible for",
    "worked on",
    "helped with",
    "assisted in",
    "involved in",
    "participated in",
    "contributed to",
    "handled",
    "dealt with",
    "managed",
    "oversaw"
]

# Strong verb replacements
STRONG_VERBS = [
    "led", "built", "launched", "increased", "reduced",
    "improved", "designed", "implemented", "created", "developed",
    "achieved", "delivered", "generated", "orchestrated", "spearheaded",
    "transformed", "optimized", "streamlined", "pioneered", "established",
    "executed", "drove", "accelerated", "scaled", "engineered",
    "architected", "deployed", "automated", "exceeded", "surpassed"
]

# ATS-unfriendly elements
ATS_KILLERS = [
    "tables", "text boxes", "headers",
    "footers", "columns", "images",
    "graphics", "charts", "special characters"
]

# Scoring weights
WEIGHTS = {
    "content": 0.35,
    "formatting": 0.25,
    "ats_compatibility": 0.25,
    "impact": 0.15
}

# Roast tone templates
ROAST_TONES = {
    "gentle": "encouraging and supportive with light humor",
    "medium": "direct and witty with constructive criticism",
    "savage": "brutally honest and hilarious like Gordon Ramsay"
}

# Maximum resume lengths (in pages)
MAX_RESUME_LENGTH = {
    "entry_level": 1,  # 0-3 years experience
    "mid_level": 1,    # 3-10 years experience
    "senior_level": 2  # 10+ years experience
}

# Standard section headers for ATS
STANDARD_SECTIONS = [
    "summary", "objective", "experience", "work experience",
    "education", "skills", "certifications", "projects"
]

# Contact info regex patterns
EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
PHONE_PATTERN = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
LINKEDIN_PATTERN = r'linkedin\.com/in/[\w-]+'

# Unprofessional email domains to flag
UNPROFESSIONAL_DOMAINS = [
    "hotmail.com", "yahoo.com", "aol.com", "live.com",
    "rocketmail.com", "aim.com", "ymail.com"
]

# Severity levels
SEVERITY = {
    "critical": 3,
    "high": 2,
    "medium": 1,
    "low": 0
}
