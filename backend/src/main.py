from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse
import asyncio
from typing import AsyncGenerator
import html
import logging

from .config import settings
from .models import ChatRequest, Source, IndexContentRequest, IndexContentResponse
from .services.content_service import ContentIndexingService
from .services.rag_service import RAGService
from .services.llm_service import LLMService
from .services.session_service import SessionService
from .services.text_selection_service import TextSelectionService
from .services.auth_service import AuthService
from .services.personalization_service import PersonalizationService
from .middleware.rate_limit import rate_limiter
from .utils.db import init_db
from .routes.auth import router as auth_router
from .routes.user import router as user_router
from .routes.personalization import router as personalization_router
from .routes.content_generation import router as content_generation_router


app = FastAPI(
    title="RAG Chatbot API",
    description="API for RAG-based chatbot that answers questions from textbook content, with content generation workflow integration",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
content_service = ContentIndexingService()
rag_service = RAGService()
llm_service = LLMService()
session_service = SessionService()
text_selection_service = TextSelectionService()
auth_service = AuthService()
personalization_service = PersonalizationService(llm_service)

# Include API routes
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(personalization_router)
app.include_router(content_generation_router)


# Security utility functions
def sanitize_input(user_input: str) -> str:
    """Sanitize user input to prevent XSS and other injection attacks"""
    if not user_input:
        return user_input

    # HTML escape the input
    sanitized = html.escape(user_input)

    # Additional sanitization could be added here
    return sanitized


def validate_query_length(query: str, max_length: int = 1000) -> bool:
    """Validate query length to prevent abuse"""
    return len(query) <= max_length


@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    await init_db()


@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}


@app.middleware("http")
async def add_rate_limiting(request: Request, call_next):
    """Add rate limiting to all requests"""
    if not rate_limiter.is_allowed(request):
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded. Please try again later."}
        )
    response = await call_next(request)
    return response


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    Main chat endpoint with SSE streaming
    """
    try:
        # Sanitize the input
        sanitized_message = sanitize_input(request.message)

        # Validate query length
        if not validate_query_length(sanitized_message):
            raise HTTPException(status_code=400, detail="Query too long")

        # Get or create session
        session_id = request.context.get("session_id")
        if session_id:
            session = session_service.get_session(session_id)
            if not session:
                # Create new session if the provided one is expired
                session = session_service.create_session(request.context.get("current_url"))
        else:
            session = session_service.create_session(request.context.get("current_url"))
            session_id = session.session_id

        # Add user message to session
        from .models import ChatMessage, RoleEnum
        from datetime import datetime
        user_message = ChatMessage(
            id=f"msg_{session_id}_user_{len(session.messages)}",
            role=RoleEnum.user,
            content=sanitized_message,
            timestamp=datetime.now()
        )
        session_service.add_message_to_session(session_id, user_message)

        # Get selected text from context if available
        selected_text = request.context.get("selected_text")

        # Validate selected text if present
        if selected_text:
            # Sanitize selected text too
            sanitized_selected_text = sanitize_input(selected_text)
            if not text_selection_service.validate_selected_text(sanitized_selected_text):
                raise HTTPException(status_code=400, detail="Invalid selected text")

        # Search for relevant content
        relevant_chunks = rag_service.search_content(sanitized_message)

        # Generate response using LLM
        response = await llm_service.generate_response(
            query=sanitized_message,
            context_chunks=relevant_chunks,
            chat_history=session.messages[:-1],  # Exclude the current message
            selected_text=selected_text
        )

        # Add assistant response to session
        assistant_message = ChatMessage(
            id=f"msg_{session_id}_assistant_{len(session.messages)}",
            role=RoleEnum.assistant,
            content=response.content,
            sources=response.sources,
            timestamp=datetime.now()
        )
        session_service.add_message_to_session(session_id, assistant_message)

        # Return the response
        return {
            "type": response.type,
            "content": response.content,
            "sources": [source.dict() for source in response.sources],
            "navigation": response.navigation,
            "session_id": session_id
        }

    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")


@app.post("/api/index-content")
async def index_content(request: IndexContentRequest):
    """
    Endpoint to index textbook content
    """
    try:
        result = content_service.index_content(request.content_chunks)
        return IndexContentResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error indexing content: {str(e)}")


@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    """
    Get a specific session
    """
    session = session_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str):
    """
    Delete a specific session
    """
    session = session_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session_service.delete_session(session_id)
    return {"message": "Session deleted successfully"}


@app.get("/api/chunks/search")
async def search_chunks(query: str, top_k: int = 5):
    """
    Search for content chunks by query
    """
    try:
        chunks = rag_service.search_content(query, top_k=top_k)
        return {"chunks": [chunk.dict() for chunk in chunks]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching chunks: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.uvicorn_host,
        port=settings.uvicorn_port,
        reload=True
    )