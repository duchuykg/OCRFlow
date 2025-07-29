import React, { useState } from 'react';
import './App.css';

interface ConversionResult {
  success: boolean;
  text: string;
  filename: string;
  error?: string;
}

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<ConversionResult | null>(null);
  const [dragActive, setDragActive] = useState(false);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setResult(null);
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setSelectedFile(e.dataTransfer.files[0]);
      setResult(null);
    }
  };

  const handleConvert = async () => {
    if (!selectedFile) return;

    setIsLoading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('/api/convert', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      setResult({
        success: false,
        text: '',
        filename: '',
        error: 'Network error occurred'
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopyText = () => {
    if (result?.text) {
      navigator.clipboard.writeText(result.text);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>OCR Document Converter</h1>
        <p>Convert documents to text using MarkItDown</p>
      </header>

      <main className="App-main">
        <div className="upload-section">
          <div 
            className={`drop-zone ${dragActive ? 'active' : ''}`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <input
              type="file"
              id="file-input"
              onChange={handleFileSelect}
              accept=".txt,.pdf,.png,.jpg,.jpeg,.gif,.docx,.pptx,.xlsx"
              style={{ display: 'none' }}
            />
            <label htmlFor="file-input" className="file-label">
              {selectedFile ? (
                <div>
                  <p>Selected: {selectedFile.name}</p>
                  <p>Click to select a different file</p>
                </div>
              ) : (
                <div>
                  <p>Drop a file here or click to select</p>
                  <p>Supported: PDF, Images, Word, PowerPoint, Excel</p>
                </div>
              )}
            </label>
          </div>

          {selectedFile && (
            <button 
              onClick={handleConvert} 
              disabled={isLoading}
              className="convert-button"
            >
              {isLoading ? 'Converting...' : 'Convert to Text'}
            </button>
          )}
        </div>

        {result && (
          <div className="result-section">
            {result.success ? (
              <div>
                <div className="result-header">
                  <h3>Conversion Result for: {result.filename}</h3>
                  <button onClick={handleCopyText} className="copy-button">
                    Copy Text
                  </button>
                </div>
                <textarea
                  value={result.text}
                  readOnly
                  className="result-text"
                  rows={20}
                />
              </div>
            ) : (
              <div className="error">
                <h3>Conversion Failed</h3>
                <p>{result.error}</p>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;