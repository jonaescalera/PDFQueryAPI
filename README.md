# PDF Q&A System with LLMs

A FastAPI application that allows users to upload PDF documents and ask questions about their content using Large Language Models.

## Features

- **PDF Processing**: Extract text from any PDF document
- **Question Answering**: Ask natural language questions about the PDF content
- **Summarization**: Automatically generate summaries of document content
- **Dual Implementation**: Supports both local LLM inference and API-based models
- **Easy Switching**: Simple configuration to toggle between local and cloud models

## Technologies

- **FastAPI**: High-performance API framework
- **Llama-2**: State-of-the-art language model for text generation
- **pdfplumber**: PDF text extraction
- **PyTorch**: Deep learning framework (local mode)
- **UUID**: Unique identifier generation for document tracking

## Getting Started

### Prerequisites

- Python 3.9+
- Virtual environment (recommended)

### Installation

```bash
# Clone the repository
git clone https://github.com/jonaescalera/llama2-pdf-qa.git
cd llama2-pdf-qa

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt