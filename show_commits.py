from github import Github
from datetime import timezone
import os

g = Github(os.environ.get('GITHUB_TOKEN'))
repo = g.get_repo('kiingxo/chat-ai')
commits = repo.get_commits()

for i, c in enumerate(commits[:5]):
    print(f'{i+1}. {c.commit.author.date.astimezone(timezone.utc)} - {c.commit.author.name} - {c.commit.message[:60]}') 