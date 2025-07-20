#!/usr/bin/env python3
"""
AI Digest Generator for BlueprintLabs
Automatically generates summaries of GitHub activity across multiple repositories.
"""

import os
import sys
import json
import base64
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import requests
from github import Github, Auth
import google.generativeai as genai
from pathlib import Path
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AIDigestGenerator:
    def __init__(self):
        self.github_token = os.getenv('PAT_TOKEN')
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.repos = os.getenv('REPO_LIST', '').split(',')
        
        if not self.github_token:
            raise ValueError("PAT_TOKEN environment variable is required")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        if not self.repos:
            raise ValueError("REPO_LIST environment variable is required")
        
        # Initialize GitHub client
        self.github = Github(auth=Auth.Token(self.github_token))
        
        # Initialize Gemini
        genai.configure(api_key=self.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Create digests directory
        self.digests_dir = Path('digests')
        self.digests_dir.mkdir(exist_ok=True)
        
        # Calculate date range (last 24 hours)
        self.end_date = datetime.now()
        self.start_date = self.end_date - timedelta(days=1)
        
        logger.info(f"Generating digest for period: {self.start_date.date()} to {self.end_date.date()}")
    
    def collect_repo_data(self, repo_name: str) -> Dict[str, Any]:
        """Collect all activity data from a single repository."""
        try:
            repo = self.github.get_repo(repo_name)
            logger.info(f"Collecting data from {repo_name}")
            
            data = {
                'name': repo_name,
                'description': repo.description or '',
                'commits': [],
                'pull_requests': [],
                'issues': [],
                'file_changes': []
            }
            
            # Check for recent commits first
            commits = repo.get_commits(since=self.start_date, until=self.end_date)
            commit_count = 0
            for commit in commits:
                commit_count += 1
                data['commits'].append({
                    'sha': commit.sha[:8],
                    'message': commit.commit.message,
                    'author': commit.commit.author.name,
                    'date': commit.commit.author.date.isoformat(),
                    'files_changed': [f.filename for f in commit.files] if commit.files else []
                })
            
            # Check for recent PRs
            prs = repo.get_pulls(state='all', sort='updated', direction='desc')
            pr_count = 0
            for pr in prs:
                # Convert timezone-aware datetime to naive for comparison
                pr_updated_naive = pr.updated_at.replace(tzinfo=None)
                if self.start_date <= pr_updated_naive <= self.end_date:
                    pr_count += 1
                    data['pull_requests'].append({
                        'number': pr.number,
                        'title': pr.title,
                        'body': pr.body or '',
                        'state': pr.state,
                        'author': pr.user.login,
                        'created_at': pr.created_at.isoformat(),
                        'updated_at': pr.updated_at.isoformat(),
                        'labels': [label.name for label in pr.labels],
                        'files_changed': [f.filename for f in pr.get_files()]
                    })
            
            # Check for recent issues
            issues = repo.get_issues(state='all', sort='updated', direction='desc')
            issue_count = 0
            for issue in issues:
                # Convert timezone-aware datetime to naive for comparison
                issue_updated_naive = issue.updated_at.replace(tzinfo=None)
                if self.start_date <= issue_updated_naive <= self.end_date:
                    issue_count += 1
                    data['issues'].append({
                        'number': issue.number,
                        'title': issue.title,
                        'body': issue.body or '',
                        'state': issue.state,
                        'author': issue.user.login,
                        'created_at': issue.created_at.isoformat(),
                        'updated_at': issue.updated_at.isoformat(),
                        'labels': [label.name for label in issue.labels],
                        'comments_count': issue.comments
                    })
            
            total_activity = commit_count + pr_count + issue_count
            
            if total_activity == 0:
                logger.info(f"No activity in the past 24 hours for {repo_name} - skipping from digest")
                return None
            else:
                logger.info(f"Collected {commit_count} commits, {pr_count} PRs, {issue_count} issues from {repo_name}")
                return data
            
        except Exception as e:
            logger.error(f"Error collecting data from {repo_name}: {e}")
            return {'name': repo_name, 'error': str(e)}
    
    def generate_gemini_prompt(self, all_repo_data: List[Dict[str, Any]]) -> str:
        """Generate a comprehensive prompt for Gemini to create the digest."""
        
        # Filter out repos with errors
        valid_repos = [repo for repo in all_repo_data if 'error' not in repo]
        
        if not valid_repos:
            return "No activity found in any repositories for the past 24 hours."
        
        prompt = f"""You are an AI assistant creating a daily pulse digest of GitHub activity for BlueprintLabs, a startup lab managing multiple AI-related projects.

PERIOD: Last 24 hours ({self.start_date.strftime('%Y-%m-%d %H:%M')} to {self.end_date.strftime('%Y-%m-%d %H:%M')})

REPOSITORY ACTIVITY DATA:
"""
        
        for repo_data in valid_repos:
            prompt += f"\n## {repo_data['name']}\n"
            prompt += f"Description: {repo_data['description']}\n"
            
            # Commits
            if repo_data['commits']:
                prompt += f"\n### Commits ({len(repo_data['commits'])})\n"
                for commit in repo_data['commits']:
                    prompt += f"- **{commit['sha']}** by {commit['author']}: {commit['message']}\n"
                    if commit['files_changed']:
                        prompt += f"  Files: {', '.join(commit['files_changed'][:5])}{'...' if len(commit['files_changed']) > 5 else ''}\n"
            
            # Pull Requests
            if repo_data['pull_requests']:
                prompt += f"\n### Pull Requests ({len(repo_data['pull_requests'])})\n"
                for pr in repo_data['pull_requests']:
                    prompt += f"- **#{pr['number']}** {pr['title']} ({pr['state']}) by {pr['author']}\n"
                    if pr['body']:
                        prompt += f"  Description: {pr['body'][:200]}{'...' if len(pr['body']) > 200 else ''}\n"
                    if pr['labels']:
                        prompt += f"  Labels: {', '.join(pr['labels'])}\n"
            
            # Issues
            if repo_data['issues']:
                prompt += f"\n### Issues ({len(repo_data['issues'])})\n"
                for issue in repo_data['issues']:
                    prompt += f"- **#{issue['number']}** {issue['title']} ({issue['state']}) by {issue['author']}\n"
                    if issue['body']:
                        prompt += f"  Description: {issue['body'][:200]}{'...' if len(issue['body']) > 200 else ''}\n"
                    if issue['labels']:
                        prompt += f"  Labels: {', '.join(issue['labels'])}\n"
        
        prompt += """

TASK: Create a "Pulse AI" daily digest with the title "Pulse AI: [Date] - Daily Summary" that includes:

1. **Executive Summary** - High-level overview of the most significant changes in the past 24 hours
2. **Repository Breakdown** - Detailed summary for each repository with recent activity
3. **Key Insights** - Important patterns, achievements, or concerns identified from today's activity
4. **Next Steps** - Recommended actions based on the recent activity
5. **Technical Highlights** - Notable technical changes or improvements from the past 24 hours

FORMAT REQUIREMENTS:
- Start with the title "Pulse AI: [Current Date] - Daily Summary"
- Use proper markdown formatting
- Include emojis for visual appeal and quick scanning
- Group related changes logically
- Highlight critical items with bold text
- Keep it professional but engaging
- Focus on business impact and technical progress
- Extract actionable insights from commit messages and PR descriptions
- Identify potential TODOs or follow-up items

STYLE: Write in a clear, professional tone suitable for startup leadership review. Focus on what matters most for business and technical progress. Make it feel like a daily pulse check on the team's progress.
"""
        
        return prompt
    
    def generate_digest(self, all_repo_data: List[Dict[str, Any]]) -> str:
        """Generate the digest using Gemini API."""
        prompt = self.generate_gemini_prompt(all_repo_data)
        
        try:
            logger.info("Generating digest with Gemini...")
            response = self.model.generate_content(prompt)
            
            if response.text:
                return response.text
            else:
                logger.error("Empty response from Gemini")
                return self.generate_fallback_digest(all_repo_data)
                
        except Exception as e:
            logger.error(f"Error generating digest with Gemini: {e}")
            return self.generate_fallback_digest(all_repo_data)
    
    def generate_fallback_digest(self, all_repo_data: List[Dict[str, Any]]) -> str:
        """Generate a basic digest if Gemini fails."""
        today = datetime.now().strftime('%Y-%m-%d')
        
        digest = f"""# Pulse AI: {today} - Daily Summary

## Executive Summary
Generated pulse digest for the last 24 hours ({self.start_date.strftime('%Y-%m-%d %H:%M')} to {self.end_date.strftime('%Y-%m-%d %H:%M')}).

## Repository Activity

"""
        
        for repo_data in all_repo_data:
            if 'error' in repo_data:
                digest += f"### {repo_data['name']}\nError: {repo_data['error']}\n\n"
                continue
                
            digest += f"### {repo_data['name']}\n"
            digest += f"- Commits: {len(repo_data['commits'])}\n"
            digest += f"- Pull Requests: {len(repo_data['pull_requests'])}\n"
            digest += f"- Issues: {len(repo_data['issues'])}\n\n"
        
        digest += "## Note\nThis is a fallback digest generated due to API issues. Please check the logs for details.\n"
        
        return digest
    
    def save_digest(self, digest_content: str) -> str:
        """Save the digest to a markdown file."""
        today = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%H:%M UTC')
        
        # Create filename with actual time
        time_suffix = current_time.replace(':', '-')
        filename = f"{today}-pulse-ai-{time_suffix}.md"
        filepath = self.digests_dir / filename
        
        # Add time header to content and ensure it's not overridden by AI response
        header = f"# Pulse AI: {today} - Daily Summary ({time_suffix.title()})\n\n"
        
        # Remove any existing title from the AI response to avoid duplication
        lines = digest_content.split('\n')
        if lines and lines[0].startswith('# '):
            # Skip the first line if it's a title
            digest_content = '\n'.join(lines[1:])
        
        full_content = header + digest_content
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        logger.info(f"Digest saved to {filepath}")
        return str(filepath)
    
    def commit_and_push(self, filepath: str):
        """Commit and push the digest file to the repository."""
        try:
            # Add the file
            subprocess.run(['git', 'add', filepath], check=True)
            
            # Commit
            today = datetime.now().strftime('%Y-%m-%d')
            current_time = datetime.now().strftime('%H:%M UTC')
            
            commit_message = f"🤖 Add Pulse AI for {today} ({current_time})"
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            
            # Push
            subprocess.run(['git', 'push'], check=True)
            
            logger.info(f"Successfully committed and pushed {filepath}")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Error in git operations: {e}")
            raise
    
    def run(self):
        """Main execution method."""
        try:
            logger.info("Starting AI Digest generation...")
            
            # Collect data from all repositories
            all_repo_data = []
            
            for repo in self.repos:
                repo = repo.strip()
                if repo:
                    data = self.collect_repo_data(repo)
                    if data is not None:  # Only add repositories with activity
                        all_repo_data.append(data)
            
            # Generate digest
            digest_content = self.generate_digest(all_repo_data)
            
            # Save digest
            filepath = self.save_digest(digest_content)
            
            # Commit and push
            self.commit_and_push(filepath)
            
            logger.info("AI Digest generation completed successfully!")
            
        except Exception as e:
            logger.error(f"Error in digest generation: {e}")
            sys.exit(1)

def main():
    """Main entry point."""
    generator = AIDigestGenerator()
    generator.run()

if __name__ == "__main__":
    main() 