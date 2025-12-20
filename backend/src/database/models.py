"""Database models for authentication and personalization"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ARRAY, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to user background
    background = relationship("UserBackground", back_populates="user", uselist=False, cascade="all, delete-orphan")
    progress = relationship("UserProgress", back_populates="user", cascade="all, delete-orphan")
    personalized_content = relationship("PersonalizedContent", back_populates="user", cascade="all, delete-orphan")

class UserBackground(Base):
    __tablename__ = "user_background"

    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    software_experience = Column(String, nullable=False)  # beginner, intermediate, advanced
    hardware_experience = Column(String, nullable=False)  # beginner, intermediate, advanced
    programming_languages = Column(ARRAY(String), nullable=False)  # e.g., ['Python', 'C++', 'JavaScript']
    robotics_background = Column(Text)  # optional text field
    learning_goals = Column(Text)  # optional text field
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship back to user
    user = relationship("User", back_populates="background")

class PersonalizedContent(Base):
    __tablename__ = "personalized_content"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    content_id = Column(String, nullable=False, index=True)  # reference to original content
    personalized_content = Column(Text, nullable=False)  # AI-generated personalized version
    personalization_rules = Column(JSON)  # rules used for personalization
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to user
    user = relationship("User", back_populates="personalized_content")

class UserProgress(Base):
    __tablename__ = "user_progress"

    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    content_id = Column(String, primary_key=True)  # reference to content
    progress_percentage = Column(Integer, default=0)  # 0-100
    time_spent = Column(Integer, default=0)  # seconds
    completed_at = Column(DateTime(timezone=True))  # nullable
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to user
    user = relationship("User", back_populates="progress")