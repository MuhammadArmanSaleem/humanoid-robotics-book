# Backend Run Guide

Complete guide to running the FastAPI backend server for the RAG Chatbot and Workflow Integration.

## Prerequisites

- **Python 3.11+** installed
- **uv** package manager (recommended) or **pip**
- Environment variables configured (see below)

## Quick Start

### Option 1: Using uv (Recommended)

```bash
cd backend
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Option 2: Using Python directly

```bash
cd backend
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Option 3: Using pip and virtual environment

```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

## Environment Variables

Create a `.env.local` file in the `backend/` directory with the following variables:

```env
# Required: Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

# Required: Qdrant Vector Database
QDRANT_URL=https://your-qdrant-instance.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=textbook_content

# Required: Database (PostgreSQL/Neon)
DATABASE_URL=postgresql://user:password@host:port/database

# Required: JWT Secret
JWT_SECRET_KEY=your_secret_key_here_min_32_chars

# Optional: Server Configuration
UVICORN_HOST=0.0.0.0
UVICORN_PORT=8000

# Optional: Frontend URL
FRONTEND_URL=http://localhost:3000

# Optional: Auth0 (for SSO integration)
AUTH0_DOMAIN=
AUTH0_CLIENT_ID=
AUTH0_CLIENT_SECRET=
AUTH0_AUDIENCE=
```

### Getting API Keys

1. **Gemini API Key**: 
   - Visit https://makersuite.google.com/app/apikey
   - Create a new API key
   - Copy and paste into `GEMINI_API_KEY`

2. **Qdrant Cloud**:
   - Sign up at https://cloud.qdrant.io
   - Create a free cluster
   - Get URL and API key from cluster settings
   - Add to `QDRANT_URL` and `QDRANT_API_KEY`

3. **Database (Neon PostgreSQL)**:
   - Sign up at https://neon.tech
   - Create a new project
   - Copy connection string to `DATABASE_URL`

4. **JWT Secret Key**:
   - Generate a random 32+ character string
   - Example: `openssl rand -hex 32`

## Installation Steps

### Step 1: Install Dependencies

**Using uv (recommended):**
```bash
cd backend
uv sync
```

**Using pip:**
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Set Up Environment Variables

Create `.env.local` file (see Environment Variables section above).

### Step 3: Initialize Database (if needed)

```bash
cd backend
python scripts/create_tables.py
```

### Step 4: Run the Server

```bash
# Development mode (with auto-reload)
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# Production mode (no reload)
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## Verify Backend is Running

1. **Health Check**: 
   ```bash
   curl http://localhost:8000/api/health
   ```
   Expected response: `{"status":"healthy","version":"1.0.0"}`

2. **API Documentation**:
   - Open http://localhost:8000/docs in your browser
   - You should see the Swagger UI with all API endpoints

3. **Alternative Docs**:
   - Open http://localhost:8000/redoc for ReDoc interface

## Available Endpoints

Once running, the backend provides:

- **Health Check**: `GET /api/health`
- **Chat API**: `POST /api/chat`
- **Content Generation**: `POST /api/content/generate`
- **Job Status**: `GET /api/content/generate/{job_id}`
- **Cancel Job**: `POST /api/content/generate/{job_id}/cancel`
- **Index Content**: `POST /api/index-content`
- **Authentication**: `POST /api/auth/signup`, `POST /api/auth/signin`
- **User Profile**: `GET /api/user/profile`
- **Personalization**: `POST /api/personalization/update`

## Troubleshooting

### Port Already in Use

If port 8000 is already in use:

```bash
# Use a different port
uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
```

Or find and kill the process using port 8000:

**Windows:**
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**macOS/Linux:**
```bash
lsof -ti:8000 | xargs kill -9
```

### Missing Environment Variables

If you see errors about missing environment variables:

1. Check that `.env.local` exists in `backend/` directory
2. Verify all required variables are set (see Environment Variables section)
3. Restart the server after adding variables

### Database Connection Errors

If you see database connection errors:

1. Verify `DATABASE_URL` is correct
2. Check that the database server is accessible
3. Ensure database tables are created: `python scripts/create_tables.py`

### Module Import Errors

If you see import errors:

1. Make sure you're in the `backend/` directory
2. Verify dependencies are installed: `uv sync` or `pip install -r requirements.txt`
3. Check Python version: `python --version` (should be 3.11+)

## Development Tips

### Auto-reload on Code Changes

The `--reload` flag enables auto-reload when code changes:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Running in Background

**Windows PowerShell:**
```powershell
Start-Process -NoNewWindow python -ArgumentList "-m","uvicorn","src.main:app","--host","0.0.0.0","--port","8000"
```

**macOS/Linux:**
```bash
nohup uvicorn src.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
```

### Viewing Logs

Logs are printed to the console. For production, consider redirecting to a file:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1
```

## Production Deployment

For production, use:

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Or use the Procfile (for platforms like Heroku/Railway):
```
web: uv run uvicorn src.main:app --host 0.0.0.0 --port $PORT
```

## Next Steps

1. ✅ Backend running on http://localhost:8000
2. ✅ Test health endpoint: http://localhost:8000/api/health
3. ✅ View API docs: http://localhost:8000/docs
4. ✅ Start frontend: `npm start` (from project root)
5. ✅ Test complete workflow

## Support

For issues or questions:
- Check the API documentation at `/docs`
- Review error logs in the console
- Verify all environment variables are set correctly


