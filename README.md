# Simple Stable Diffusion Icon Generator

An MVP app to generate colorful app icons using Stable Diffusion with LoRA fine-tuning.

---

## Features
- Minimal React frontend
- FastAPI backend with Stable Diffusion + LoRA
- Prompts enhanced to produce icon-style images automatically
- Generates 512x512 colorful icons

---

## Requirements
- Python 3.8+
- Node.js (for rebuilding frontend)
- (Optionally) CUDA-capable GPU recommended for performance

---

## Installation

1. Clone this repository

2. Setup Python virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt  # (create this based on your env)
```

3. Install JS dependencies:

```bash
cd frontend
npm install
npm run build
```

---

## Usage

Simply run:

```bash
start.bat
```

This will start the FastAPI server and serve the React frontend at:

[http://127.0.0.1:8088](http://127.0.0.1:8088)

---

## Updating or Rebuilding Frontend

```
cd frontend
npm run build
```

---

## Model & LoRA

Make sure these files are in the root directory:

- `LiberteRedmond.safetensors`
- `IconsRedmond15V-Icons.safetensors`

---

## License

MIT License or specify your own.
