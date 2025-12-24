"""Authentication service for user registration, login, and session management"""

from datetime import timedelta
from typing import Optional
import logging
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from ..database.models import User, UserBackground
from ..utils.auth import verify_password, get_password_hash, create_access_token
from ..models import SignupRequest, SigninRequest, UserResponse, BackgroundData
from ..config import settings

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self):
        self.access_token_expires = timedelta(days=settings.jwt_expiration_days)

    async def register_user(self, db: AsyncSession, signup_data: SignupRequest):
        """Register a new user with background information"""
        try:
            # Check if user already exists
            result = await db.execute(
                select(User).filter(User.email == signup_data.email)
            )
            existing_user = result.scalar_one_or_none()

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

            # Hash the password
            password_hash = get_password_hash(signup_data.password)

            # Create the user
            user = User(
                email=signup_data.email,
                password_hash=password_hash
            )

            db.add(user)
            await db.flush()  # This ensures the user gets an ID without committing

            # Create user background
            background = UserBackground(
                user_id=user.id,
                software_experience=signup_data.software_experience,
                hardware_experience=signup_data.hardware_experience,
                programming_languages=signup_data.programming_languages,
                robotics_background=signup_data.robotics_background,
                learning_goals=signup_data.learning_goals
            )

            db.add(background)
            await db.commit()
            await db.refresh(user)

            # Create access token
            access_token = create_access_token(
                data={"sub": user.id, "email": user.email},
                expires_delta=self.access_token_expires
            )

            return {
                "user": UserResponse(
                    id=user.id,
                    email=user.email,
                    is_active=user.is_active,
                    created_at=user.created_at
                ),
                "access_token": access_token,
                "token_type": "bearer"
            }

        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        except Exception as e:
            await db.rollback()
            logger.error(f"Error registering user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Registration failed"
            )

    async def authenticate_user(self, db: AsyncSession, signin_data: SigninRequest):
        """Authenticate user credentials and return token"""
        try:
            # Find user by email
            result = await db.execute(
                select(User).filter(User.email == signin_data.email)
            )
            user = result.scalar_one_or_none()

            if not user or not verify_password(signin_data.password, user.password_hash):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect email or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            if not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Inactive user account",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # Create access token
            access_token = create_access_token(
                data={"sub": user.id, "email": user.email},
                expires_delta=self.access_token_expires
            )

            return {
                "user": UserResponse(
                    id=user.id,
                    email=user.email,
                    is_active=user.is_active,
                    created_at=user.created_at
                ),
                "access_token": access_token,
                "token_type": "bearer"
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Authentication failed"
            )

    async def get_current_user(self, db: AsyncSession, user_id: str):
        """Get current user by ID"""
        try:
            result = await db.execute(
                select(User).filter(User.id == user_id)
            )
            user = result.scalar_one_or_none()

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            if not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Inactive user account",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            return UserResponse(
                id=user.id,
                email=user.email,
                is_active=user.is_active,
                created_at=user.created_at
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting current user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve user"
            )

    async def get_user_background(self, db: AsyncSession, user_id: str):
        """Get user background information"""
        try:
            result = await db.execute(
                select(UserBackground).filter(UserBackground.user_id == user_id)
            )
            background = result.scalar_one_or_none()

            if not background:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User background not found"
                )

            return BackgroundData(
                software_experience=background.software_experience,
                hardware_experience=background.hardware_experience,
                programming_languages=background.programming_languages,
                robotics_background=background.robotics_background,
                learning_goals=background.learning_goals
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting user background: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve user background"
            )

    async def update_user_background(self, db: AsyncSession, user_id: str, background_data: BackgroundData):
        """Update user background information"""
        try:
            result = await db.execute(
                select(UserBackground).filter(UserBackground.user_id == user_id)
            )
            existing_background = result.scalar_one_or_none()

            if not existing_background:
                # Create new background if it doesn't exist
                new_background = UserBackground(
                    user_id=user_id,
                    software_experience=background_data.software_experience,
                    hardware_experience=background_data.hardware_experience,
                    programming_languages=background_data.programming_languages,
                    robotics_background=background_data.robotics_background,
                    learning_goals=background_data.learning_goals
                )
                db.add(new_background)
            else:
                # Update existing background
                existing_background.software_experience = background_data.software_experience
                existing_background.hardware_experience = background_data.hardware_experience
                existing_background.programming_languages = background_data.programming_languages
                existing_background.robotics_background = background_data.robotics_background
                existing_background.learning_goals = background_data.learning_goals

            await db.commit()

            if not existing_background:
                await db.refresh(new_background)
                return BackgroundData(
                    software_experience=new_background.software_experience,
                    hardware_experience=new_background.hardware_experience,
                    programming_languages=new_background.programming_languages,
                    robotics_background=new_background.robotics_background,
                    learning_goals=new_background.learning_goals
                )
            else:
                return BackgroundData(
                    software_experience=existing_background.software_experience,
                    hardware_experience=existing_background.hardware_experience,
                    programming_languages=existing_background.programming_languages,
                    robotics_background=existing_background.robotics_background,
                    learning_goals=existing_background.learning_goals
                )

        except Exception as e:
            await db.rollback()
            logger.error(f"Error updating user background: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update user background"
            )