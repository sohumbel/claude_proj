#!/usr/bin/env python3
"""
Resume Roaster - CLI tool for analyzing and improving resumes.

Usage:
    python main.py resume.pdf
    python main.py resume.pdf --tone savage
    python main.py resume.pdf --export-json --no-improve
"""

import sys
import os
import argparse
from pathlib import Path
from typing import Dict
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

# Load environment variables
load_dotenv()

# Import modules
from parser import parse_resume
from analyzer import analyze_resume
from roaster import generate_roast_report, display_roast_report, export_json_report
from improver import generate_improved_resume


def main():
    """Main CLI entry point."""
    console = Console()

    # Parse command line arguments
    args = parse_arguments()

    # Validate file path
    if not os.path.exists(args.file_path):
        console.print(f"[red]❌ Error: File not found: {args.file_path}[/red]")
        sys.exit(1)

    # Validate file type
    if not args.file_path.lower().endswith(('.pdf', '.docx')):
        console.print("[red]❌ Error: Unsupported file format. Please provide a PDF or DOCX file.[/red]")
        sys.exit(1)

    # Check API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[red]❌ Error: ANTHROPIC_API_KEY not found![/red]")
        console.print("Please create a .env file with your API key:")
        console.print("  echo 'ANTHROPIC_API_KEY=your_key_here' > .env")
        sys.exit(1)

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:

            # Step 1: Parse resume
            task1 = progress.add_task("🔍 Parsing resume...", total=None)
            parsed_data = parse_resume(args.file_path)
            progress.update(task1, completed=True)
            console.print("✅ Resume parsed successfully!\n")

            # Step 2: Analyze resume
            task2 = progress.add_task("🔬 Analyzing content...", total=None)
            analysis = analyze_resume(parsed_data)
            progress.update(task2, completed=True)
            console.print("✅ Analysis complete!\n")

            # Step 3: Generate roast report
            task3 = progress.add_task(f"🔥 Generating {args.tone} roast...", total=None)
            roast_report = generate_roast_report(analysis, args.tone)
            progress.update(task3, completed=True)

        # Display the roast report
        console.print("\n")
        display_roast_report(roast_report)
        console.print("\n")

        # Step 4: Export JSON if requested
        if args.export_json:
            output_dir = args.output_dir or os.path.dirname(args.file_path) or "."
            json_path = os.path.join(output_dir, "resume_analysis.json")
            export_json_report(analysis, json_path)

        # Step 5: Generate improved resume if not disabled
        if not args.no_improve:
            console.print("📝 Generating improved resume...\n")
            output_dir = args.output_dir or os.path.dirname(args.file_path) or "."

            # Determine output filename
            base_name = Path(args.file_path).stem
            output_path = os.path.join(output_dir, f"{base_name}_improved.docx")

            improved_path = generate_improved_resume(parsed_data, analysis, output_path)
            console.print(f"✅ Improved resume saved: [green]{improved_path}[/green]\n")

        # Print summary and next steps
        print_summary(console, args, analysis)

    except ValueError as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]❌ Unexpected error: {str(e)}[/red]")
        console.print("[yellow]💡 Tip: Make sure your PDF is not password-protected or corrupted.[/yellow]")
        sys.exit(1)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Resume Roaster - Analyze and improve your resume with AI-powered feedback",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py resume.pdf
  python main.py resume.pdf --tone savage
  python main.py resume.pdf --export-json --output-dir ./results
  python main.py resume.docx --no-improve

Tone options:
  gentle  - Encouraging feedback with light humor
  medium  - Direct criticism with wit (default)
  savage  - Brutally honest and hilarious (Gordon Ramsay mode)
        """
    )

    parser.add_argument(
        "file_path",
        help="Path to resume file (PDF or DOCX)"
    )

    parser.add_argument(
        "--tone",
        choices=["gentle", "medium", "savage"],
        default="medium",
        help="Roast tone level (default: medium)"
    )

    parser.add_argument(
        "--export-json",
        action="store_true",
        help="Export analysis as JSON file"
    )

    parser.add_argument(
        "--no-improve",
        action="store_true",
        help="Skip generating improved resume"
    )

    parser.add_argument(
        "--output-dir",
        help="Custom output directory for generated files"
    )

    parser.add_argument(
        "--job-description",
        help="Path to job description file for keyword matching (future feature)"
    )

    return parser.parse_args()


def print_summary(console: Console, args, analysis: Dict):
    """Print summary and next steps."""
    console.print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    console.print("✅ [green bold]DONE![/green bold]\n")

    # Print what was generated
    output_dir = args.output_dir or os.path.dirname(args.file_path) or "."

    if not args.no_improve:
        base_name = Path(args.file_path).stem
        console.print(f"📁 Improved resume saved: {base_name}_improved.docx")

    if args.export_json:
        console.print(f"📊 Analysis exported: resume_analysis.json")

    console.print("\n[cyan bold]Next steps:[/cyan bold]")
    console.print("1. Review the improved resume carefully")
    console.print("2. Fill in any [PLACEHOLDER] or [ADD:...] items with real data")
    console.print("3. Customize the resume for specific job applications")
    console.print("4. Run this tool again to track your improvement!")

    # Show score-based encouragement
    score = analysis["scores"]["overall"]
    if score >= 80:
        console.print(f"\n[green]🌟 Great job! Your resume scored {score}/100![/green]")
    elif score >= 60:
        console.print(f"\n[yellow]💪 Keep going! Your resume scored {score}/100. You're on the right track![/yellow]")
    else:
        console.print(f"\n[red]🔨 Your resume scored {score}/100. Time to rebuild and come back stronger![/red]")

    console.print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")


if __name__ == "__main__":
    main()
