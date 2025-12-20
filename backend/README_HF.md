---
title: RAG Chatbot for Textbook Content
emoji: 📚
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
---

# RAG Chatbot for Textbook Content

This is a RAG (Retrieval-Augmented Generation) chatbot that answers questions from textbook content using Qdrant for vector storage and Google's Gemini 1.5 Flash for responses.

## Setup Instructions

1. Set your environment variables:
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `QDRANT_URL`: Your Qdrant Cloud instance URL
   - `QDRANT_API_KEY`: Your Qdrant API key

2. The application will be available on the port specified by the `PORT` environment variable.

## Features

- Q&A functionality for textbook content
- Text selection and context-aware responses
- Navigation links to relevant textbook sections
- Learning guidance and recommendations
- Session management for conversation continuity

## Architecture

- Backend: FastAPI with uv package manager
- Vector Database: Qdrant Cloud (free tier)
- LLM: Gemini 1.5 Flash via OpenAI Agents SDK
- Embeddings: Qdrant FastEmbed (local, free)

## Note

This application requires external services (Qdrant Cloud and Google Gemini) to function properly. Make sure to configure your API keys in the Space's secrets.