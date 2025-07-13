import React, { useState } from 'react';

const App: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setError(null);
    setPdfUrl(null);
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setPdfUrl(null);
    if (!file) {
      setError('Please select a PDF file.');
      return;
    }
    if (file.type !== 'application/pdf') {
      setError('Only PDF files are supported.');
      return;
    }
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    try {
      const response = await fetch('/api/redact_pdf', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) {
        throw new Error('Redaction failed.');
      }
      const blob = await response.blob();
      setPdfUrl(URL.createObjectURL(blob));
    } catch (err: any) {
      setError(err.message || 'Something went wrong.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 500, margin: '2rem auto', padding: '2rem', boxShadow: '0 4px 24px #eee', borderRadius: 8 }}>
      <h2>OpenRedact PDF Redactor</h2>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="application/pdf" onChange={handleFileChange} />
        <button type="submit" disabled={loading || !file} style={{ marginLeft: 8 }}>
          {loading ? 'Redacting...' : 'Redact PDF'}
        </button>
      </form>
      {error && <div style={{ color: 'red', marginTop: 16 }}>{error}</div>}
      {pdfUrl && (
        <div style={{ marginTop: 24 }}>
          <a href={pdfUrl} download="redacted.pdf">Download Redacted PDF</a>
          <iframe src={pdfUrl} title="Redacted PDF" width="100%" height="400px" style={{ marginTop: 12, border: '1px solid #ccc' }} />
        </div>
      )}
    </div>
  );
};

export default App;
