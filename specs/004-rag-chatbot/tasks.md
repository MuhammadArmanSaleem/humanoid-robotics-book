# RAG Chatbot Implementation Tasks

## Phase 0: Setup & Prerequisites (10 tasks)

- [X] **T001** Create api/ directory structure with src/, scripts/, tests/ subdirectories
- [X] **T002** Initialize Python project in api/ with uv package manager and create pyproject.toml
- [X] **T003** Create .env.example file with GEMINI_API_KEY, QDRANT_URL, QDRANT_API_KEY, FRONTEND_URL variables
- [X] **T004** Create .env file (for user to manually paste credentials) with same variables as .env.example
- [X] **T005** Install dependencies: fastapi, uvicorn, python-dotenv, qdrant-client, fastembed, agents, sse-starlette, pydantic
- [X] **T006** Create basic FastAPI app structure in api/src/main.py with basic imports
- [X] **T007** Create Pydantic settings model for configuration in api/src/config.py
- [ ] **T008** Test Qdrant connection using provided Qdrant connection code from user
- [ ] **T009** Test Gemini API connection via OpenAI Agents SDK with provided API key
- [ ] **T010** Verify all dependencies install correctly and basic app runs without errors

## Phase 1: Configuration & Models (4 tasks)

- [X] **T011** Create Pydantic models for configuration (Settings) with Qdrant and Gemini settings
- [X] **T012** Create request/response schemas: ChatRequest, Source, ChatResponse, ContentChunk
- [X] **T013** Create Pydantic models for entities: ContentChunk, ChatMessage, ChatSession
- [X] **T014** Set up proper validation rules for all models based on data-model.md

## Phase 2: Backend Services (18 tasks)

- [X] **T015** [P] Create ContentIndexingService with FastEmbed initialization (BAAI/bge-small-en-v1.5)
- [X] **T016** [P] Implement content chunking strategy (200-500 words with metadata preservation)
- [ ] **T017** [P] Test embedding generation with sample content and verify 384-dimensional vectors
- [X] **T018** [P] Create RAGService with Qdrant vector search functionality
- [X] **T019** [P] Implement similarity search with top-5 chunk retrieval
- [X] **T020** [P] Add metadata filtering (chapter, lesson, section) to vector search
- [X] **T021** [P] Create LLMService with Gemini 1.5 Flash via OpenAI Agents SDK
- [X] **T022** [P] Implement custom provider for Gemini with OpenAI Agents SDK
- [ ] **T023** [P] Test LLM service with sample queries and verify response format
- [X] **T024** [P] Create ContentService for managing content chunks in Qdrant
- [X] **T025** [P] Implement content indexing with URL, chapter, lesson metadata
- [X] **T026** [P] Add embedding generation and storage to ContentService
- [X] **T027** [P] Create SessionService for managing chat sessions (24-hour expiration)
- [X] **T028** [P] Implement session persistence with in-memory storage
- [X] **T029** [P] Add session cleanup for expired sessions
- [X] **T030** [P] Create TextSelectionService for handling selected text context
- [X] **T031** [P] Integrate selected text context into RAG pipeline
- [ ] **T032** [P] Test end-to-end RAG pipeline with sample content and queries

## Phase 3: API Endpoints (8 tasks)

- [X] **T033** Create FastAPI app with CORS middleware configuration
- [X] **T034** Implement POST /api/chat endpoint with request/response validation
- [X] **T035** Add Server-Sent Events (SSE) streaming to chat endpoint
- [X] **T036** Implement proper error handling and response formatting for SSE
- [X] **T037** Add source citation generation to chat responses
- [X] **T038** Implement navigation link generation in responses
- [X] **T039** Create GET /api/health endpoint with dependency health checks
- [X] **T040** Create POST /api/index-content endpoint for content ingestion

## Phase 4: US1 - Core Q&A (19 tasks) - P0

- [X] **T041** [P] Create ChatWidget React component with floating button UI
- [X] **T042** [P] Implement message list display with markdown rendering support
- [X] **T043** [P] Add loading states and visual feedback during query processing
- [X] **T044** [P] Create API service for frontend to communicate with backend
- [X] **T045** [P] Implement chat session management in frontend
- [X] **T046** [P] Add session persistence across page navigation
- [X] **T047** [P] Integrate ChatWidget with Docusaurus using Root swizzling
- [ ] **T048** [P] Test global chat widget accessibility on all textbook pages
- [ ] **T049** [P] Implement proper error handling for API communication
- [ ] **T050** [P] Add offline/error state handling with user-friendly messages
- [ ] **T051** [P] Test basic Q&A functionality with textbook content
- [ ] **T052** [P] Verify source citations appear in responses
- [ ] **T053** [P] Test off-topic query handling and rejection
- [ ] **T054** [P] Validate response accuracy against textbook content
- [ ] **T055** [P] Test conversation context maintenance
- [ ] **T056** [P] Verify response formatting with markdown support
- [ ] **T057** [P] Test multiple concurrent chat sessions
- [ ] **T058** [P] Validate proper session cleanup after 24 hours
- [ ] **T059** [P] Performance test: verify <3s response time for 95% of queries

