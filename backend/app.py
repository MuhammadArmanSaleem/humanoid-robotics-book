# Hugging Face Spaces entry point
# This file allows the API to be run on Hugging Face Spaces

import uvicorn
import os
from src.main import app

if __name__ == "__main__":
    # Use PORT from environment or default to 8000
    port = int(os.environ.get("PORT", 8000))

    # Run with Hugging Face Spaces settings
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=port,
        reload=False  # Disable reload in production
    )