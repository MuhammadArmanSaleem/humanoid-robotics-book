"""Personalization service for adapting content based on user background"""

import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from fastapi import HTTPException, status
from ..database.models import User, UserBackground, PersonalizedContent
from ..models import BackgroundData
from ..services.llm_service import LLMService
from ..config import settings

logger = logging.getLogger(__name__)

class PersonalizationService:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    async def get_personalized_content(self, db: AsyncSession, user_id: str, content_id: str, original_content: str):
        """Get personalized content for a user, generating if not cached"""
        try:
            # First, try to get cached personalized content
            result = await db.execute(
                select(PersonalizedContent)
                .filter(
                    and_(
                        PersonalizedContent.user_id == user_id,
                        PersonalizedContent.content_id == content_id
                    )
                )
            )
            cached_content = result.scalar_one_or_none()

            if cached_content:
                return cached_content.personalized_content

            # If not cached, get user background to personalize content
            user_result = await db.execute(
                select(UserBackground).filter(UserBackground.user_id == user_id)
            )
            user_background = user_result.scalar_one_or_none()

            if not user_background:
                # If no background, return original content
                return original_content

            # Generate personalized content using LLM
            personalized_content = await self._generate_personalized_content(
                original_content,
                user_background,
                content_id
            )

            # Cache the personalized content
            new_personalized = PersonalizedContent(
                user_id=user_id,
                content_id=content_id,
                personalized_content=personalized_content,
                personalization_rules={
                    "software_experience": user_background.software_experience,
                    "hardware_experience": user_background.hardware_experience,
                    "programming_languages": user_background.programming_languages,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            db.add(new_personalized)
            await db.commit()

            return personalized_content

        except Exception as e:
            logger.error(f"Error getting personalized content: {e}")
            # Return original content if personalization fails
            return original_content

    async def _generate_personalized_content(self, original_content: str, user_background: UserBackground, content_id: str):
        """Generate personalized content using LLM based on user background"""
        try:
            # Create a prompt that incorporates user background for personalization
            background_context = f"""
            User Background:
            - Software Experience: {user_background.software_experience}
            - Hardware Experience: {user_background.hardware_experience}
            - Programming Languages: {', '.join(user_background.programming_languages)}
            - Robotics Background: {user_background.robotics_background or 'None provided'}
            - Learning Goals: {user_background.learning_goals or 'None provided'}
            """

            # Create a detailed prompt for content personalization
            system_prompt = f"""
            You are an AI tutor specializing in Physical AI & Humanoid Robotics education.
            Your task is to adapt educational content to match the student's background and learning needs.

            {background_context}

            Guidelines for personalization:
            1. Adjust complexity based on experience levels (beginner/intermediate/advanced)
            2. Use programming examples in the student's preferred languages when applicable
            3. Include relevant analogies based on their background
            4. Provide additional explanations for concepts that might be challenging given their background
            5. Maintain the core educational value and accuracy of the content
            6. Keep the same structure and key points, just adapt the presentation

            Original content:
            """

            user_prompt = original_content

            # Use the LLM service to generate personalized content
            response = await self.llm_service.generate_response(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                context=None  # No additional context needed
            )

            return response

        except Exception as e:
            logger.error(f"Error generating personalized content: {e}")
            # Return original content if LLM generation fails
            return original_content

    async def get_learning_path(self, db: AsyncSession, user_id: str, topic: str = None):
        """Generate a personalized learning path based on user background"""
        try:
            # Get user background
            user_result = await db.execute(
                select(UserBackground).filter(UserBackground.user_id == user_id)
            )
            user_background = user_result.scalar_one_or_none()

            if not user_background:
                # Return a default learning path if no background
                return self._get_default_learning_path(topic)

            # Create a prompt for learning path generation
            background_context = f"""
            User Background:
            - Software Experience: {user_background.software_experience}
            - Hardware Experience: {user_background.hardware_experience}
            - Programming Languages: {', '.join(user_background.programming_languages)}
            - Robotics Background: {user_background.robotics_background or 'None provided'}
            - Learning Goals: {user_background.learning_goals or 'None provided'}
            """

            system_prompt = f"""
            You are an AI tutor specializing in Physical AI & Humanoid Robotics education.
            Generate a personalized learning path based on the user's background.

            {background_context}

            Consider:
            1. Start with concepts appropriate for their experience level
            2. Include topics that align with their learning goals
            3. Consider their programming language preferences
            4. Account for any gaps in their background that should be addressed first
            5. Provide a structured path with prerequisites

            If a specific topic is requested, focus the path on that topic while still considering their background.
            """

            user_prompt = f"Generate a personalized learning path for Physical AI & Humanoid Robotics. The user wants to focus on: {topic or 'general robotics concepts'}"

            # Generate learning path using LLM
            response = await self.llm_service.generate_response(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                context=None
            )

            return {
                "path_description": response,
                "generated_at": datetime.utcnow().isoformat(),
                "user_background_considered": {
                    "software_experience": user_background.software_experience,
                    "hardware_experience": user_background.hardware_experience,
                    "programming_languages": user_background.programming_languages
                }
            }

        except Exception as e:
            logger.error(f"Error generating learning path: {e}")
            return self._get_default_learning_path(topic)

    def _get_default_learning_path(self, topic: str = None):
        """Return a default learning path when personalization isn't possible"""
        return {
            "path_description": f"A general learning path for {topic or 'Physical AI & Humanoid Robotics'} starting with fundamentals and progressing to advanced concepts.",
            "generated_at": datetime.utcnow().isoformat(),
            "user_background_considered": None
        }

    async def update_personalization_cache(self, db: AsyncSession, user_id: str, content_id: str, new_content: str):
        """Update the cached personalized content"""
        try:
            # Check if there's already cached content for this user and content ID
            result = await db.execute(
                select(PersonalizedContent)
                .filter(
                    and_(
                        PersonalizedContent.user_id == user_id,
                        PersonalizedContent.content_id == content_id
                    )
                )
            )
            existing_cache = result.scalar_one_or_none()

            if existing_cache:
                # Update existing cache
                existing_cache.personalized_content = new_content
                existing_cache.updated_at = datetime.utcnow()
            else:
                # Create new cache entry
                new_cache = PersonalizedContent(
                    user_id=user_id,
                    content_id=content_id,
                    personalized_content=new_content,
                    personalization_rules={"updated_manually": True}
                )
                db.add(new_cache)

            await db.commit()

        except Exception as e:
            logger.error(f"Error updating personalization cache: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update personalization cache"
            )