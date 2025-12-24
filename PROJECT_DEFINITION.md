# Project Definition: Physical AI & Humanoid Robotics Textbook

**Version:** 1.0.0  
**Last Updated:** 2025-12-23  
**Status:** Active Development

---

## Executive Summary

The **Physical AI & Humanoid Robotics Textbook** is a comprehensive, AI-powered educational platform that delivers personalized learning experiences for students studying Physical AI and Humanoid Robotics. The platform combines a structured textbook (built with Docusaurus), an intelligent RAG-based chatbot, automated content generation workflows, and user personalization features to create an adaptive learning environment.

### Core Value Proposition

- **Educational Excellence**: High-quality, structured textbook content on Physical AI and Humanoid Robotics
- **AI-Powered Assistance**: RAG chatbot that answers questions using textbook content
- **Personalized Learning**: Content adaptation based on user background and experience
- **Automated Content Generation**: Workflow integration for programmatic content creation
- **Zero-Cost Architecture**: Built entirely on free-tier services

---

## Project Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Docusaurus)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Textbook    │  │  Chat Widget │  │  Auth Pages  │     │
│  │  Content     │  │  (RAG Chat)  │  │  (Signin/Up)│     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                          ↕ HTTP/REST API
┌─────────────────────────────────────────────────────────────┐
│              Backend API (FastAPI - Python)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Auth        │  │  RAG Service │  │  Workflow    │     │
│  │  Service     │  │  (Qdrant)    │  │  Orchestrator│     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Personaliz. │  │  Content    │  │  Validation  │     │
│  │  Service     │  │  Indexing   │  │  Service     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
         ↕                    ↕                    ↕
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  PostgreSQL   │    │  Qdrant      │    │  Gemini API  │
│  (Neon)       │    │  (Vector DB) │    │  (LLM)       │
└──────────────┘    └──────────────┘    └──────────────┘
```

---

## Technology Stack

### Frontend
- **Framework**: Docusaurus v3.x (React-based static site generator)
- **Language**: JavaScript/TypeScript
- **UI Components**: React 18+
- **Styling**: CSS Modules, Docusaurus theme system
- **Deployment**: GitHub Pages (static hosting)

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Package Manager**: uv (recommended) or pip
- **Database ORM**: SQLAlchemy (async)
- **Authentication**: JWT (JSON Web Tokens)
- **API Documentation**: OpenAPI/Swagger (auto-generated)

### Data Storage
- **Relational Database**: PostgreSQL (Neon Serverless - free tier)
- **Vector Database**: Qdrant Cloud (free tier)
- **File Storage**: File system (Markdown files in `frontend/textbook-content/`)

### AI/ML Services
- **LLM**: Google Gemini 1.5 Flash (via OpenAI Agents SDK)
- **Embeddings**: Qdrant FastEmbed (local, free)
- **RAG Pipeline**: Custom implementation with Qdrant vector search

### Development Tools
- **Specification**: Spec-Kit Plus methodology
- **AI Assistance**: Claude Code (Subagents and Skills)
- **Testing**: pytest (backend), Jest/Playwright (frontend)
- **CI/CD**: GitHub Actions
- **Version Control**: Git

---

## Core Features

### 1. Textbook Content System

**Purpose**: Structured educational content delivery

**Components**:
- Docusaurus-based static site
- Markdown-based lesson content
- Chapter/lesson organization
- Sidebar navigation
- Search functionality

**Content Structure**:
```
Chapter 1: Introduction to Physical AI
  ├── Lesson 1: What is Physical AI?
  └── Lesson 2: History and Evolution

Chapter 2: Fundamentals of Humanoid Robotics
  ├── Lesson 1: Kinematics and Motion
  └── Lesson 2: Control Systems

Chapter 3: Advanced Topics
  ├── Lesson 1: AI Integration
  └── Lesson 2: Future Directions
