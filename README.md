# SIH26117 – Sovereign On-Premise Agentic AI Workbench

**Motto:** Sovereign AI for Confidential Work — Nothing Leaves the Premises

## Project Overview

This project is a fully offline, air-gapped AI workbench designed for confidential industrial work (especially for organizations like MRPL - Mangalore Refinery and Petrochemicals Limited).

It allows users to upload scanned inspection reports or documents and automatically generates a formal **Inspection Observation / Approval Note** in Word format using local open-weight models.

**Key Feature (Current Focus):**
Scanned Document (PDF/Image) → OCR → Local LLM → Generate Word Approval Note

## Features

- Fully offline (no external API calls)
- Works with scanned PDFs and images
- Uses local open-weight model (Qwen2.5-7B via Ollama)
- Generates professional Word documents
- Clean Gradio-based graphical interface
- Designed for confidential industrial environments

## Tech Stack

- **LLM Runtime:** Ollama
- **Model:** qwen2.5:7b
- **OCR:** Tesseract
- **Document Generation:** python-docx
- **Interface:** Gradio
- **Language:** Python

## How to Run

### 1. Prerequisites
- Python 3.10+
- Ollama installed ([https://ollama.com](https://ollama.com))
- Tesseract OCR installed

### 2. Setup

```bash
# Clone the repository
git clone https://github.com/susesh10/SIH-26117.git
cd SIH-26117

# Create virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Pull the model
ollama pull qwen2.5:7b

#project structure
SIH-26117/
├── app/
│   ├── tools/
│   │   ├── ocr.py
│   │   └── document.py
│   └── ui.py
├── scripts/
│   ├── run_pipeline.py
│   └── test_model.py
├── data/sample_docs/
├── outputs/
└── requirements.txt