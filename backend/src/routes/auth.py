"""Authentication API routes"""

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils.db import get_db
from ..services.auth_service import AuthService
from ..models import SignupRequest, SigninRequest, AuthResponse, UpdateBackgroundRequest
from ..utils.auth import verify_token, get_current_user_id
from typing import Optional

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/signup", response_model=AuthResponse)
async def signup(
    signup_data: SignupRequest,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user"""
    auth_service = AuthService()
    return await auth_service.register_user(db, signup_data)


@router.post("/signin", response_model=AuthResponse)
async def signin(
    signin_data: SigninRequest,
    db: AsyncSession = Depends(get_db)
):
    """Authenticate user and return token"""
    auth_service = AuthService()
    return await auth_service.authenticate_user(db, signin_data)


@router.post("/signout")
async def signout():
    """Sign out user (client-side token removal is sufficient)"""
    return {"message": "Successfully signed out"}


@router.get("/me")
async def get_current_user(
    authorization: str = Header(None),
    db: AsyncSession = Depends(get_db)
):
    """Get current authenticated user"""
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
    return await auth_service.get_current_user(db, user_id)