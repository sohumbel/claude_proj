"""Resume analysis module for identifying issues and scoring."""

import re
from typing import Dict, List
from config import (
    BUZZWORDS, WEAK_VERBS, STRONG_VERBS, ATS_KILLERS,
    WEIGHTS, UNPROFESSIONAL_DOMAINS, SEVERITY, STANDARD_SECTIONS
)


def analyze_resume(parsed_data: Dict) -> Dict:
    """
    Analyze parsed resume data and identify issues.

    Args:
        parsed_data: Dictionary containing parsed resume data

    Returns:
        Dictionary containing analysis results with scores and issues
    """
    issues = []
    strengths = []

    # Analyze different aspects
    content_issues = analyze_content(parsed_data)
    formatting_issues = analyze_formatting(parsed_data)
    ats_issues = analyze_ats_compatibility(parsed_data)
    impact_analysis = analyze_impact(parsed_data)

    issues.extend(content_issues)
    issues.extend(formatting_issues)
    issues.extend(ats_issues)

    # Calculate scores
    content_score = calculate_content_score(content_issues, parsed_data)
    formatting_score = calculate_formatting_score(formatting_issues, parsed_data)
    ats_score = calculate_ats_score(ats_issues)
    impact_score = calculate_impact_score(impact_analysis)

    # Calculate overall score
    overall_score = (
        content_score * WEIGHTS["content"] +
        formatting_score * WEIGHTS["formatting"] +
        ats_score * WEIGHTS["ats_compatibility"] +
        impact_score * WEIGHTS["impact"]
    )

    # Identify strengths
    strengths = identify_strengths(parsed_data, issues)

    # Get critical fixes (top 3 most important)
    critical_fixes = get_critical_fixes(issues)

    return {
        "scores": {
            "overall": round(overall_score),
            "content": round(content_score),
            "formatting": round(formatting_score),
            "ats_compatibility": round(ats_score),
            "impact": round(impact_score)
        },
        "issues": issues,
        "strengths": strengths,
        "critical_fixes": critical_fixes,
        "impact_analysis": impact_analysis
    }


def analyze_content(parsed_data: Dict) -> List[Dict]:
    """Analyze resume content for buzzwords, weak verbs, and other issues."""
    issues = []
    text = parsed_data.get("raw_text", "")

    # Check for buzzwords
    for buzzword in BUZZWORDS:
        if buzzword.lower() in text.lower():
            issues.append({
                "category": "buzzwords",
                "severity": "medium",
                "location": "content",
                "problem": f"Overused phrase: '{buzzword}'",
                "fix": "Replace with specific, quantifiable achievement"
            })

    # Check for weak verbs in experience bullets
    experience = parsed_data.get("experience", [])
    for exp in experience:
        for bullet in exp.get("bullets", []):
            for weak_verb in WEAK_VERBS:
                if weak_verb.lower() in bullet.lower():
                    issues.append({
                        "category": "weak_verbs",
                        "severity": "high",
                        "location": "experience",
                        "problem": f"Weak phrase: '{weak_verb}' in bullet point",
                        "fix": f"Use strong action verb like: {', '.join(STRONG_VERBS[:3])}"
                    })
                    break  # Only flag once per bullet

    # Check for lack of quantification
    for exp in experience:
        for bullet in exp.get("bullets", []):
            # Look for numbers, percentages, dollar signs
            has_metrics = bool(re.search(r'\d+[%$]?|\$\d+', bullet))
            if not has_metrics and len(bullet) > 20:
                issues.append({
                    "category": "quantification",
                    "severity": "high",
                    "location": "experience",
                    "problem": "Bullet point lacks metrics",
                    "fix": "Add specific numbers, percentages, or measurable outcomes"
                })

    # Check contact information
    contact = parsed_data.get("contact", {})
    if contact.get("email"):
        email = contact["email"]
        domain = email.split('@')[-1].lower() if '@' in email else ""
        if domain in UNPROFESSIONAL_DOMAINS:
            issues.append({
                "category": "professionalism",
                "severity": "medium",
                "location": "contact",
                "problem": f"Unprofessional email domain: {domain}",
                "fix": "Consider using a custom domain or Gmail for professional communication"
            })

    if not contact.get("email"):
        issues.append({
            "category": "contact_info",
            "severity": "critical",
            "location": "contact",
            "problem": "Missing email address",
            "fix": "Add your professional email address"
        })

    if not contact.get("phone"):
        issues.append({
            "category": "contact_info",
            "severity": "medium",
            "location": "contact",
            "problem": "Missing phone number",
            "fix": "Add your phone number"
        })

    # Check for summary/objective
    if not parsed_data.get("summary"):
        issues.append({
            "category": "missing_section",
            "severity": "low",
            "location": "summary",
            "problem": "No professional summary or objective",
            "fix": "Consider adding a brief 2-3 sentence summary highlighting your key qualifications"
        })

    return issues