```

**Location**: `frontend/textbook-content/`

---

### 2. RAG Chatbot System

**Purpose**: AI-powered assistant that answers questions using textbook content

**How It Works**:
1. User asks a question via chat widget
2. System searches Qdrant vector database for relevant content chunks
3. Retrieves top-k most relevant sections
4. Sends question + context to Gemini LLM
5. Returns AI-generated answer with source citations

**Features**:
- Text selection support (users can select text for context)
- Source citations (links to relevant textbook sections)
- Navigation suggestions (related content links)
- Session management (conversation continuity)
- Real-time responses

**API Endpoints**:
- `POST /api/chat` - Send chat message
- `GET /api/sessions/{session_id}` - Get session history
- `DELETE /api/sessions/{session_id}` - Delete session

**Components**:
- `ChatWidget` (React component)
- `RAGService` (backend service)
- `ContentIndexingService` (RAG indexing)
- `LLMService` (Gemini integration)

---

### 3. User Authentication & Personalization

**Purpose**: Secure user accounts with personalized content delivery

**Authentication Features**:
- User registration with background information
- Secure login/logout with JWT tokens
- Password hashing (bcrypt)
- Token-based session management
- Protected API endpoints

**User Background Data Collected**:
- Software experience level (beginner/intermediate/advanced)
- Hardware experience level
- Programming languages known
- Robotics background (optional)
- Learning goals (optional)

**Personalization Features**:
- Content adaptation based on experience level
- Difficulty adjustment
- Learning path generation
- Progress tracking

**API Endpoints**:
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/signin` - Login
- `POST /api/auth/signout` - Logout
- `GET /api/auth/me` - Get current user
- `GET /api/user/background` - Get user background
- `PUT /api/user/background` - Update user background
- `POST /api/personalize/{content_id}` - Get personalized content
- `GET /api/personalize/learning-path` - Get learning path

**Components**:
- `AuthService` (backend)
- `PersonalizationService` (backend)
- `AuthContext` (React context)
- Signin/Signup pages (React components)

---

### 4. Workflow Integration System

**Purpose**: Automated content generation workflow orchestration

**Workflow Pipeline**:
```
Content Architect → Template Generator → Technical Writer → 
Validation → RAG Indexing → Frontend Sync
```

**Features**:
- API endpoint to trigger content generation
- Job status tracking (pending, in_progress, completed, failed)
- Progress updates (0-100%)
- Error handling and edge case management
- Automatic validation (word count, source validation)
- Automatic RAG indexing
- Frontend-backend synchronization
- Concurrent request management (one job at a time)
- Job cancellation support

**API Endpoints**:
- `POST /api/content/generate` - Create content generation job
- `GET /api/content/generate/{job_id}` - Get job status
- `POST /api/content/generate/{job_id}/cancel` - Cancel job

**Components**:
- `WorkflowOrchestrator` (orchestrates workflow)
- `ValidationService` (runs validation scripts)
- `SyncService` (handles RAG indexing and frontend sync)
- `ErrorHandler` (error handling module)
- `EdgeCaseHandler` (edge case handling module)

**Job Lifecycle**:
```
pending → in_progress → validating → indexing → syncing → completed
                                    ↓
                                 failed (at any step)
```

---

### 5. Content Generation Components

**Purpose**: AI-powered content generation using Claude Code agents

**Components**:
- **Content Architect**: Designs chapter/lesson structure
- **Lesson Template Generator**: Creates lesson templates
- **Technical Writer**: Generates lesson content (~800 words)
- **Validation Scripts**: 
  - `validate-word-count.py` - Validates word count
  - `validate-sources.py` - Validates source citations
- **Error Handler**: Handles workflow errors gracefully
- **Edge Case Handler**: Manages edge cases (insufficient sources, etc.)

**Location**: `specs/book-writing/scripts/`

---

## Project Structure

