import React, { useState } from 'react';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [imgSrc, setImgSrc] = useState(null);
  const [loading, setLoading] = useState(false);
  const [useCuda, setUseCuda] = useState(false);
  const [resolution, setResolution] = useState('64');
  const [steps, setSteps] = useState('20');
  const [format, setFormat] = useState('jpeg');

  /**
   * Calls the backend to generate an icon image.
   * @returns {Promise<void>}
   */
  const generateIcon = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, use_cuda: useCuda, resolution: parseInt(resolution), steps: parseInt(steps), format }),
      });
      if (!response.ok) {
        throw new Error('API request failed');
      }
      const data = await response.json();
      const mimeType = format === 'jpeg' ? 'jpeg' : 'png';
      setImgSrc(`data:image/${mimeType};base64,${data.image}`);
      
    } catch (error) {
      console.error('Error generating icon:', error);
      setImgSrc(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="HeaderBar">
        <h1>Cool Icon Maker</h1>
      </div>
      <div className="content">
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter prompt"
        />
        <div>
          <label>
            <input
              type="checkbox"
              checked={useCuda}
              onChange={(e) => setUseCuda(e.target.checked)}
            />{' '}
            Enable GPU acceleration
          </label>
        </div>
        <div>
          <label>Resolution (pixels): </label>
          <select value={resolution} onChange={(e) => setResolution(e.target.value)}>
            <option value="64">64x64</option>
            <option value="512">512x512</option>
          </select>
        </div>
        <div>
          <label>Inference steps:</label>
          <select value={steps} onChange={(e) => setSteps(e.target.value)}>
            <option value="20">20</option>
            <option value="50">50</option>
          </select>
        </div>
        <div>
          <label>File format: </label>
          <select value={format} onChange={(e) => setFormat(e.target.value)}>
            <option value="jpeg">JPEG</option>
            <option value="png">PNG</option>
          </select>
        </div>
        <button onClick={generateIcon} disabled={loading} className="blue-button">
          {loading ? 'Generating...' : 'Generate'}
        </button>
        {imgSrc && (
          <div>
            <h2>Result:</h2>
            <img src={imgSrc} alt="Generated icon" style={{ maxWidth: '256px' }} />
            <br />
            <a href={imgSrc} download={`icon.${format}`} className="blue-button download-button">Download Icon</a>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
