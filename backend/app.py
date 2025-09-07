"""
FastAPI application for the Smart Resume Analyzer.

This module defines a single `/analyze` endpoint that accepts a résumé
file and a job description via multipart/form-data.  It leverages
`utils.py` to extract text, compute keywords, calculate an ATS score and
generate suggestions.  The response is returned as JSON for easy
consumption by a frontend.
"""

from __future__ import annotations

import os
import tempfile
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import utils

# Initialize the FastAPI application
app = FastAPI(title="Smart Resume Analyzer")

# Allow all origins to simplify local development with a React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalysisResult(BaseModel):
    """Schema for the résumé analysis response."""

    keywords: list[str]
    ats_score: float
    suggestions: list[str]


@app.post("/analyze", response_model=AnalysisResult)
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...),
) -> AnalysisResult:
    """Analyze a résumé and compute ATS match results.

    Args:
        file: The uploaded résumé file (PDF, DOCX or plain text).
        job_description: A free‑text job description against which the résumé
            should be compared.

    Returns:
        An AnalysisResult containing extracted keywords, ATS score and
        suggestions.
    """
    # Read file content into a temporary file to pass into text extractors
    contents = await file.read()
    suffix = os.path.splitext(file.filename or "")[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        resume_text = utils.extract_text(tmp_path)
    finally:
        # Clean up the temporary file
        try:
            os.unlink(tmp_path)
        except Exception:
            pass

    keywords = utils.extract_keywords(resume_text)
    ats_score = utils.compute_ats_score(resume_text, job_description)
    suggestions = utils.generate_suggestions(resume_text)

    return AnalysisResult(keywords=keywords, ats_score=ats_score, suggestions=suggestions)