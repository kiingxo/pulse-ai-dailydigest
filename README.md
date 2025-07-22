# Pulse AI - Daily Digest Generator

![Built by BlueprintLabs](https://img.shields.io/badge/built%20by-BlueprintLabs-0057ff?style=flat-square)

🤖 **Pulse AI** - Automated daily GitHub activity summaries for your startup projects using Google Gemini 1.5 Flash.

## Overview

This automation generates focused **24-hour pulse digests** of GitHub activity across multiple repositories. It analyzes commits, pull requests, and issues from the past day to create concise, actionable summaries that give you a daily pulse on your team's progress.

## Features

- 🔍 **Multi-repo Analysis**: Collects data from multiple repositories (public/private)
- ⚡ **24-Hour Focus**: Analyzes only the past 24 hours of activity for daily pulse
- 🧠 **AI-Powered Summaries**: Uses Google Gemini 1.5 Flash for intelligent digest generation
- 📅 **Automated Scheduling**: Runs daily via GitHub Actions
- 📝 **Markdown Output**: Clean, structured Pulse AI digests saved as markdown files
- 🔄 **Auto-commit**: Automatically commits and pushes digest files back to the repo
- 🚀 **Smart Filtering**: Skips repositories with no recent activity for efficiency

## Repository Structure

```
ai-digest/
├── .github/workflows/
│   └── digest.yml          # GitHub Actions workflow
├── digests/                # Generated digest files
│   └── YYYY-MM-DD-pulse-ai-HH-MM.md
├── generate_digest.py      # Main Python script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Setup Instructions

### 1. Repository Setup

1. **Fork or clone this repository** to your GitHub account
2. **Enable GitHub Actions** in your repository settings
3. **Ensure the repository has write permissions** for GitHub Actions

### 2. GitHub Secrets Configuration

Navigate to your repository → Settings → Secrets and variables → Actions, then add the following secrets:

#### Required Secrets:

- **`PAT_TOKEN`**: 
  - Go to Settings → Developer settings → Personal access tokens → Tokens (classic)
  - Generate a new token with `repo` scope
  - Copy the token and add it as a secret

- **`GEMINI_API_KEY`**:
  - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
  - Create a new API key
  - Copy the key and add it as a secret

- **`REPO_LIST`**:
  - Comma-separated list of repository names (format: `owner/repo-name`)
  - Example: `kiingxo/pulse-ai-dailydigest,kiingxo/blueprint-website,kiingxo/portfolio-website`
  - Include the full repository names as they appear in GitHub URLs

### 3. Repository Permissions

Ensure your GitHub token has access to all repositories listed in `REPO_LIST`. For private repositories, the token owner must have access to them.

### 4. Manual Testing

You can test the automation manually:

1. Go to your repository → Actions
2. Select "Generate Pulse AI" workflow
3. Click "Run workflow" → "Run workflow"

## Configuration

### Customizing Repository List

Update the `REPO_LIST` secret with your repository names:

```
kiingxo/pulse-ai-dailydigest,kiingxo/blueprint-website,kiingxo/portfolio-website
```

### Modifying Schedule

Edit `.github/workflows/digest.yml` to change the schedule:

```yaml
schedule:
  # Current: Daily at 9 AM UTC
  - cron: '0 9 * * *'
  
  # Alternative schedules:
  # Every 2 days: '0 9 */2 * *'
  # Weekly on Mondays: '0 9 * * 1'
  # Every 3 days: '0 9 */3 * *'
```

### Local Development

To run the script locally:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variables:
   ```bash
   export PAT_TOKEN="your_PAT_TOKEN"
   export GEMINI_API_KEY="your_gemini_api_key"
   export REPO_LIST="owner/repo1,owner/repo2"
   ```

3. Run the script:
   ```bash
   python generate_digest.py
   ```

## Output Format

The generated **Pulse AI** digest includes:

### 📋 Executive Summary
High-level overview of the most significant changes in the past 24 hours.

### 🏗️ Repository Breakdown
Detailed summary for each repository with recent activity:
- Commit activity and key changes
- Pull request status and descriptions
- Issue updates and resolutions
- File change patterns

### 💡 Key Insights
AI-generated insights about:
- Development patterns and trends from today's activity
- Potential bottlenecks or concerns
- Achievement highlights
- Team collaboration patterns

### 🎯 Next Steps
Recommended actions based on the recent activity:
- Follow-up items from PRs and issues
- Technical debt or refactoring needs
- Priority items for upcoming sprints

### 🔧 Technical Highlights
Notable technical changes from the past 24 hours:
- Architecture improvements
- Performance optimizations
- Security updates
- Dependency changes

## Example Pulse AI Digest Output

```markdown
# Pulse AI: 2025-07-20 - Daily Summary (09-00 UTC)

## 🎯 Executive Summary
Today's pulse shows focused progress across key projects with 8 commits, 2 new pull requests, and 3 issue updates in the past 24 hours. Highlights include the completion of the Pulse AI digest generator and UI improvements in the portfolio website.

## 📊 Repository Activity

### 🤖 kiingxo/pulse-ai-dailydigest
**Description**: AI-powered daily digest generator for GitHub activity

#### Commits (3)
- **a1b2c3d4** by kiingxo: Implement 24-hour activity filtering
- **e5f6g7h8** by kiingxo: Add Pulse AI branding and daily summary format

#### Pull Requests (1)
- **#12** Convert to Pulse AI 24-hour daily digest format (merged) by kiingxo

### 🌐 kiingxo/portfolio-website
**Description**: Personal portfolio website built with Next.js

#### Commits (5)
- **i9j0k1l2** by kiingxo: Update project showcase with new Pulse AI project
- **m3n4o5p6** by kiingxo: Improve responsive design for mobile devices

## 💡 Key Insights
- **Focused Development**: 8 commits in 24 hours shows steady daily progress
- **Product Launch**: Pulse AI digest generator completed and operational
- **UI/UX Focus**: Portfolio updates indicate ongoing design improvements

## 🎯 Next Steps
1. **Monitor Pulse AI**: Track the daily digest generation performance
2. **Portfolio Polish**: Continue mobile responsiveness improvements
3. **Documentation**: Update project documentation for new features

## 🔧 Technical Highlights
- **24-Hour Filtering**: New time-based activity filtering for focused daily digests
- **Pulse AI Branding**: Consistent branding and formatting across all outputs
- **Smart Repository Filtering**: Automatic skipping of inactive repositories
```

## Troubleshooting

### Common Issues

1. **"PAT_TOKEN environment variable is required"**
   - Ensure the `PAT_TOKEN` secret is properly configured
   - Verify the token has the `repo` scope

2. **"GEMINI_API_KEY environment variable is required"**
   - Check that the `GEMINI_API_KEY` secret is set correctly
   - Verify the API key is valid and has sufficient quota

3. **"Repository not found" errors**
   - Ensure all repositories in `REPO_LIST` exist and are accessible
   - Verify the GitHub token has access to all listed repositories

4. **Empty digests**
   - Check if there's actually activity in the past 24 hours
   - Verify repository names are in the correct format (`owner/repo`)
   - The system now automatically skips repositories with no recent activity

### Debugging

Enable debug logging by modifying the script:

```python
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
```

### Manual Testing

Test individual components:

```bash
# Test GitHub API access
python -c "from github import Github; g = Github('your_token'); print(g.get_user().login)"

# Test Gemini API
python -c "import google.generativeai as genai; genai.configure(api_key='your_key'); model = genai.GenerativeModel('gemini-1.5-flash'); print(model.generate_content('Hello').text)"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review GitHub Actions logs for detailed error messages
3. Open an issue in this repository

---

![Built by BlueprintLabs](https://img.shields.io/badge/built%20by-BlueprintLabs-0057ff?style=flat-square)
