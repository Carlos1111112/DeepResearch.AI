from pathlib import Path
from typing import Dict
from dotenv import load_dotenv
import os
import google.generativeai as genai

from ingestion import fetch_repo_code

"""Module to analyze code snippets using Google Gemini."""

# Load environment variables
load_dotenv(dotenv_path=Path('.env'))

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise EnvironmentError('GEMINI_API_KEY not found in .env')

# Configure generative AI client
genai.configure(api_key=GEMINI_API_KEY)


def summarize_code(snippets: Dict[str, str]) -> str:
    """Summarize given code snippets using Gemini."""
    code_text = "\n".join(snippets.values())
    prompt = (
        "Eres un investigador experto en software. Analiza este código y "
        "extrae sus objetivos, puntos fuertes y débiles:\n\n" + code_text
    )
    response = genai.chat.create(
        model="models/chat-bison-001",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.last


if __name__ == '__main__':
    repo_code = fetch_repo_code('psf', 'requests')
    summary = summarize_code(repo_code)
    print(summary)
