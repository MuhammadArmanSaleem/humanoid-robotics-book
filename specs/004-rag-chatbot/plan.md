# RAG Chatbot Implementation Plan

## Technical Context

### Architecture Overview
- **Frontend**: Docusaurus-integrated React chat widget with floating button
- **Backend**: FastAPI service with uv package manager
- **Vector Database**: Qdrant Cloud (free tier) with 384-dim embeddings
- **LLM**: Gemini 1.5 Flash via OpenAI Agents SDK (free tier)
- **Embeddings**: Qdrant FastEmbed (BGE-small-en-v1.5, local, no API cost)
- **Deployment**: Multiple options (Docker, Render, Railway, Hugging Face Spaces)

### Technology Stack
- **Backend**: Python 3.11+, FastAPI, uv
- **Vector DB**: Qdrant Cloud + FastEmbed
- **LLM Integration**: OpenAI Agents SDK with Gemini 1.5 Flash
- **Frontend**: React components integrated with Docusaurus
- **API**: REST API with Server-Sent Events (SSE) for streaming responses
- **Security**: CORS, rate limiting, input sanitization

### Infrastructure Requirements
- **Memory**: Minimum 1GB RAM (for 100 concurrent users support)
- **CPU**: 1vCPU minimum for performance targets
- **Storage**: Qdrant Cloud free tier (1GB) for embeddings
- **Network**: Internet connectivity for Qdrant and Gemini APIs

### Known Unknowns
- Qdrant connection code details (to be provided by user)
- Gemini API key (to be provided by user)
- Specific Docusaurus swizzling requirements for global chat widget
- Exact content chunking strategy for textbook content

## Constitution Check

### Principle Compliance Analysis

| Principle | Status | Notes |
|-----------|--------|-------|
| Content-First Development | ✅ | RAG chatbot enhances learning experience |
| AI-Assisted Spec-Driven Workflow | ✅ | Following spec-driven approach with formal requirements |
| Progressive Enhancement Architecture | ✅ | Core Q&A first, then text selection, navigation, guidance |
| Reusable Intelligence | ✅ | Qdrant FastEmbed for local embeddings, reusable components |
| User-Centered Personalization | ❌ | Not in scope for this feature (textbook content only) |
| Multilingual Accessibility | ✅ | Bilingual interface support (English/Urdu) |
| Performance & Scalability Standards | ✅ | Target <3s response, 100+ concurrent users |
| Test-Before-Implement Discipline | ✅ | Tests will be written for all functionality |
| Documentation as Code | ✅ | PHRs and proper documentation |

### Compliance Gaps
- **User Personalization**: Not applicable for this feature (textbook-only Q&A)
- **Better-Auth Integration**: Not in scope for this RAG chatbot feature

### Risk Mitigation
- Zero-cost architecture maintained with free tiers
- Performance targets validated with infrastructure assumptions
- Security requirements met with input sanitization and rate limiting

## Phase 0: Research & Discovery

### Research Tasks
1. **Qdrant Integration Research**
   - Decision: Use Qdrant Cloud with FastEmbed for local embeddings
   - Rationale: Zero-cost implementation with good performance
   - Alternatives considered: Pinecone, Weaviate (cost concerns)

2. **Gemini API Integration Research**
   - Decision: Use OpenAI Agents SDK with custom provider for Gemini 1.5 Flash
   - Rationale: Free tier access, good for RAG applications
   - Alternatives considered: Direct Gemini API, OpenAI GPT (cost concerns)

3. **Docusaurus Integration Research**
   - Decision: Use Root swizzling to inject global chat widget
   - Rationale: Provides floating chat button across all textbook pages
   - Alternatives considered: Layout swizzling (less flexible)

4. **Text Selection Implementation Research**
   - Decision: Mouseup/touchend events with 500ms delay for "Ask about this" button
   - Rationale: Non-intrusive user experience, works on all devices
   - Alternatives considered: Context menu, toolbar button (more intrusive)

## Phase 1: Data Model & API Design

### Data Model (data-model.md)

#### ContentChunk Entity
- **id**: string (unique identifier)
- **content**: string (text content, 200-500 words)
- **chapter**: string (chapter identifier)
- **lesson**: string (lesson identifier within chapter)
- **section**: string (section within lesson)
- **url**: string (URL to specific location in textbook)
- **embedding**: float[384] (384-dimensional vector embedding)

#### ChatMessage Entity
- **id**: string (unique identifier)
- **role**: enum (user/system/assistant)
- **content**: string (message content)
- **sources**: array of objects (source references used in response)
- **timestamp**: datetime (when message was created)