```
physical-ai-humanoid-robotics-book/
├── backend/                          # FastAPI backend
│   ├── src/
│   │   ├── main.py                  # FastAPI app entry point
│   │   ├── config.py                # Configuration (env vars)
│   │   ├── models.py                # Pydantic models (API schemas)
│   │   ├── database/
│   │   │   └── models.py            # SQLAlchemy models (DB schemas)
│   │   ├── routes/                  # API route handlers
│   │   │   ├── auth.py              # Authentication endpoints
│   │   │   ├── user.py              # User management endpoints
│   │   │   ├── personalization.py  # Personalization endpoints
│   │   │   └── content_generation.py # Workflow endpoints
│   │   ├── services/                 # Business logic
│   │   │   ├── auth_service.py      # Authentication logic
│   │   │   ├── rag_service.py       # RAG search logic
│   │   │   ├── llm_service.py       # Gemini LLM integration
│   │   │   ├── content_service.py   # Content indexing
│   │   │   ├── personalization_service.py # Content personalization
│   │   │   ├── workflow_orchestrator.py # Workflow orchestration
│   │   │   ├── validation_service.py # Validation wrapper
│   │   │   └── sync_service.py      # RAG/frontend sync
│   │   ├── utils/
│   │   │   ├── auth.py              # JWT utilities
│   │   │   ├── db.py                # Database utilities
│   │   │   └── workflow_utils.py    # Workflow utilities
│   │   └── middleware/
│   │       └── rate_limit.py        # Rate limiting
│   ├── tests/                        # Test suite
│   ├── requirements.txt              # Python dependencies
│   └── .env.local                    # Environment variables
│
├── frontend/                         # Textbook content (Markdown)
│   └── textbook-content/
│       ├── chapter-1-introduction-to-physical-ai/
│       ├── chapter-2-fundamentals-of-humanoid-robotics/
│       └── chapter-3-advanced-topics/
│
├── src/                              # Frontend React components
│   ├── components/
│   │   ├── ChatWidget/              # RAG chatbot widget
│   │   ├── NavbarAuth/              # Auth navbar component
│   │   └── TextSelectionHandler/    # Text selection handler
│   ├── pages/
│   │   ├── index.js                 # Home page
│   │   ├── signin.js                # Sign in page
│   │   ├── signup.js                # Sign up page
│   │   └── Root.jsx                 # Root layout
│   ├── theme/
│   │   ├── AuthContext.js           # Auth React context
│   │   └── Root.jsx                 # Docusaurus theme root
│   └── css/
│       └── custom.css               # Custom styles
│
├── specs/                            # Feature specifications
│   ├── 001-content-architect-subagent/
│   ├── 002-textbook-content-generation/
│   ├── 004-rag-chatbot/
│   ├── 005-personalized-content/
│   ├── 006-workflow-integration/
│   └── book-writing/                # Content generation scripts
│
├── history/                          # Prompt History Records (PHRs)
│   └── prompts/
│
├── docusaurus.config.js             # Docusaurus configuration
├── sidebars.ts                      # Documentation sidebar
├── package.json                     # Node.js dependencies
└── README.md                        # Project README
```

---

## Data Models

### User & Authentication
- **User**: Email, password hash, active status, created_at
- **UserBackground**: Software/hardware experience, programming languages, robotics background, learning goals
- **AuthResponse**: User data + JWT access token

### Content & RAG
- **ContentChunk**: Content text, chapter, lesson, embedding vector, URL
- **ChatMessage**: Role (user/assistant), content, sources, timestamp
- **ChatSession**: Session ID, messages, current page, expiration

### Workflow Integration
- **ContentGenerationRequest**: Chapters, lessons, research guidance, target word count
- **ContentGenerationJob**: Job ID, status, progress, results, error details
- **ValidationResult**: Word count validation, source validation, quality checks
- **IntegrationStatus**: RAG indexing status, frontend sync status

---

## API Architecture

### Authentication Endpoints
```
POST   /api/auth/signup          # Register new user
POST   /api/auth/signin          # Login
POST   /api/auth/signout         # Logout
GET    /api/auth/me              # Get current user
```

