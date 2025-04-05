import React, { useState } from 'react';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [imgSrc, setImgSrc] = useState(null);
  const [loading, setLoading] = useState(false);

  const generateIcon = async () => {
    setLoading(true);
    const response = await fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt }),
    });
    const data = await response.json();
    setImgSrc('data:image/png;base64,' + data.image);
    setLoading(false);
  };

  return (
    <div className="App">
      <h1>Icon Generator</h1>
      <input
        type="text"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter prompt"
      />
      <button onClick={generateIcon} disabled={loading}>
        {loading ? 'Generating...' : 'Generate'}
      </button>
      {imgSrc && (
        <div>
          <h2>Result:</h2>
          <img src={imgSrc} alt="Generated icon" style={{ maxWidth: '256px' }} />
        </div>
      )}
    </div>
  );
}

export default App;
