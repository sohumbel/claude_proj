# Resume Roaster 🔥

A command-line tool that analyzes resumes, provides entertaining but constructive criticism, and outputs an improved version with actionable fixes.

## Features

- 📄 **Multi-format Support**: Parse both PDF and DOCX resumes
- 🔍 **Comprehensive Analysis**: Detect 10+ common resume mistakes
- 🎭 **Three Roast Levels**: Choose from gentle, medium, or savage feedback
- 🤖 **AI-Powered**: Uses Claude API for intelligent, contextual roasting
- 📊 **Detailed Scoring**: Get scores for content, formatting, ATS compatibility, and impact
- ✨ **Auto-Improvement**: Generate an improved resume with fixes applied
- 📈 **Progress Tracking**: See what you're doing right and what needs work

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd resume-roaster
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API key:
```bash
echo "ANTHROPIC_API_KEY=your_key_here" > .env
```

Get your API key from: https://console.anthropic.com/

## Usage

### Basic Usage

```bash
python main.py resume.pdf
```

### With Options

```bash
# Savage mode (Gordon Ramsay style)
python main.py resume.pdf --tone savage

# Gentle mode (encouraging feedback)
python main.py resume.pdf --tone gentle

# Export analysis as JSON
python main.py resume.pdf --export-json

# Skip generating improved resume
python main.py resume.pdf --no-improve

# Specify output directory
python main.py resume.pdf --output-dir ./results

# Combine options
python main.py resume.pdf --tone savage --export-json --output-dir ./output
```

## What It Analyzes

### Content Quality
- 🚫 Buzzwords and clichés ("results-oriented", "team player", etc.)
- 💪 Weak vs. strong action verbs
- 📊 Lack of quantifiable metrics
- ✉️ Unprofessional email addresses
- 📝 Missing or weak professional summaries

### ATS Compatibility
- 🤖 Standard section headers
- 📋 Resume structure
- 🔤 Special characters that confuse ATS systems
- 📑 Missing critical sections

### Formatting
- 📏 Resume length (ideal: 1-2 pages)
- 📅 Date format consistency
- 🎨 Overall structure and readability

### Impact Assessment
- 🎯 High-impact vs. low-impact bullet points
- 💥 Action verb + metrics + context formula
- 🏆 Achievement-focused content

## Output

The tool generates:

1. **Roast Report** (terminal output with colorful formatting)
   - Overall score out of 100
   - Category breakdowns
   - Entertaining roasts with actionable fixes
   - Top 3 critical improvements
   - Your resume's strengths

2. **Improved Resume** (`<filename>_improved.docx`)
   - Fixes applied automatically where possible
   - Placeholders for areas needing your input
   - Improvement notes page explaining changes

3. **JSON Analysis** (optional, with `--export-json`)
   - Complete analysis data
   - All issues and scores
   - Machine-readable format for further processing

## Roast Tone Levels

- **Gentle**: Encouraging and supportive with light humor
- **Medium**: Direct and witty with constructive criticism (default)
- **Savage**: Brutally honest and hilarious (Gordon Ramsay mode)

## Example Output

```
🔥 RESUME ROAST REPORT 🔥
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 OVERALL SCORE: 67/100 😬 Needs improvement
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Breakdown:
⚠️ Content Quality: 70/100
❌ ATS Compatibility: 60/100
⚠️ Formatting: 65/100
❌ Impact Score: 50/100

[AI-generated roasts and fixes here...]

🎯 TOP 3 CRITICAL FIXES:
1. Replace "responsible for" with strong action verbs
2. Add quantifiable metrics to experience bullets
3. Remove buzzwords and replace with specific achievements

💪 WHAT YOU'RE DOING RIGHT:
• Concise one-page format
• Includes LinkedIn profile
• Shows 3 relevant work experiences
```

## Requirements

- Python 3.8+
- Anthropic API key
- Internet connection (for API calls)

## Dependencies

- `pdfplumber` - PDF parsing
- `python-docx` - DOCX parsing and generation
- `anthropic` - Claude API integration
- `rich` - Beautiful terminal output
- `python-dotenv` - Environment variable management

## Error Handling

The tool handles common errors gracefully:

- ❌ Invalid file paths
- ❌ Unsupported file formats
- ❌ Corrupted or unreadable files
- ❌ Empty resumes
- ❌ Missing API keys
- ❌ Network errors

Each error provides helpful suggestions for resolution.

## Tips for Best Results

1. **Use a real resume**: The tool works best with actual content
2. **Fill in placeholders**: Review the improved resume and add specific metrics
3. **Run it multiple times**: Track your improvement by scoring updated versions
4. **Try different tones**: Savage mode is hilarious but gentle might be more actionable
5. **Customize for jobs**: Use the improved resume as a template, then customize for specific roles

## Privacy & Security

- Your resume is processed locally and sent only to the Claude API
- No resume data is stored or logged by this tool
- Your API key should be kept private in the `.env` file
- Add `.env` to your `.gitignore` to prevent accidental commits

## Future Enhancements

Potential features for future versions:

- [ ] Web interface
- [ ] Job description keyword matching
- [ ] Industry-specific analysis
- [ ] A/B testing between resume versions
- [ ] LinkedIn profile analysis
- [ ] Cover letter generation
- [ ] Multi-language support

## Contributing

Contributions are welcome! Areas for improvement:

- Better regex patterns for parsing
- More comprehensive buzzword/weak verb lists
- Industry-specific roasting templates
- Improved ATS detection algorithms

## License

MIT License - feel free to use and modify as needed.

## Support

If you encounter issues:

1. Check that your resume file is not password-protected
2. Verify your API key is set correctly in `.env`
3. Ensure all dependencies are installed
4. Try with a different resume file to isolate the issue

## Acknowledgments

- Built with Claude AI for intelligent roasting
- Uses `pdfplumber` for robust PDF parsing
- Terminal UI powered by `rich`

---

**Disclaimer**: This tool provides entertaining and educational feedback. Always review suggestions carefully and use your judgment when making changes to your resume.
