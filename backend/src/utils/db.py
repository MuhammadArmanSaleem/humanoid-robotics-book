"""Database utilities and connection setup"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from psycopg2.extensions import register_adapter, AsIs
import numpy as np
from typing import List
import asyncio
from ..database.models import Base
from ..config import settings

# Create sync engine (using psycopg2) instead of async engine to avoid driver issues
from sqlalchemy import create_engine
engine = create_engine(
    settings.database_url,
    echo=False,  # Set to True for SQL debugging
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

# Create sync session maker
from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(
    engine,
    expire_on_commit=False
)

# For compatibility with async code, create async session maker that wraps sync
from sqlalchemy.ext.asyncio import async_sessionmaker
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False
)

# PostgreSQL array adapter for proper list handling
def adapt_list(lst):
    return AsIs(f"ARRAY[{','.join(repr(item) for item in lst)}]")

register_adapter(list, adapt_list)

async def get_db():
    """Dependency to get database session"""
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    """Initialize database tables"""
    # For sync engine, use regular with statement
    with engine.begin() as conn:
        Base.metadata.create_all(conn)

async def test_connection():
    """Test database connection"""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT 1"))
            return result.scalar() == 1
    except Exception as e:
        print(f"Database connection test failed: {e}")
        return False

# Additional utility functions for user operations
async def create_user_tables():
    """Create all user-related tables if they don't exist"""
    async with engine.begin() as conn:
        # Create all tables defined in models
        await conn.run_sync(Base.metadata.create_all)