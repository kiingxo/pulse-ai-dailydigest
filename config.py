"""
Configuration file for AI Digest Generator
Customize these settings to match your needs.
"""

import os
from datetime import timedelta

# GitHub Configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPOS = os.getenv('GITHUB_REPOS', '').split(',')

# Gemini API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_MODEL = 'gemini-1.5-flash'  # Alternative: 'gemini-1.5-pro'

# Digest Configuration
DIGEST_PERIOD_DAYS = 2  # How many days back to analyze
DIGEST_TIMEZONE = 'UTC'  # Timezone for date calculations

# Output Configuration
DIGEST_DIR = 'digests'  # Directory to save digest files
DIGEST_FILENAME_FORMAT = '{date}-ai-digest.md'  # Format: 2024-01-15-ai-digest.md

# Git Configuration
GIT_COMMIT_MESSAGE_FORMAT = '🤖 Add AI Digest for {date}'
GIT_USER_NAME = 'GitHub Action'
GIT_USER_EMAIL = 'action@github.com'

# Logging Configuration
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

# Repository Data Collection Settings
MAX_COMMITS_PER_REPO = 100  # Maximum commits to collect per repository
MAX_PRS_PER_REPO = 50       # Maximum PRs to collect per repository
MAX_ISSUES_PER_REPO = 50    # Maximum issues to collect per repository

# Gemini Prompt Customization
CUSTOM_PROMPT_PREFIX = """
You are an AI assistant creating a comprehensive digest of GitHub activity for BlueprintLabs, 
a startup lab managing multiple AI-related projects including TagPilot, BrainCrate, and AI CoFounder.

Focus on:
- Business impact and strategic value
- Technical achievements and innovations
- Team collaboration and productivity patterns
- Risk identification and mitigation opportunities
- Cross-project synergies and integration opportunities
"""

CUSTOM_PROMPT_SUFFIX = """
Additional Instructions:
- Highlight any security-related changes or concerns
- Identify potential technical debt or refactoring needs
- Note any dependencies or integration points between projects
- Suggest opportunities for knowledge sharing or code reuse
- Flag any issues that might require immediate attention
"""

# Error Handling
RETRY_ATTEMPTS = 3
RETRY_DELAY_SECONDS = 5

# Performance Settings
REQUEST_TIMEOUT_SECONDS = 30
BATCH_SIZE = 10  # Process repositories in batches

# Optional Features
ENABLE_FILE_CHANGE_ANALYSIS = True
ENABLE_COMMIT_MESSAGE_ANALYSIS = True
ENABLE_PERFORMANCE_METRICS = True
ENABLE_CROSS_REPO_INSIGHTS = True

# Custom Repository Descriptions (optional)
REPOSITORY_DESCRIPTIONS = {
    'BlueprintLabs/TagPilot': 'AI-powered content tagging and categorization platform',
    'BlueprintLabs/BrainCrate': 'Knowledge management and AI collaboration platform',
    'BlueprintLabs/ai-cofounder': 'AI-powered business planning and strategy platform',
    # Add more repositories as needed
}

# Custom Labels and Categories
PRIORITY_LABELS = ['high-priority', 'critical', 'urgent', 'blocker']
FEATURE_LABELS = ['enhancement', 'feature', 'feature-request']
BUG_LABELS = ['bug', 'fix', 'hotfix']
PERFORMANCE_LABELS = ['performance', 'optimization', 'speed']

# Digest Sections (customize which sections to include)
INCLUDE_SECTIONS = {
    'executive_summary': True,
    'repository_breakdown': True,
    'key_insights': True,
    'next_steps': True,
    'technical_highlights': True,
    'metrics_summary': True,
    'team_activity': True,
    'security_notes': True,
}

# Custom Emojis for Different Types of Changes
EMOJI_MAPPING = {
    'feature': '✨',
    'bugfix': '🐛',
    'performance': '⚡',
    'security': '🔒',
    'refactor': '🔧',
    'documentation': '📚',
    'test': '🧪',
    'ci_cd': '🚀',
    'dependencies': '📦',
    'ui_ux': '🎨',
    'api': '🔌',
    'database': '🗄️',
    'ml_ai': '🧠',
    'mobile': '📱',
    'web': '🌐',
    'backend': '⚙️',
    'frontend': '🎯',
} 