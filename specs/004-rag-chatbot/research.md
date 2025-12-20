# RAG Chatbot Research & Decision Log

## Decision 1: Vector Database & Embedding Strategy

**Decision:** Use Qdrant Cloud (free tier) with Qdrant FastEmbed for local embeddings

**Rationale:**
- Zero-cost implementation as required by project constraints
- Qdrant FastEmbed runs locally (no API cost) using BAAI/bge-small-en-v1.5 model
- 384-dimensional embeddings provide good balance of accuracy and performance
- Qdrant Cloud free tier (1GB) sufficient for textbook content

**Alternatives considered:**
- Pinecone: Commercial solution, exceeds zero-cost constraint
- Weaviate: Self-hosted option but requires more infrastructure management
- OpenAI embeddings: Would incur API costs, violates zero-cost requirement

**Technical details:**
- Model: BAAI/bge-small-en-v1.5 (384 dimensions)
- Local embedding generation with no API calls
- Vector storage in Qdrant Cloud with free tier limits

## Decision 2: LLM Integration

**Decision:** Use OpenAI Agents SDK with custom provider for Gemini 1.5 Flash

**Rationale:**
- Free tier access to Gemini 1.5 Flash provides cost-effective RAG capabilities
- OpenAI Agents SDK allows custom provider integration
- Better cost efficiency than OpenAI GPT models for RAG applications
- Good performance for educational Q&A use case

**Alternatives considered:**
- Direct OpenAI API: Would incur costs, violates zero-cost constraint
- Anthropic Claude: Would require different SDK integration, potential costs
- Open-source models: Would require self-hosting, more infrastructure

**Technical details:**
- Provider: Google Gemini via OpenAI Agents SDK
- Model: gemini-1.5-flash
- Streaming responses via SSE for better UX

## Decision 3: Frontend Integration Approach

**Decision:** Use Docusaurus Root swizzling for global chat widget

**Rationale:**
- Provides floating chat button accessible on all textbook pages
- Maintains Docusaurus theme and styling consistency
- Non-intrusive integration that doesn't modify existing pages
- Works with existing Docusaurus architecture

**Alternatives considered:**
- Layout swizzling: Would affect all page layouts, more intrusive
- Individual page modifications: Would require changes to every textbook page
- Iframe embedding: Would create isolation issues, styling problems

**Technical details:**
- React component injected globally via Root swizzling
- Floating button with minimal space usage
- CSS positioning to avoid content interference

## Decision 4: Text Selection Implementation

**Decision:** Mouseup/touchend events with 500ms delay for "Ask about this" button

**Rationale:**
- Non-intrusive user experience that doesn't interfere with reading
- Works consistently across desktop and mobile devices
- 500ms delay prevents accidental button appearance during normal reading
- Clear visual indication of selection context

**Alternatives considered:**
- Context menu: Would require right-click which isn't available on mobile
- Toolbar button: Would take up permanent screen space
- Highlight with immediate button: Too intrusive, appears during every selection

**Technical details:**
- Event listeners for mouseup and touchend
- 500ms delay to avoid interference with normal reading
- Position button near selection with absolute positioning

## Decision 5: Session Management

**Decision:** In-memory storage with optional Redis for scaling

**Rationale:**
- Simpler implementation for initial deployment
- Sufficient for 24-hour session persistence requirement
- Redis option available for production scaling
- Aligns with performance targets (100 concurrent users)

**Alternatives considered:**
- Database storage: More complex, unnecessary for session-only data
- Client-side storage: Security concerns, limited capacity
- Server-side files: Less scalable, harder to manage

**Technical details:**
- 24-hour inactivity timeout
- Session cleanup mechanism
- Optional Redis backend for horizontal scaling

## Decision 6: Deployment Strategy

**Decision:** Multiple deployment options (Docker, Render, Railway, Hugging Face)

**Rationale:**
- Provides flexibility for different use cases and preferences
- Supports hackathon demo requirements (multiple options)
- Docker for local development and containerized deployment
- Cloud options for easy production deployment

**Alternatives considered:**
- Single deployment option: Less flexible, doesn't meet user requirements
- Other cloud platforms: Would require additional research and configuration

**Technical details:**
- Docker configuration with multi-stage build
- Render and Railway configs for easy cloud deployment
- Hugging Face Spaces for ML-focused demos
- Environment variable management across all options

## Decision 7: Content Chunking Strategy

**Decision:** 200-500 word semantic chunks with chapter/lesson metadata

**Rationale:**
- Optimal size for RAG retrieval and context window usage
- Semantic coherence within chunks improves response quality
- Metadata enables navigation and context awareness
- Aligns with textbook structure for better user experience

**Alternatives considered:**
- Fixed character counts: Might break semantic coherence
- Sentence-level chunks: Too granular, loses context
- Full-page chunks: Too large, reduces precision

**Technical details:**
- 200-500 word range for optimal retrieval
- Preserve paragraph boundaries where possible
- Include chapter, lesson, section, and URL metadata
- Overlap handling to maintain context across chunks