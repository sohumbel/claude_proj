"""Roast generation module using Claude API."""

import os
from typing import Dict
from anthropic import Anthropic
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from config import ROAST_TONES


def generate_roast_report(analysis: Dict, tone: str = "medium") -> str:
    """
    Generate an entertaining but constructive roast report using Claude API.

    Args:
        analysis: Analysis results from analyzer module
        tone: Roast tone level (gentle/medium/savage)

    Returns:
        Formatted roast report as string
    """
    # Get API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set. Please add it to your .env file.")

    client = Anthropic(api_key=api_key)

    # Prepare the prompt
    tone_description = ROAST_TONES.get(tone, ROAST_TONES["medium"])

    prompt = f"""You are a brutally honest but helpful resume coach. Your job is to roast this resume analysis in a {tone_description} tone.

Here's the resume analysis:

SCORES:
- Overall: {analysis['scores']['overall']}/100
- Content Quality: {analysis['scores']['content']}/100
- ATS Compatibility: {analysis['scores']['ats_compatibility']}/100
- Formatting: {analysis['scores']['formatting']}/100
- Impact Score: {analysis['scores']['impact']}/100

ISSUES FOUND:
{format_issues_for_prompt(analysis['issues'])}

STRENGTHS:
{chr(10).join(f"- {s}" for s in analysis['strengths'])}

Your task:
1. For each major issue category (content, formatting, ATS, impact), deliver an entertaining roast (1-2 sentences)
2. Explain why each issue is a problem for job seekers
3. Provide specific, actionable fixes with examples
4. Keep it funny but constructive - the goal is to help, not hurt
5. Use emojis to make it visually engaging
6. End with the top 3 critical fixes and genuine compliments

Format your response in clear sections. Be creative and entertaining while being helpful!"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        roast_content = response.content[0].text

        # Format the complete report
        report = format_roast_report(analysis, roast_content)
        return report

    except Exception as e:
        raise ValueError(f"Failed to generate roast: {str(e)}")


def format_issues_for_prompt(issues: list) -> str:
    """Format issues list for the prompt."""
    if not issues:
        return "No major issues found!"

    formatted = []
    for issue in issues:
        formatted.append(
            f"- [{issue['severity'].upper()}] {issue['category']}: {issue['problem']} (Fix: {issue['fix']})"
        )

    return "\n".join(formatted)


def format_roast_report(analysis: Dict, roast_content: str) -> str:
    """Format the complete roast report with scores and roast."""
    scores = analysis['scores']

    report = f"""
🔥 RESUME ROAST REPORT 🔥
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 OVERALL SCORE: {scores['overall']}/100 {get_score_emoji(scores['overall'])}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Breakdown:
{"✅" if scores['content'] >= 80 else "⚠️" if scores['content'] >= 60 else "❌"} Content Quality: {scores['content']}/100
{"✅" if scores['ats_compatibility'] >= 80 else "⚠️" if scores['ats_compatibility'] >= 60 else "❌"} ATS Compatibility: {scores['ats_compatibility']}/100
{"✅" if scores['formatting'] >= 80 else "⚠️" if scores['formatting'] >= 60 else "❌"} Formatting: {scores['formatting']}/100
{"✅" if scores['impact'] >= 80 else "⚠️" if scores['impact'] >= 60 else "❌"} Impact Score: {scores['impact']}/100

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{roast_content}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 TOP 3 CRITICAL FIXES:
"""

    for i, fix in enumerate(analysis['critical_fixes'], 1):
        report += f"{i}. {fix}\n"

    report += f"""
💪 WHAT YOU'RE DOING RIGHT:
"""

    for strength in analysis['strengths']:
        report += f"• {strength}\n"

    return report


def get_score_emoji(score: int) -> str:
    """Get emoji based on score."""
    if score >= 90:
        return "🌟 Excellent!"
    elif score >= 80:
        return "👍 Pretty good!"
    elif score >= 70:
        return "😐 Decent, but needs work"
    elif score >= 60:
        return "😬 Needs improvement"
    else:
        return "💀 Needs serious help"


def display_roast_report(report: str) -> None:
    """Display roast report in terminal with rich formatting."""
    console = Console()

    # Print the report with syntax highlighting
    console.print(report, style="bold")


def export_json_report(analysis: Dict, output_path: str) -> None:
    """Export analysis results as JSON file."""
    import json

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        print(f"✅ JSON analysis exported to: {output_path}")
    except Exception as e:
        print(f"❌ Failed to export JSON: {str(e)}")
