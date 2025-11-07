"""Resume parsing module for extracting content from PDF and DOCX files."""

import re
import pdfplumber
import docx
from typing import Dict, List, Optional
from config import EMAIL_PATTERN, PHONE_PATTERN, LINKEDIN_PATTERN


def parse_resume(file_path: str) -> Dict:
    """
    Parse a resume file and extract structured information.

    Args:
        file_path: Path to the resume file (PDF or DOCX)

    Returns:
        Dictionary containing parsed resume data

    Raises:
        ValueError: If file format is not supported
        FileNotFoundError: If file does not exist
    """
    if file_path.lower().endswith('.pdf'):
        return parse_pdf(file_path)
    elif file_path.lower().endswith('.docx'):
        return parse_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a PDF or DOCX file.")


def parse_pdf(file_path: str) -> Dict:
    """Parse PDF resume and extract structured data."""
    text = ""
    page_count = 0

    try:
        with pdfplumber.open(file_path) as pdf:
            page_count = len(pdf.pages)
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        raise ValueError(f"Failed to parse PDF: {str(e)}")

    if not text.strip():
        raise ValueError("Resume appears to be empty or unreadable.")

    return extract_resume_data(text, page_count, 'pdf')


def parse_docx(file_path: str) -> Dict:
    """Parse DOCX resume and extract structured data."""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])

        # Estimate page count (rough estimate: 500 words per page)
        word_count = len(text.split())
        page_count = max(1, round(word_count / 500))

    except Exception as e:
        raise ValueError(f"Failed to parse DOCX: {str(e)}")

    if not text.strip():
        raise ValueError("Resume appears to be empty or unreadable.")

    return extract_resume_data(text, page_count, 'docx')


def extract_resume_data(text: str, page_count: int, file_type: str) -> Dict:
    """Extract structured data from resume text."""

    return {
        "raw_text": text,
        "contact": extract_contact_info(text),
        "summary": extract_summary(text),
        "experience": extract_experience(text),
        "education": extract_education(text),
        "skills": extract_skills(text),
        "formatting": {
            "page_count": page_count,
            "file_type": file_type,
            "has_links": bool(re.search(LINKEDIN_PATTERN, text, re.IGNORECASE)),
            "character_count": len(text),
            "word_count": len(text.split())
        }
    }


def extract_contact_info(text: str) -> Dict:
    """Extract contact information from resume text."""
    # Take first 500 characters as contact section is usually at top
    header_section = text[:500]

    email_match = re.search(EMAIL_PATTERN, header_section)
    phone_match = re.search(PHONE_PATTERN, header_section)
    linkedin_match = re.search(LINKEDIN_PATTERN, header_section, re.IGNORECASE)

    # Extract name (assume it's the first non-empty line)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    name = lines[0] if lines else ""

    return {
        "name": name,
        "email": email_match.group(0) if email_match else None,
        "phone": phone_match.group(0) if phone_match else None,
        "linkedin": linkedin_match.group(0) if linkedin_match else None
    }


def extract_summary(text: str) -> Optional[str]:
    """Extract professional summary or objective."""
    summary_patterns = [
        r'(?:SUMMARY|PROFESSIONAL SUMMARY|OBJECTIVE|PROFILE)(.*?)(?=\n\n|\n[A-Z]{2,})',
        r'(?:Summary|Professional Summary|Objective|Profile)(.*?)(?=\n\n|\n[A-Z]{2,})',
    ]

    for pattern in summary_patterns:
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            summary = match.group(1).strip()
            if len(summary) > 20:  # Ensure it's substantial
                return summary

    return None


def extract_experience(text: str) -> List[Dict]:
    """Extract work experience entries."""
    experience_entries = []

    # Find experience section
    exp_pattern = r'(?:EXPERIENCE|WORK EXPERIENCE|EMPLOYMENT)(.*?)(?=\n(?:EDUCATION|SKILLS|CERTIFICATIONS|$))'
    exp_match = re.search(exp_pattern, text, re.DOTALL | re.IGNORECASE)

    if not exp_match:
        return experience_entries

    exp_section = exp_match.group(1)

    # Split into individual job entries (look for date patterns)
    date_pattern = r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December|\d{4})'

    # Split by lines and group entries
    lines = exp_section.split('\n')
    current_entry = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if this line contains a date (likely a job header)
        if re.search(date_pattern, line, re.IGNORECASE):
            if current_entry:
                experience_entries.append(current_entry)

            current_entry = {
                "title": "",
                "company": "",
                "dates": line,
                "bullets": []
            }
        elif current_entry:
            # Check if it's a bullet point
            if line.startswith(('•', '-', '*', '·')) or re.match(r'^\d+\.', line):
                bullet = re.sub(r'^[•\-*·]\s*|\d+\.\s*', '', line)
                current_entry["bullets"].append(bullet)
            elif not current_entry["title"]:
                current_entry["title"] = line
            elif not current_entry["company"]:
                current_entry["company"] = line

    # Add last entry
    if current_entry:
        experience_entries.append(current_entry)

    return experience_entries


def extract_education(text: str) -> List[Dict]:
    """Extract education entries."""
    education_entries = []

    # Find education section
    edu_pattern = r'(?:EDUCATION)(.*?)(?=\n(?:EXPERIENCE|SKILLS|CERTIFICATIONS|$))'
    edu_match = re.search(edu_pattern, text, re.DOTALL | re.IGNORECASE)

    if not edu_match:
        return education_entries

    edu_section = edu_match.group(1)

    # Look for degree patterns
    degree_patterns = [
        r'(?:Bachelor|Master|PhD|Ph\.D|B\.S\.|M\.S\.|B\.A\.|M\.A\.|Associate)',
        r'(?:BS|MS|BA|MA|MBA|PhD)'
    ]

    lines = edu_section.split('\n')
    current_entry = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if line contains degree pattern
        has_degree = any(re.search(pattern, line, re.IGNORECASE) for pattern in degree_patterns)

        if has_degree:
            if current_entry:
                education_entries.append(current_entry)

            current_entry = {
                "degree": line,
                "school": "",
                "dates": "",
                "gpa": None
            }
        elif current_entry:
            # Look for GPA
            gpa_match = re.search(r'GPA:?\s*(\d+\.?\d*)', line, re.IGNORECASE)
            if gpa_match:
                current_entry["gpa"] = gpa_match.group(1)
            elif not current_entry["school"]:
                current_entry["school"] = line
            elif not current_entry["dates"]:
                current_entry["dates"] = line

    if current_entry:
        education_entries.append(current_entry)

    return education_entries


def extract_skills(text: str) -> List[str]:
    """Extract skills list."""
    skills = []

    # Find skills section
    skills_pattern = r'(?:SKILLS|TECHNICAL SKILLS|CORE COMPETENCIES)(.*?)(?=\n\n|\n[A-Z]{2,}|$)'
    skills_match = re.search(skills_pattern, text, re.DOTALL | re.IGNORECASE)

    if not skills_match:
        return skills

    skills_section = skills_match.group(1)

    # Split by common delimiters
    skill_list = re.split(r'[,;|•·\n]', skills_section)

    for skill in skill_list:
        skill = skill.strip()
        if skill and len(skill) > 1:
            skills.append(skill)

    return skills
