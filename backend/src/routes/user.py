"""User management API routes"""

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils.db import get_db
from ..services.auth_service import AuthService
from ..models import UpdateBackgroundRequest
from ..utils.auth import get_current_user_id

router = APIRouter(prefix="/api/user", tags=["User Management"])

@router.get("/background")
async def get_user_background(
    authorization: str = Header(None),
    db: AsyncSession = Depends(get_db)
):
    """Get current user's background information"""
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

    auth_service = AuthService()
    return await auth_service.get_user_background(db, user_id)


@router.put("/background")
async def update_user_background(
    request: UpdateBackgroundRequest,
    authorization: str = Header(None),
    db: AsyncSession = Depends(get_db)
):
    """Update current user's background information"""
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

    auth_service = AuthService()
    return await auth_service.update_user_background(db, user_id, request.background)