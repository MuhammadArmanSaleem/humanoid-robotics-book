# RAG Chatbot Deployment Guide

This guide provides instructions for deploying the RAG Chatbot API using multiple platforms.

## Prerequisites

Before deploying, you need the following:

- **Qdrant Cloud Account**: Sign up at [qdrant.tech](https://qdrant.tech) for a free tier account
- **Google Gemini API Key**: Get an API key from [Google AI Studio](https://aistudio.google.com)
- **Environment Variables**:
  - `GEMINI_API_KEY`: Your Google Gemini API key
  - `QDRANT_URL`: Your Qdrant Cloud instance URL
  - `QDRANT_API_KEY`: Your Qdrant API key
  - `FRONTEND_URL`: URL of your Docusaurus textbook (default: http://localhost:3000)

## Deployment Options

### 1. Docker Deployment

#### Build and Run Locally

```bash
# Navigate to the api directory
cd api/

# Build the Docker image
docker build -t rag-chatbot-api .

# Run the container
docker run -d \
  --name rag-chatbot \
  -p 8000:8000 \
  -e GEMINI_API_KEY=your_gemini_key \
  -e QDRANT_URL=your_qdrant_url \
  -e QDRANT_API_KEY=your_qdrant_key \
  -e FRONTEND_URL=http://your-frontend-url \
  rag-chatbot-api
```

#### Using Docker Compose

```bash
# Create a .env file with your environment variables
cp .env.example .env
# Edit .env with your values

# Start the service
docker-compose up -d
```

### 2. Render Deployment

1. Push your code to a GitHub repository
2. Create a new Web Service on [Render](https://render.com)
3. Connect to your GitHub repository
4. Configure the build and start commands:
   - **Build Command**: `pip install uv && uv sync`
   - **Start Command**: `uv run uvicorn src.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables in the Render dashboard:
   - `GEMINI_API_KEY`
   - `QDRANT_URL`
   - `QDRANT_API_KEY`
   - `FRONTEND_URL`
6. Deploy!

### 3. Railway Deployment

1. Install Railway CLI or use the web interface
2. Create a new project and connect to your GitHub repository
3. Railway will automatically detect the `railway.json` configuration
4. Add environment variables in the Railway dashboard:
   - `GEMINI_API_KEY`
   - `QDRANT_URL`
   - `QDRANT_API_KEY`
   - `FRONTEND_URL`
5. Deploy using the provided Procfile

### 4. Hugging Face Spaces Deployment

1. Create a new Space on [Hugging Face](https://huggingface.co/spaces)
2. Choose Docker as the SDK
3. Upload your code or connect to a Git repository
4. Add the following secrets:
   - `GEMINI_API_KEY`
   - `QDRANT_URL`
   - `QDRANT_API_KEY`
5. The Space will use the `app.py` and `requirements.txt` files

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes | Google Gemini API key |
| `QDRANT_URL` | Yes | Qdrant Cloud instance URL |
| `QDRANT_API_KEY` | Yes | Qdrant API key |
| `FRONTEND_URL` | No | Frontend URL for CORS (default: http://localhost:3000) |
| `UVICORN_HOST` | No | Host to bind to (default: 0.0.0.0) |
| `UVICORN_PORT` | No | Port to bind to (default: 8000) |
| `SESSION_TIMEOUT_HOURS` | No | Session timeout in hours (default: 24) |

## Configuration Options

The application can be configured through environment variables or by modifying the `src/config.py` file:

- `session_timeout_hours`: How long before sessions expire (default: 24)
- `content_chunk_size`: Size of content chunks in words (default: 500)
- `content_overlap_size`: Overlap between chunks (default: 50)
- `rag_top_k`: Number of results to return from RAG (default: 5)
- `rag_min_relevance_score`: Minimum relevance for results (default: 0.3)

## Health Checks

The application provides a health check endpoint:
- `GET /api/health` - Returns health status

## Troubleshooting

### Common Issues

1. **Connection to Qdrant fails**:
   - Verify `QDRANT_URL` and `QDRANT_API_KEY` are correct
   - Check that your Qdrant Cloud instance is running

2. **Gemini API errors**:
   - Verify `GEMINI_API_KEY` is valid
   - Check that your Gemini API quota hasn't been exceeded

3. **CORS errors**:
   - Ensure `FRONTEND_URL` matches your Docusaurus deployment URL

4. **Rate limiting**:
   - The app has built-in rate limiting (60 requests per minute per IP)
   - Adjust in `src/middleware/rate_limit.py` if needed

### Logs

Check application logs for errors:
```bash
# Docker
docker logs rag-chatbot

# Render/Railway - Check the dashboard logs
```

## Scaling

For production use:
- Use Redis for session storage instead of in-memory
- Implement proper load balancing
- Set up monitoring and alerting
- Use CDN for static assets
- Implement caching layers where appropriate

## Security

- Never commit API keys to version control
- Use environment variables or secrets management
- Enable HTTPS in production
- Regularly rotate API keys
- Monitor for unusual API usage patterns