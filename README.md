# AI Digest Generator for BlueprintLabs

![Built by BlueprintLabs](https://img.shields.io/badge/built%20by-BlueprintLabs-0057ff?style=flat-square)

🤖 Automated GitHub activity summaries for BlueprintLabs startup projects using Google Gemini 1.5 Flash.

## Overview

This automation generates comprehensive digests of GitHub activity across multiple repositories every 2 days. It analyzes commits, pull requests, and issues to create meaningful summaries that highlight key insights and next steps for your AI startup projects.

## Features

- 🔍 **Multi-repo Analysis**: Collects data from multiple private repositories
- 📊 **Comprehensive Coverage**: Analyzes commits, PRs, issues, and file changes
- 🧠 **AI-Powered Summaries**: Uses Google Gemini 1.5 Flash for intelligent digest generation
- 📅 **Automated Scheduling**: Runs every 2 days via GitHub Actions
- 📝 **Markdown Output**: Clean, structured digests saved as markdown files
- 🔄 **Auto-commit**: Automatically commits and pushes digest files back to the repo

## Repository Structure

```
ai-digest/
├── .github/workflows/
│   └── digest.yml          # GitHub Actions workflow
├── digests/                # Generated digest files
│   └── YYYY-MM-DD-ai-digest.md
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

- **`GITHUB_REPOS`**:
  - Comma-separated list of repository names (format: `owner/repo-name`)
  - Example: `BlueprintLabs/TagPilot,BlueprintLabs/BrainCrate,BlueprintLabs/ai-cofounder`
  - Include the full repository names as they appear in GitHub URLs

### 3. Repository Permissions

Ensure your GitHub token has access to all repositories listed in `GITHUB_REPOS`. For private repositories, the token owner must have access to them.

### 4. Manual Testing

You can test the automation manually:

1. Go to your repository → Actions
2. Select "Generate AI Digest" workflow
3. Click "Run workflow" → "Run workflow"

## Configuration

### Customizing Repository List

Update the `GITHUB_REPOS` secret with your repository names:

```
BlueprintLabs/TagPilot,BlueprintLabs/BrainCrate,BlueprintLabs/ai-cofounder
```

### Modifying Schedule

Edit `.github/workflows/digest.yml` to change the schedule:

```yaml
schedule:
  # Current: Every 2 days at 9 AM UTC
  - cron: '0 9 */2 * *'
  
  # Alternative schedules:
  # Daily at 9 AM: '0 9 * * *'
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
   export GITHUB_REPOS="owner/repo1,owner/repo2"
   ```

3. Run the script:
   ```bash
   python generate_digest.py
   ```

## Output Format

The generated digest includes:

### 📋 Executive Summary
High-level overview of the most significant changes across all repositories.

### 🏗️ Repository Breakdown
Detailed summary for each repository with:
- Commit activity and key changes
- Pull request status and descriptions
- Issue updates and resolutions
- File change patterns

### 💡 Key Insights
AI-generated insights about:
- Development patterns and trends
- Potential bottlenecks or concerns
- Achievement highlights
- Team collaboration patterns

### 🎯 Next Steps
Recommended actions based on the activity:
- Follow-up items from PRs and issues
- Technical debt or refactoring needs
- Priority items for upcoming sprints

### 🔧 Technical Highlights
Notable technical changes:
- Architecture improvements
- Performance optimizations
- Security updates
- Dependency changes

## Example Digest Output

```markdown
# AI Digest - 2024-01-15

## 🎯 Executive Summary
This period saw significant progress across all BlueprintLabs projects, with 23 commits, 5 new pull requests, and 8 issue updates. Key highlights include the completion of TagPilot's core tagging engine and major UI improvements in BrainCrate.

## 📊 Repository Activity

### 🏷️ BlueprintLabs/TagPilot
**Description**: AI-powered content tagging and categorization platform

#### Commits (12)
- **a1b2c3d4** by John Doe: Implement core tagging engine with ML model integration
- **e5f6g7h8** by Jane Smith: Add support for custom tag categories

#### Pull Requests (3)
- **#45** Enhanced tagging accuracy with new ML model (merged) by John Doe
- **#46** Add bulk tagging functionality (open) by Jane Smith

### 🧠 BlueprintLabs/BrainCrate
**Description**: Knowledge management and AI collaboration platform

#### Commits (8)
- **i9j0k1l2** by Alex Johnson: Redesign main dashboard UI with modern components
- **m3n4o5p6** by Sarah Wilson: Implement real-time collaboration features

## 💡 Key Insights
- **High Development Velocity**: 23 commits in 2 days indicates strong team productivity
- **Focus on Core Features**: Majority of work centered on fundamental platform capabilities
- **UI/UX Improvements**: Significant frontend work across multiple projects

## 🎯 Next Steps
1. **Review Open PRs**: 2 pull requests need review and testing
2. **Address Technical Debt**: Consider refactoring the tagging engine for better performance
3. **Plan Integration**: Coordinate TagPilot and BrainCrate integration features

## 🔧 Technical Highlights
- **ML Model Integration**: New tagging engine with 95% accuracy improvement
- **Modern UI Framework**: Migration to React 18 with improved performance
- **Real-time Features**: WebSocket implementation for live collaboration
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
   - Ensure all repositories in `GITHUB_REPOS` exist and are accessible
   - Verify the GitHub token has access to all listed repositories

4. **Empty digests**
   - Check if there's actually activity in the specified time period
   - Verify repository names are in the correct format (`owner/repo`)

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

**Built for BlueprintLabs** 🚀
*Empowering AI startups with intelligent insights* 
