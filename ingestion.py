from pathlib import Path
from typing import Dict
from dotenv import load_dotenv
import os
from github import Github


"""Module to fetch code from GitHub repositories."""

# Load environment variables from .env
load_dotenv(dotenv_path=Path('.env'))

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    raise EnvironmentError('GITHUB_TOKEN not found in .env')

# Initialize GitHub client
github_client = Github(GITHUB_TOKEN)


def fetch_repo_code(owner: str, repo: str, ext: str = '.py') -> Dict[str, str]:
    """Recursively fetch files with the given extension from a GitHub repo."""
    repository = github_client.get_repo(f"{owner}/{repo}")
    contents = repository.get_contents("")
    files = {}
    while contents:
        file_content = contents.pop(0)
        if file_content.type == 'dir':
            contents.extend(repository.get_contents(file_content.path))
        else:
            if file_content.path.endswith(ext):
                files[file_content.path] = file_content.decoded_content.decode('utf-8')
    return files


if __name__ == '__main__':
    data = fetch_repo_code('psf', 'requests')
    print(f'Fetched {len(data)} files.')
