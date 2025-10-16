# Smart Resume Analyzer


Smart Resume Analyzer is a simple web application that helps job‑seekers analyze their résumés (PDF or DOCX) against a job description.  It extracts relevant keywords, computes a rough Applicant Tracking System (ATS) match score and proposes suggestions to improve phrasing and quantify accomplishments.

## Features

- **Upload a résumé** in PDF or DOCX format via the frontend.
- **Keyword extraction** using a simple NLP pipeline to find skills, tools and other frequently used terms.
- **ATS score** calculation that measures overlap between the résumé text and the provided job description.
- **Actionable suggestions** to encourage quantifying achievements and improving wording.
- **Full‑stack example** consisting of a Python backend (FastAPI) and a React frontend.

## Project Structure

```
resume_analyzer/
├── backend/           # Python FastAPI service
│   ├── app.py         # API routes and server setup
│   ├── utils.py       # Text extraction and analysis helpers
│   └── requirements.txt
├── frontend/          # React application
│   ├── package.json   # npm dependencies and scripts
│   ├── src/
│   │   ├── App.js     # Main React component
│   │   └── index.js   # Entry point
│   └── public/
│       └── index.html # HTML template
├── .gitignore         # Ignore build artefacts and temporary files
└── README.md          # Project overview and setup instructions
```

## Getting Started

### Backend

The backend is built with [FastAPI](https://fastapi.tiangolo.com/) and exposes a single endpoint for résumé analysis.

1. Navigate to the `backend` folder:

   ```bash
   cd resume_analyzer/backend
   ```

2. Create a virtual environment and activate it (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the development server on `http://localhost:8000`:

   ```bash
   uvicorn app:app --reload --port 8000
   ```

This will run an HTTP API with a single POST endpoint at `/analyze` which accepts a résumé file and job description.  The response contains the extracted keywords, ATS score and suggestions.

### Frontend

The frontend is a minimal React application that lets you upload a résumé and job description, then displays the analysis results.

1. In a separate terminal, navigate to the `frontend` folder:

   ```bash
   cd resume_analyzer/frontend
   ```

2. Install the dependencies with npm:

   ```bash
   npm install
   ```

   

3. Launch the development server:

   ```bash
   npm start
   ```

The React app runs on `http://localhost:3000` and expects the backend to be available on `http://localhost:8000`.  If you are using a different port, update the fetch URL in `src/App.js` accordingly.

## How It Works

1. **Text extraction**: The backend attempts to extract plain text from PDF files using `pdfminer.six` and from DOCX files using `python-docx`.  If the file type isn’t recognized, it treats the contents as plain text.
2. **Keyword extraction**:  A simple heuristic collects predefined skill keywords (for example `python`, `java`, `sql`, etc.) and the most frequent non‑stopwords from the résumé.
3. **ATS score**:  The job description is tokenized, common stopwords are removed and the fraction of unique tokens also present in the résumé text is computed and returned as a percentage.
4. **Suggestions**:  The analysis looks at bullet points (lines starting with `-`, `*` or `•`) and recommends adding quantification when numbers are missing.  General advice is provided when no specific suggestions are found.

## Improving This Project


This starter project is intentionally simple and is intended as a baseline for more advanced résumé analysis tools.  You can improve it by:

- Integrating a proper NLP library such as [spaCy](https://spacy.io/) for part‑of‑speech tagging and named entity recognition.
- Using pre‑trained transformer models from [HuggingFace](https://huggingface.co/) to better identify skills and compute semantic similarity between résumés and job descriptions.
- Implementing more sophisticated ATS scoring metrics that consider keyword weighting, phrase matching and context.
- Expanding the React interface with charts (e.g. pie chart of skill categories) and additional fields such as cover letter analysis.


## License

This project is provided for educational purposes and comes with no warranty.  Feel free to use and modify it under the terms of the MIT License.