### User Management
```
GET    /api/user/background     # Get user background
PUT    /api/user/background     # Update user background
```

### Personalization
```
POST   /api/personalize/{content_id}  # Get personalized content
GET    /api/personalize/learning-path # Get learning path
```

### RAG Chatbot
```
POST   /api/chat                # Send chat message
GET    /api/sessions/{session_id}    # Get session
DELETE /api/sessions/{session_id}    # Delete session
POST   /api/index-content        # Index content in RAG
GET    /api/chunks/search        # Search content chunks
```

### Content Generation Workflow
```
POST   /api/content/generate                    # Create generation job
GET    /api/content/generate/{job_id}           # Get job status
POST   /api/content/generate/{job_id}/cancel    # Cancel job
```

### Health & Utility
```
GET    /api/health              # Health check
GET    /docs                    # API documentation (Swagger UI)
GET    /redoc                   # API documentation (ReDoc)
```

---

## Key Workflows

### 1. User Registration & Login Flow

```
1. User visits signup page
2. Fills form (email, password, background info)
3. Frontend validates inputs (real-time)
4. POST /api/auth/signup
5. Backend creates user + background in database
6. Backend generates JWT token
7. Frontend saves token to localStorage
8. User redirected to home page
9. Token used for authenticated requests
```

### 2. RAG Chatbot Flow

```
1. User opens chat widget
2. User types question
3. Frontend sends POST /api/chat with:
   - Message text
   - Selected text (if any)
   - Current page URL
   - Session ID
4. Backend RAGService searches Qdrant for relevant chunks
5. Backend LLMService sends question + context to Gemini
6. Gemini generates answer
7. Backend returns answer + sources + navigation links
8. Frontend displays answer in chat widget
```

### 3. Content Generation Workflow

```
1. Developer calls POST /api/content/generate
2. Backend creates job (status: pending)
3. WorkflowOrchestrator starts background task
4. Orchestrator invokes Content Architect (subprocess)
5. Orchestrator invokes Template Generator (subprocess)
6. Orchestrator invokes Technical Writer (subprocess)
7. ValidationService runs validation scripts
8. If validation passes:
   - SyncService indexes content in Qdrant
   - SyncService syncs files to frontend
9. Job status updated to "completed"
10. Developer polls GET /api/content/generate/{job_id} for status
```

---

## Development Methodology

### Spec-Kit Plus Workflow

All features follow a strict specification-driven development process:

1. **Specification** (`/sp.specify`): Define feature requirements
2. **Planning** (`/sp.plan`): Create implementation plan
3. **Clarification** (`/sp.clarify`): Resolve ambiguities
4. **Task Breakdown** (`/sp.tasks`): Generate detailed task list
5. **Analysis** (`/sp.analyze`): Validate spec/plan/tasks consistency
6. **Implementation** (`/sp.implement`): Execute tasks
7. **Testing**: Verify functionality
8. **Documentation**: Update docs and create PHRs

### Feature Development History

**Completed Features**:
- ✅ Content Architect Subagent (001)
- ✅ Textbook Content Generation (002)
- ✅ RAG Chatbot (004)
- ✅ Personalized Content (005)
- ✅ Workflow Integration (006)

**Current Status**: All core features implemented, UI improvements in progress

---

## Configuration & Environment

### Backend Environment Variables (`.env.local`)

```env
# Required
GEMINI_API_KEY=your_gemini_api_key
QDRANT_URL=https://your-instance.qdrant.io
QDRANT_API_KEY=your_qdrant_key
DATABASE_URL=postgresql://user:pass@host:port/db
JWT_SECRET_KEY=your_secret_key_min_32_chars

# Optional
UVICORN_HOST=0.0.0.0
UVICORN_PORT=8000
FRONTEND_URL=http://localhost:3000
```

### Frontend Environment Variables

