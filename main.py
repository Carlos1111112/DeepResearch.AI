from pathlib import Path
from typing import Dict
import sys
from dotenv import load_dotenv

from ingestion import fetch_repo_code
from analysis import summarize_code

"""Main entry point for the deep research engine."""

load_dotenv(dotenv_path=Path('.env'))


def main(owner: str = 'psf', repo: str = 'requests') -> None:
    """Generate summary report for a GitHub repository."""
    code_snippets = fetch_repo_code(owner, repo)
    summary = summarize_code(code_snippets)
    report_content = f"# Reporte de {owner}/{repo}\n\n{summary}\n"
    Path('report.md').write_text(report_content, encoding='utf-8')
    print('Reporte generado en report.md')


if __name__ == '__main__':
    args = sys.argv[1:]
    owner = args[0] if len(args) > 0 else 'psf'
    repo = args[1] if len(args) > 1 else 'requests'
    main(owner, repo)