def analyze_formatting(parsed_data: Dict) -> List[Dict]:
    """Analyze formatting issues."""
    issues = []
    formatting = parsed_data.get("formatting", {})

    # Check page count
    page_count = formatting.get("page_count", 1)
    word_count = formatting.get("word_count", 0)

    if page_count > 2:
        issues.append({
            "category": "length",
            "severity": "high",
            "location": "formatting",
            "problem": f"Resume is {page_count} pages long",
            "fix": "Reduce to 1-2 pages by removing outdated or irrelevant information"
        })
    elif page_count == 0 or word_count < 100:
        issues.append({
            "category": "length",
            "severity": "critical",
            "location": "formatting",
            "problem": "Resume appears too short or empty",
            "fix": "Expand with more detailed experience and accomplishments"
        })

    # Check for consistent date formatting
    experience = parsed_data.get("experience", [])
    date_formats = []
    for exp in experience:
        dates = exp.get("dates", "")
        if dates:
            date_formats.append(dates)

    if len(set(date_formats)) > len(date_formats) / 2:  # Many different formats
        issues.append({
            "category": "consistency",
            "severity": "medium",
            "location": "formatting",
            "problem": "Inconsistent date formatting",
            "fix": "Use consistent format like 'Jan 2020 - Dec 2022' throughout"
        })

    return issues


def analyze_ats_compatibility(parsed_data: Dict) -> List[Dict]:
    """Check for ATS (Applicant Tracking System) compatibility issues."""
    issues = []
    text = parsed_data.get("raw_text", "").lower()

    # Check for standard section headers
    has_experience = any(section in text for section in ["experience", "work experience", "employment"])
    has_education = "education" in text
    has_skills = "skills" in text or "technical skills" in text

    if not has_experience:
        issues.append({
            "category": "ats",
            "severity": "critical",
            "location": "structure",
            "problem": "Missing or non-standard 'Experience' section header",
            "fix": "Use clear section header: 'Work Experience' or 'Experience'"
        })

    if not has_education:
        issues.append({
            "category": "ats",
            "severity": "high",
            "location": "structure",
            "problem": "Missing or non-standard 'Education' section header",
            "fix": "Use clear section header: 'Education'"
        })

    if not has_skills:
        issues.append({
            "category": "ats",
            "severity": "medium",
            "location": "structure",
            "problem": "Missing 'Skills' section",
            "fix": "Add a 'Skills' section with relevant technical and soft skills"
        })

    # Check for special characters that might confuse ATS
    special_chars = re.findall(r'[^\w\s,.\-\(\)@:/]', text)
    if len(special_chars) > 20:
        issues.append({
            "category": "ats",
            "severity": "low",
            "location": "formatting",
            "problem": "Contains many special characters",
            "fix": "Minimize use of special characters that may confuse ATS"
        })

    return issues


def analyze_impact(parsed_data: Dict) -> Dict:
    """Analyze the impact of experience bullet points."""
    experience = parsed_data.get("experience", [])
    impact_ratings = {
        "high": 0,
        "medium": 0,
        "low": 0
    }

    for exp in experience:
        for bullet in exp.get("bullets", []):
            rating = rate_bullet_impact(bullet)
            impact_ratings[rating] += 1

    total_bullets = sum(impact_ratings.values())
    if total_bullets == 0:
        return impact_ratings

    return {
        "high": impact_ratings["high"],
        "medium": impact_ratings["medium"],
        "low": impact_ratings["low"],
        "high_percentage": round(impact_ratings["high"] / total_bullets * 100) if total_bullets > 0 else 0
    }


