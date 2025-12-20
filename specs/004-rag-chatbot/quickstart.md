# RAG Chatbot Quickstart Guide

## Overview
This guide provides quick setup instructions for the RAG-based chatbot that answers questions from textbook content. The system uses Qdrant for vector storage, Gemini 1.5 Flash for responses, and integrates with Docusaurus textbook.

## Prerequisites
- Python 3.11+
- uv package manager
- Qdrant Cloud account (free tier)
- Google Gemini API key (free tier)
- Node.js for Docusaurus integration

## Local Development Setup

### 1. Clone and Initialize
```bash
# Clone the repository
git clone <your-repo-url>
cd <your-repo-name>

# Navigate to the API directory (create if doesn't exist)
mkdir -p api
cd api
```

### 2. Create Virtual Environment and Install Dependencies
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install uv if not already installed
pip install uv

# Create pyproject.toml with dependencies
uv init
uv add fastapi uvicorn python-dotenv qdrant-client fastembed agents sse-starlette
```

### 3. Environment Configuration
Create `.env` file in the api directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
FRONTEND_URL=http://localhost:3000
UVICORN_HOST=0.0.0.0
UVICORN_PORT=8000
```

Create `.env.example` file:
```env
GEMINI_API_KEY=
QDRANT_URL=
QDRANT_API_KEY=
FRONTEND_URL=http://localhost:3000
UVICORN_HOST=0.0.0.0
UVICORN_PORT=8000
```

### 4. Basic Application Structure
Create the main application file `main.py`:
```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import asyncio
from sse_starlette.sse import EventSourceResponse

app = FastAPI(title="RAG Chatbot API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = {}

class Source(BaseModel):
    url: str
    title: str
    chapter: str
    lesson: str
    relevance: float

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.post("/api/chat")
async def chat(request: ChatRequest):
    # Implementation will go here
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

### 5. Run the Application
```bash
# Start the development server
uvicorn main:app --reload
```

## Content Indexing
To index textbook content for RAG:

1. Prepare content chunks in the format specified in the API contract
2. Call the `/api/index-content` endpoint with your content
3. Verify content is properly embedded and stored in Qdrant

## Docusaurus Integration
1. Create a React component for the chat widget
2. Use Docusaurus Root swizzling to inject globally
3. The widget will appear as a floating button on all textbook pages

## Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key
- `QDRANT_URL`: URL to your Qdrant Cloud instance
- `QDRANT_API_KEY`: API key for Qdrant Cloud
- `FRONTEND_URL`: URL of your Docusaurus textbook (for CORS)

## API Endpoints
- `POST /api/chat`: Main chat endpoint with SSE streaming
- `GET /api/health`: Health check
- `POST /api/index-content`: Content indexing

## Testing the API
```bash
# Test health endpoint
curl http://localhost:8000/api/health

# Test chat endpoint (example)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Physical AI?"}'
```

## Next Steps
1. Implement the RAG service with Qdrant and Gemini integration
2. Add text selection and navigation features
3. Complete the Docusaurus integration
4. Set up proper deployment configuration