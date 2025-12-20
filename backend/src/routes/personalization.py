"""Personalization API routes"""

from fastapi import APIRouter, Depends, HTTPException, status, Header, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils.db import get_db
from ..services.personalization_service import PersonalizationService
from ..services.llm_service import LLMService
from ..utils.auth import get_current_user_id

router = APIRouter(prefix="/api/personalize", tags=["Personalization"])

@router.post("/{content_id}")
async def personalize_content(
    content_id: str,
    original_content: str = Query(..., description="Original content to personalize"),
    authorization: str = Header(None),
    db: AsyncSession = Depends(get_db)
):
    """Get personalized content for authenticated user"""
    # Extract token from Authorization header
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]

    if not token:
        # If not authenticated, return original content
        return {"personalized_content": original_content}

    user_id = get_current_user_id(token)
    if not user_id:
        # If invalid token, return original content
        return {"personalized_content": original_content}

    # Initialize services
    llm_service = LLMService()
    personalization_service = PersonalizationService(llm_service)

    personalized_content = await personalization_service.get_personalized_content(
        db, user_id, content_id, original_content
    )

    return {
        "content_id": content_id,
        "personalized_content": personalized_content,
        "user_specific": True
    }


@router.get("/learning-path")
async def get_learning_path(
    topic: str = Query(None, description="Specific topic for learning path"),
    authorization: str = Header(None),
    db: AsyncSession = Depends(get_db)
):
    """Get personalized learning path for authenticated user"""
    # Extract token from Authorization header
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = get_current_user_id(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Initialize services
    llm_service = LLMService()
    personalization_service = PersonalizationService(llm_service)

    learning_path = await personalization_service.get_learning_path(db, user_id, topic)

    return learning_path