def rate_bullet_impact(bullet: str) -> str:
    """Rate the impact level of a single bullet point."""
    # High impact: strong verb + metrics + context
    has_strong_verb = any(verb in bullet.lower() for verb in STRONG_VERBS[:10])
    has_metrics = bool(re.search(r'\d+[%$]?|\$\d+|by \d+|increased|decreased|reduced|improved', bullet.lower()))
    has_context = len(bullet.split()) > 10

    if has_strong_verb and has_metrics and has_context:
        return "high"
    elif has_strong_verb or has_metrics:
        return "medium"
    else:
        return "low"


def calculate_content_score(issues: List[Dict], parsed_data: Dict) -> float:
    """Calculate content quality score."""
    base_score = 100

    # Deduct points for issues
    for issue in issues:
        if issue["category"] in ["buzzwords", "weak_verbs", "quantification"]:
            if issue["severity"] == "critical":
                base_score -= 10
            elif issue["severity"] == "high":
                base_score -= 5
            elif issue["severity"] == "medium":
                base_score -= 2

    return max(0, base_score)


def calculate_formatting_score(issues: List[Dict], parsed_data: Dict) -> float:
    """Calculate formatting score."""
    base_score = 100

    for issue in issues:
        if issue["category"] in ["length", "consistency"]:
            if issue["severity"] == "critical":
                base_score -= 15
            elif issue["severity"] == "high":
                base_score -= 10
            elif issue["severity"] == "medium":
                base_score -= 5

    return max(0, base_score)


def calculate_ats_score(issues: List[Dict]) -> float:
    """Calculate ATS compatibility score."""
    base_score = 100

    for issue in issues:
        if issue["category"] == "ats":
            if issue["severity"] == "critical":
                base_score -= 20
            elif issue["severity"] == "high":
                base_score -= 10
            elif issue["severity"] == "medium":
                base_score -= 5

    return max(0, base_score)


def calculate_impact_score(impact_analysis: Dict) -> float:
    """Calculate impact score based on bullet point quality."""
    if not impact_analysis:
        return 50

    high_pct = impact_analysis.get("high_percentage", 0)

    # Score based on percentage of high-impact bullets
    if high_pct >= 70:
        return 95
    elif high_pct >= 50:
        return 80
    elif high_pct >= 30:
        return 65
    elif high_pct >= 15:
        return 50
    else:
        return 30


def identify_strengths(parsed_data: Dict, issues: List[Dict]) -> List[str]:
    """Identify positive aspects of the resume."""
    strengths = []

    # Check for good things
    if parsed_data.get("contact", {}).get("linkedin"):
        strengths.append("Includes LinkedIn profile link")

    formatting = parsed_data.get("formatting", {})
    if formatting.get("page_count") == 1:
        strengths.append("Concise one-page format (ideal for most professionals)")

    experience = parsed_data.get("experience", [])
    if len(experience) >= 2:
        strengths.append(f"Shows {len(experience)} relevant work experiences")

    skills = parsed_data.get("skills", [])
    if len(skills) >= 5:
        strengths.append(f"Lists {len(skills)} skills")

    # Check if most bullets have metrics
    total_bullets = sum(len(exp.get("bullets", [])) for exp in experience)
    bullets_with_metrics = 0
    for exp in experience:
        for bullet in exp.get("bullets", []):
            if re.search(r'\d+', bullet):
                bullets_with_metrics += 1

    if total_bullets > 0 and bullets_with_metrics / total_bullets > 0.5:
        strengths.append("Good use of quantifiable metrics in experience bullets")

    return strengths if strengths else ["Resume has basic structure in place"]


def get_critical_fixes(issues: List[Dict]) -> List[str]:
    """Get top 3 most critical fixes."""
    # Sort by severity
    severity_order = {"critical": 4, "high": 3, "medium": 2, "low": 1}
    sorted_issues = sorted(issues, key=lambda x: severity_order.get(x.get("severity", "low"), 0), reverse=True)

    critical_fixes = []
    for issue in sorted_issues[:3]:
        fix_text = f"{issue.get('problem')}: {issue.get('fix')}"
        critical_fixes.append(fix_text)

    return critical_fixes if critical_fixes else ["Keep up the good work!"]