#### ChatSession Entity
- **session_id**: string (unique session identifier)
- **messages**: array of ChatMessage (conversation history)
- **created_at**: datetime (session creation time)
- **current_page**: string (current page URL where chat initiated)
- **expires_at**: datetime (session expiration time, 24 hours after inactivity)

### API Contracts

#### POST /api/chat
**Request Body:**
```json
{
  "message": "User's question",
  "context": {
    "selected_text": "Text selected by user (optional)",
    "current_url": "Current page URL",
    "session_id": "Conversation session ID (optional)"
  }
}
```

**Response:** Server-Sent Events stream with JSON messages containing:
- response text chunks
- source citations
- navigation links
- session information

#### GET /api/health
**Response:** Health status of the chatbot service

#### POST /api/index-content
**Request Body:**
```json
{
  "content_chunks": [
    {
      "content": "Text content",
      "chapter": "Chapter identifier",
      "lesson": "Lesson identifier",
      "section": "Section identifier",
      "url": "URL to location"
    }
  ]
}
```

**Response:** Status of content indexing operation

## Phase 2: Implementation Strategy

### Phase 2A: Backend Setup
1. Initialize FastAPI project with uv package manager
2. Create .env.example and .env files for configuration
3. Implement Qdrant connection and test with provided code
4. Implement Gemini API connection via OpenAI Agents SDK
5. Create Pydantic settings models for configuration

### Phase 2B: Core RAG Services
1. Implement content indexing service with FastEmbed
2. Implement RAG service with Qdrant vector search
3. Implement LLM service with Gemini 1.5 Flash
4. Create content chunking strategy (200-500 words with metadata)

### Phase 2C: API Endpoints
1. Create FastAPI app with CORS configuration
2. Implement POST /api/chat with SSE streaming
3. Implement GET /api/health endpoint
4. Implement POST /api/index-content for content ingestion

### Phase 2D: Frontend Integration
1. Create ChatWidget React component with floating button
2. Implement message list with markdown rendering
3. Integrate with Docusaurus using Root swizzling
4. Implement visual feedback during query processing

### Phase 2E: Text Selection Feature
1. Create TextSelectionHandler component
2. Implement text selection capture (mouseup/touchend events)
3. Create "Ask about this" floating button with 500ms delay
4. Pass selected text context to backend RAG pipeline

### Phase 2F: Navigation Feature
1. Add URL metadata to content chunks during indexing
2. Update LLM prompt to include link generation
3. Implement clickable source citations with navigation
4. Handle navigation queries ("Where can I learn about X?")

### Phase 2G: Guidance Feature
1. Implement curriculum structure understanding in LLM context
2. Handle "What should I study next?" queries
3. Provide course overview and prerequisites information
4. Implement learning path recommendations

### Phase 2H: Testing & Polish
1. Implement error handling (empty query, length limits, XSS protection)
2. Add Urdu locale support
3. Performance testing with concurrent users
4. Security validation and rate limiting

### Phase 2I: Deployment
1. Create Docker configuration (Dockerfile, docker-compose.yml)
2. Implement Render deployment (render.yaml)
3. Create Railway configuration (railway.json, Procfile)
4. Implement Hugging Face Spaces deployment (app.py, requirements.txt)
5. Create comprehensive DEPLOYMENT.md guide

## Phase 3: Quality Assurance

### Testing Strategy
- Unit tests for all services and components
- Integration tests for RAG pipeline
- End-to-end tests for user flows
- Performance tests for 100 concurrent users
- Security tests for input sanitization

### Performance Benchmarks
- Response latency under 3 seconds (95% of queries)
- Support for 100 concurrent users
- Content indexing performance
- Embedding generation speed

### Security Validation
- Input sanitization validation
- Rate limiting effectiveness
- API key security
- Session management security

## Dependencies & Integration Points

### External Dependencies
- Qdrant Cloud API (vector storage)
- Gemini 1.5 Flash API (LLM)
- Docusaurus (frontend integration)
- FastAPI (backend framework)

### Integration Points
- Textbook content extraction and chunking
- Docusaurus Root swizzling for global widget
- Session management with in-memory/Redis
- Content indexing from textbook structure

## Risk Assessment

### High Risk Items
- Qdrant and Gemini API availability and rate limits
- Performance with 100 concurrent users on minimum infrastructure
- Content chunking quality affecting RAG performance

### Medium Risk Items
- Docusaurus integration complexity
- Text selection UX implementation
- Multi-deployment configuration maintenance

### Mitigation Strategies
- Implement proper error handling and fallbacks
- Thorough testing with load scenarios
- Clear documentation for deployment options