# Quick Start Guide

Get your AI Digest Generator running in 5 minutes! 🚀

## Prerequisites

- GitHub account with access to your repositories
- Google Gemini API key (free tier available)

## Step 1: Clone and Setup

```bash
# Clone this repository
git clone <your-repo-url>
cd ai-digest

# Run the interactive setup
python setup.py
```

The setup script will guide you through:
- GitHub token configuration
- Gemini API key setup
- Repository selection
- Schedule configuration

## Step 2: Add GitHub Secrets

1. Go to your repository → **Settings** → **Secrets and variables** → **Actions**
2. Add these secrets:
   - `GITHUB_TOKEN`: Your GitHub personal access token
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `GITHUB_REPOS`: Comma-separated list of repositories (e.g., `owner/repo1,owner/repo2`)

## Step 3: Test Locally (Optional)

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GITHUB_TOKEN="your_token"
export GEMINI_API_KEY="your_key"
export GITHUB_REPOS="owner/repo1,owner/repo2"

# Run the generator
python generate_digest.py
```

## Step 4: Enable GitHub Actions

1. Go to your repository → **Actions**
2. Click **"I understand my workflows, go ahead and enable them"**
3. The digest will now run automatically every 2 days

## Step 5: Monitor Results

- Check the `digests/` folder for generated markdown files
- Review GitHub Actions logs for any issues
- Customize the prompt and settings as needed

## Troubleshooting

### Common Issues

**"Repository not found"**
- Ensure your GitHub token has access to all repositories
- Check repository names are in `owner/repo` format

**"Empty digest"**
- Verify there's activity in the specified time period
- Check repository permissions

**"API rate limit exceeded"**
- Wait for rate limits to reset
- Consider reducing the number of repositories

### Getting Help

1. Check the full [README.md](README.md) for detailed documentation
2. Review GitHub Actions logs for error details
3. Open an issue in this repository

## Customization

### Modify Schedule
Edit `.github/workflows/digest.yml`:
```yaml
schedule:
  - cron: '0 9 */2 * *'  # Every 2 days at 9 AM
```

### Customize Prompt
Edit the `generate_gemini_prompt()` method in `generate_digest.py`

### Add Repositories
Update the `GITHUB_REPOS` secret with new repository names

## Example Output

Your digest will look like this:

```markdown
# AI Digest - 2024-01-15

## 🎯 Executive Summary
Strong development momentum with 23 commits across 3 repositories...

## 📊 Repository Activity
### 🏷️ BlueprintLabs/TagPilot
- **12 commits** including ML model integration
- **3 pull requests** with enhanced tagging features
- **2 issues** resolved

## 💡 Key Insights
- High development velocity across all projects
- Focus on core AI/ML capabilities
- Excellent team collaboration patterns

## 🎯 Next Steps
1. Review 3 open pull requests
2. Address performance optimizations
3. Plan cross-project integrations
```

---

**Need help?** Check the [full documentation](README.md) or open an issue! 🆘 