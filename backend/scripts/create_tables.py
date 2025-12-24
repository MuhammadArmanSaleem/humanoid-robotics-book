#!/usr/bin/env python3
"""
Database initialization script to create all required tables
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the path so we can import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.db import engine
from src.database.models import Base


async def create_tables():
    """Create all database tables"""
    print("Creating database tables...")

    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)

    print("Database tables created successfully!")


if __name__ == "__main__":
    asyncio.run(create_tables())