"""
Utility functions for résumé analysis.

This module provides helper functions to extract text from résumé files, perform
simple keyword extraction, compute an Applicant Tracking System (ATS) score
against a job description and generate suggestions for improving bullet points.

If you wish to replace these naive implementations with more sophisticated NLP
models (e.g. spaCy or transformer embeddings), feel free to do so.  The
functions exposed here form the contract used by the FastAPI application.
"""

from __future__ import annotations

import os
import re
from collections import Counter
from typing import List, Set


def extract_text(file_path: str) -> str:
    """Extract text from a résumé file.

    Supports PDF and DOCX formats via optional dependencies.  Falls back to
    reading the file as UTF‑8 text for unknown extensions.

    Args:
        file_path: Path to the uploaded file.

    Returns:
        A single string containing the extracted text.
    """
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == ".docx":
            # DOCX extraction using python-docx
            from docx import Document  # type: ignore

            doc = Document(file_path)
            paragraphs = [p.text for p in doc.paragraphs]
            return "\n".join(paragraphs)
        elif ext == ".pdf":
            # PDF extraction using pdfminer.six
            from pdfminer.high_level import extract_text  # type: ignore

            return extract_text(file_path) or ""
    except Exception:
        # If parsing fails or the library isn't installed, fall back to plain read
        pass

    # Fallback: attempt to read as plain text
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return ""


# A simple list of English stopwords to filter out common words.  This list is
# intentionally short; consider using a more comprehensive stopword list from
# NLTK or spaCy when available.
STOPWORDS: Set[str] = {
    "the", "and", "to", "of", "in", "a", "for", "on", "with", "as", "is",
    "are", "was", "were", "be", "been", "it", "that", "this", "by", "at",
    "an", "from", "or", "we", "you", "your", "our", "their", "they", "i",
    "have", "has", "had", "will", "would", "can", "could", "should", "may",
    "if", "but", "about", "into", "up", "out", "than", "more", "so", "such",
}

# A predefined list of skill keywords; extend this list based on your domain.
SKILL_KEYWORDS: List[str] = [
    "python", "java", "javascript", "typescript", "c++", "c#", "sql",
    "html", "css", "react", "angular", "node", "django", "flask",
    "aws", "azure", "gcp", "docker", "kubernetes", "git", "linux",
    "pandas", "numpy", "tensorflow", "pytorch", "machine learning",
    "data analysis", "communication", "leadership", "project management",
    "problem solving", "teamwork", "time management", "analysis",
]


def _tokenize(text: str) -> List[str]:
    """Lowercase and split a text into alphabetic tokens."""
    return re.findall(r"[a-zA-Z]+", text.lower())


def extract_keywords(text: str, top_n: int = 10) -> List[str]:
    """Extract a set of keywords from the résumé text.

    The function searches for any predefined skill keywords within the text and
    complements them with the most frequent non‑stopword tokens.

    Args:
        text: The résumé text to analyse.
        top_n: The number of most common tokens to include.

    Returns:
        A list of unique keyword strings.
    """
    keywords: Set[str] = set()
    lower_text = text.lower()
    # Find occurrences of predefined skill keywords
    for kw in SKILL_KEYWORDS:
        if kw.lower() in lower_text:
            keywords.add(kw)

    # Tokenize and count frequencies for additional keywords
    tokens = [t for t in _tokenize(text) if t not in STOPWORDS and len(t) > 2]
    freq = Counter(tokens)
    for word, _ in freq.most_common(top_n):
        keywords.add(word)

    return sorted(keywords)


def _filter_tokens(tokens: Set[str]) -> Set[str]:
    """Remove stopwords and very short words from a set of tokens."""
    return {t for t in tokens if t not in STOPWORDS and len(t) > 2}


def compute_ats_score(resume_text: str, job_description: str) -> float:
    """Compute a simple ATS match score between a résumé and job description.

    The score is defined as the percentage of unique, filtered tokens in the job
    description that also appear in the résumé.  It does not weight tokens by
    importance and does not account for context – it serves only as a rough
    approximation.

    Args:
        resume_text: Extracted text from the résumé.
        job_description: The job description provided by the user.

    Returns:
        A percentage (0–100) representing the match score.
    """
    resume_tokens = set(_tokenize(resume_text))
    job_tokens = set(_tokenize(job_description))

    resume_filtered = _filter_tokens(resume_tokens)
    job_filtered = _filter_tokens(job_tokens)

    if not job_filtered:
        return 0.0
    intersection = job_filtered.intersection(resume_filtered)
    score = len(intersection) / len(job_filtered) * 100
    # Round to two decimal places for readability
    return round(score, 2)


def generate_suggestions(resume_text: str) -> List[str]:
    """Generate simple suggestions to improve résumé bullet points.

    This function looks for bullet points (lines starting with '-', '*' or '•')
    and recommends quantifying achievements when no numbers are present.  If no
    bullet‑specific suggestions can be made, it falls back to general advice.

    Args:
        resume_text: Extracted text from the résumé.

    Returns:
        A list of suggestion strings.
    """
    suggestions: List[str] = []
    lines = resume_text.splitlines()
    bullet_lines = [line.strip() for line in lines if line.strip().startswith(("-", "*", "•"))]
    for line in bullet_lines:
        # If the line does not contain any digits, suggest adding quantifiable results
        if not re.search(r"\d", line):
            suggestions.append(f"Consider quantifying this bullet: '{line}'")

    if not suggestions:
        suggestions.append(
            "Include more action verbs and quantify achievements with numbers and percentages."
        )

    return suggestions