## Phase 5: US2 - Text Selection (14 tasks) - P1

- [X] **T060** [P] Create TextSelectionHandler React component
- [X] **T061** [P] Implement text selection detection using mouseup/touchend events
- [X] **T062** [P] Add 500ms delay to prevent interference with normal reading
- [X] **T063** [P] Create floating "Ask about this" button positioned near selection
- [X] **T064** [P] Style the selection button to match Docusaurus theme
- [X] **T065** [P] Pass selected text context to the chat API
- [ ] **T066** [P] Handle selected text in the backend RAG pipeline
- [ ] **T067** [P] Generate context-aware responses based on selected text
- [ ] **T068** [P] Test text selection on all textbook pages (4 pages)
- [ ] **T069** [P] Verify button appears correctly on desktop and mobile
- [ ] **T070** [P] Test selection of multiple text ranges
- [ ] **T071** [P] Validate selected text context is preserved during conversation
- [ ] **T072** [P] Test integration with existing chat session functionality
- [ ] **T073** [P] Performance test: verify text selection doesn't impact page performance

## Phase 6: US3 - Navigation (8 tasks) - P2

- [X] **T074** [P] Enhance content chunks with proper URL metadata during indexing
- [X] **T075** [P] Update LLM prompt to include instructions for generating navigation links
- [X] **T076** [P] Implement clickable source citations in chat responses
- [X] **T077** [P] Create navigation link component with proper styling
- [X] **T078** [P] Test navigation queries ("Where can I learn about X?")
- [X] **T079** [P] Validate all generated navigation links point to existing content
- [X] **T080** [P] Test navigation link accuracy across all textbook pages
- [X] **T081** [P] Verify navigation links open in appropriate contexts

## Phase 7: US4 - Guidance (8 tasks) - P3

- [X] **T082** [P] Add curriculum structure (chapters, lessons, prerequisites) to LLM context
- [X] **T083** [P] Implement "What should I study next?" query handling
- [X] **T084** [P] Create course overview functionality with structured navigation
- [X] **T085** [P] Implement prerequisite detection for difficult concepts
- [X] **T086** [P] Add learning path recommendation algorithm
- [X] **T087** [P] Test guidance functionality with different user progression states
- [X] **T088** [P] Validate guidance responses align with curriculum structure
- [X] **T089** [P] Test course overview and structured navigation options

## Phase 8: Polish & Testing (12 tasks)

- [X] **T090** [P] Implement rate limiting to prevent API abuse
- [X] **T091** [P] Add input sanitization to prevent injection attacks
- [X] **T092** [P] Implement proper error handling for empty queries
- [X] **T093** [P] Add query length limits to prevent abuse
- [X] **T094** [P] Implement XSS protection for user inputs
- [ ] **T095** [P] Add Urdu locale support to UI components
- [ ] **T096** [P] Test concurrent user performance (100+ users)
- [ ] **T097** [P] Verify <3s p95 latency under load
- [ ] **T098** [P] Run security assessment to verify no vulnerabilities
- [ ] **T099** [P] Test off-topic query refusal rate (target 95%+)
- [ ] **T100** [P] Performance optimization for embedding generation speed
- [ ] **T101** [P] Final integration testing of all features together

## Phase 9: Deployment (23 tasks)

- [X] **T102** [P] Create Dockerfile for api/ backend with multi-stage build
- [X] **T103** [P] Create .dockerignore file for backend
- [X] **T104** [P] Create docker-compose.yml for local development
- [ ] **T105** [P] Test Docker deployment locally
- [X] **T106** [P] Create render.yaml configuration for Render deployment
- [X] **T107** [P] Add build and start commands for Render (uv sync, uv run)
- [X] **T108** [P] Configure environment variables for Render deployment
- [ ] **T109** [P] Test Render deployment with sample content
- [X] **T110** [P] Create railway.json configuration for Railway deployment
- [X] **T111** [P] Create Procfile for Railway deployment
- [X] **T112** [P] Configure environment variables for Railway deployment
- [ ] **T113** [P] Test Railway deployment with sample content
- [X] **T114** [P] Create app.py for Hugging Face Spaces deployment
- [X] **T115** [P] Create requirements.txt for Hugging Face Spaces
- [X] **T116** [P] Create README_HF.md with Hugging Face Spaces instructions
- [ ] **T117** [P] Test Hugging Face Spaces deployment
- [X] **T118** [P] Create comprehensive DEPLOYMENT.md guide
- [X] **T119** [P] Document Docker deployment process and commands
- [X] **T120** [P] Document Render deployment configuration and environment variables
- [X] **T121** [P] Document Railway deployment process and configuration
- [X] **T122** [P] Document Hugging Face Spaces deployment and customization
- [X] **T123** [P] Add troubleshooting section for common deployment issues
- [ ] **T124** [P] Final deployment testing across all platforms