```env
REACT_APP_API_URL=http://localhost:8000
```

---

## Deployment

### Backend Deployment Options
- **Render**: Free tier, auto-deploy from GitHub
- **Railway**: Free tier, easy setup
- **Hugging Face Spaces**: Docker-based
- **Heroku**: Using Procfile

### Frontend Deployment
- **GitHub Pages**: Free, automatic from main branch
- **Netlify**: Free tier, continuous deployment
- **Vercel**: Free tier, optimized for React

---

## Performance Targets

- **RAG Response Time**: < 3 seconds
- **Page Load Time**: < 2 seconds
- **API Response Time**: < 2 seconds (validation)
- **Concurrent Users**: 100+ supported
- **Content Generation**: < 5 minutes per job
- **Success Rate**: 95% without manual intervention

---

## Security Features

- **Authentication**: JWT tokens with expiration
- **Password Security**: bcrypt hashing (12 rounds)
- **API Security**: Rate limiting (60 req/min per IP)
- **CORS**: Configured for frontend origin only
- **Input Validation**: Pydantic models for all inputs
- **SQL Injection Protection**: SQLAlchemy ORM
- **XSS Protection**: Input sanitization

---

## Testing Strategy

### Backend Tests
- **Unit Tests**: pytest for services and utilities
- **Integration Tests**: API endpoint testing
- **Contract Tests**: OpenAPI specification validation
- **Test Coverage**: >80% for base features

### Frontend Tests
- **Component Tests**: Jest + React Testing Library
- **E2E Tests**: Playwright
- **Accessibility Tests**: WCAG 2.1 AA compliance

---

## Current Implementation Status

### ✅ Completed
- Backend API (FastAPI)
- RAG chatbot system
- User authentication
- Content personalization
- Workflow integration (90/90 tasks)
- Textbook content structure
- Frontend UI components

### 🔧 In Progress
- UI/UX improvements
- Form validation enhancements
- Error handling refinement

### 📋 Planned
- Urdu translation support
- Advanced personalization features
- Performance optimization
- Additional content chapters

---

## Key Files Reference

### Backend Entry Points
- `backend/src/main.py` - FastAPI application
- `backend/app.py` - Hugging Face Spaces entry point
- `backend/Procfile` - Heroku/Railway deployment

### Frontend Entry Points
- `src/pages/index.js` - Home page
- `src/theme/Root.jsx` - Docusaurus root component
- `docusaurus.config.js` - Docusaurus configuration

### Configuration
- `backend/src/config.py` - Backend settings
- `backend/.env.local` - Environment variables
- `package.json` - Frontend dependencies

---

## Getting Started

### Quick Start

1. **Clone repository**
2. **Backend setup**:
   ```bash
   cd backend
   cp .env.example .env.local
   # Edit .env.local with your API keys
   uv sync  # or pip install -r requirements.txt
   python scripts/create_tables.py
   uvicorn src.main:app --reload
   ```

3. **Frontend setup**:
   ```bash
   npm install
   npm start
   ```

4. **Access**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

---

## Project Goals

### Primary Goals
1. Deliver high-quality educational content on Physical AI & Humanoid Robotics
2. Provide AI-powered learning assistance via RAG chatbot
3. Enable personalized learning experiences
4. Support automated content generation workflows

### Success Metrics
- **Educational**: User engagement, learning outcomes
- **Technical**: <3s response times, 95% uptime
- **Performance**: 100+ concurrent users
- **Quality**: >80% test coverage, zero critical bugs

---

## License

MIT License - See LICENSE file for details

---

## Contact & Support

- **Repository**: [GitHub](https://github.com/arman-saleem/physical-ai-humanoid-robotics-book)
- **Documentation**: See `/docs` folder
- **API Documentation**: http://localhost:8000/docs (when backend running)

---

**Last Updated**: 2025-12-23  
**Maintained By**: Arman Saleem  
**Project Status**: Active Development


