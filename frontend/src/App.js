import React, { useState } from 'react';

/**
 * Main application component for the Smart Resume Analyzer.
 *
 * Renders a form to upload a résumé and provide a job description.  After
 * submitting the form, it sends the data to the backend and displays the
 * keywords, ATS score and suggestions returned by the API.
 */
function App() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  /**
   * Handle file selection.
   */
  const handleFileChange = (event) => {
    const selected = event.target.files[0];
    setFile(selected);
  };

  /**
   * Submit the form to the backend API.
   */
  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      setError('Please select a résumé file.');
      return;
    }
    setError(null);
    setLoading(true);
    setAnalysis(null);
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('job_description', jobDescription);

      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) {
        throw new Error('Server error');
      }
      const data = await response.json();
      setAnalysis(data);
    } catch (err) {
      setError('An error occurred while analysing the résumé.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '700px', margin: '0 auto', padding: '1rem' }}>
      <h1>Smart Resume Analyzer</h1>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '1rem' }}>
          <label>
            Upload résumé (PDF/DOCX):
            <input
              type="file"
              accept=".pdf,.docx,.txt"
              onChange={handleFileChange}
              style={{ display: 'block', marginTop: '0.5rem' }}
            />
          </label>
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label>
            Job Description:
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              rows={6}
              style={{ width: '100%', marginTop: '0.5rem' }}
              placeholder="Paste the job description here..."
            />
          </label>
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
      </form>
      {error && <p style={{ color: 'red', marginTop: '1rem' }}>{error}</p>}
      {analysis && (
        <div style={{ marginTop: '2rem' }}>
          <h2>Results</h2>
          <p>
            <strong>ATS Score:</strong> {analysis.ats_score}%
          </p>
          <h3>Keywords</h3>
          <ul>
            {analysis.keywords.map((kw, idx) => (
              <li key={idx}>{kw}</li>
            ))}
          </ul>
          <h3>Suggestions</h3>
          <ul>
            {analysis.suggestions.map((sg, idx) => (
              <li key={idx}>{sg}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;