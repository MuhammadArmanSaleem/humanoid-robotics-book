# RAG Chatbot for Textbook Content - Feature Specification

## Executive Summary

Implement a RAG (Retrieval-Augmented Generation) based chatbot that serves as an intelligent learning assistant embedded within the Docusaurus textbook. The chatbot will exclusively source answers from textbook content, provide text selection queries, navigation to relevant pages, and guide students through the book content. The implementation will use free services only to maintain $0 cost, utilizing Qdrant FastEmbed for embeddings, Qdrant Cloud free tier for vector storage, and Gemini 1.5 Flash via OpenAI Agents SDK.

## User Scenarios & Testing

### User Story 1 (P0): Answer Questions from Book Content
As a student, I want to ask questions about the textbook content so that I can get accurate answers with proper citations to the source material.

**Acceptance Scenarios:**
- Student asks a general question about Physical AI concepts and receives a comprehensive answer with source citations
- Student asks a specific question about humanoid robotics and gets a detailed response with relevant textbook references
- Student asks an off-topic question and the system politely declines while explaining its scope
- Student asks for clarification on a complex topic and receives an explanation with examples from the textbook

### User Story 2 (P1): Answer Questions from Selected Text
As a student, I want to select text on a page and ask questions about that specific content so that I can get contextual answers.

**Acceptance Scenarios:**
- Student selects a paragraph about kinematics and clicks "Ask about this" to get detailed explanation
- Student highlights a definition and asks for examples, receiving relevant examples from other parts of the textbook
- Student selects a code snippet and asks for explanation, getting a breakdown of the implementation
- Student selects multiple sections and asks comparative questions, receiving synthesized answers

### User Story 3 (P2): Navigate User to Relevant Pages
As a student, I want the chatbot to provide navigation links to relevant pages when answering questions so that I can explore the content further.

**Acceptance Scenarios:**
- Chatbot answers a question and provides clickable links to related lessons in the textbook
- Student asks about prerequisites for a topic and receives navigation links to foundational concepts
- Chatbot identifies the most relevant pages for a query and provides direct URLs
- Student asks to continue learning about a topic and gets navigation to advanced materials

### User Story 4 (P3): Guide Student Through Book Content
As a student, I want the chatbot to recommend learning paths and guide me through the book content so that I can follow an optimal learning journey.

**Acceptance Scenarios:**
- New student asks for an overview and receives a structured course outline with recommended sequence
- Student asks for help with a difficult concept and gets guided to prerequisite materials
- Student asks for next steps after completing a chapter and receives personalized recommendations
- Student asks for review materials and gets links to relevant exercises and summaries

## Functional Requirements

### Core RAG Functionality (FR-001 to FR-007)
- **FR-001**: System shall use Qdrant Cloud (free tier) for vector storage to maintain $0 cost
- **FR-002**: System shall use Qdrant FastEmbed for local embedding generation (no API cost)
- **FR-003**: System shall use Gemini 1.5 Flash (free tier) via OpenAI Agents SDK for chat completion
- **FR-004**: System shall retrieve relevant textbook content based on user queries with semantic search
- **FR-005**: System shall generate responses that are grounded in textbook content only
- **FR-006**: System shall provide source citations for all information in its responses
- **FR-007**: System shall handle off-topic queries by declining and explaining its scope

### Text Selection Feature (FR-008 to FR-011)
- **FR-008**: System shall capture selected text from the current page when user initiates a query
- **FR-009**: System shall provide an "Ask about this" button accessible when text is selected
- **FR-010**: System shall pass selected text context to the RAG pipeline for contextual answers
- **FR-011**: System shall maintain the context of selected text during the conversation
- **FR-012a**: System shall detect text selection using mouseup/touchend events on all textbook pages
- **FR-012b**: System shall show floating "Ask about this" button near selected text with 500ms delay to avoid interference

### Navigation Feature (FR-012 to FR-015)
- **FR-012**: System shall map textbook content to URLs for navigation purposes
- **FR-013**: System shall generate clickable links to relevant lessons and chapters
- **FR-014**: System shall provide direct navigation URLs when answering queries about specific topics
- **FR-015**: System shall validate navigation links to ensure they point to existing content

### Guidance Feature (FR-016 to FR-018)
- **FR-016**: System shall understand the curriculum structure (chapters, lessons, sections)
- **FR-017**: System shall recommend learning paths based on student progress and goals
- **FR-018**: System shall provide course overview and structured navigation options

### UI/UX Requirements (FR-019 to FR-024)
- **FR-019**: System shall provide a floating chat button that is accessible on all textbook pages
- **FR-020**: System shall have a responsive chat interface that works on desktop and mobile
- **FR-021**: System shall support both English and relevant local languages (bilingual interface)
- **FR-022**: System shall provide visual feedback during query processing
- **FR-023**: System shall maintain conversation history within a session
- **FR-024**: System shall provide clear instructions and examples for using the chatbot

### Backend Requirements (FR-025 to FR-031)
- **FR-025**: Backend shall be implemented using FastAPI framework
- **FR-026**: Backend shall use uv as package manager
- **FR-027**: Backend shall implement Server-Sent Events (SSE) for streaming responses
- **FR-028**: Backend shall implement rate limiting to prevent abuse
- **FR-029**: Backend shall support session management for conversation continuity
- **FR-029a**: Sessions shall persist for 24 hours of inactivity before cleanup
- **FR-029b**: Session data shall be stored in-memory with optional Redis backend for scaling
- **FR-030**: Backend shall implement proper error handling and logging
- **FR-031**: Backend shall implement health check endpoints

### Security Requirements (FR-032 to FR-035)
- **FR-032**: System shall sanitize all user inputs to prevent injection attacks
- **FR-033**: System shall use environment variables for API keys and sensitive configuration
- **FR-034**: System shall implement proper CORS policies for web integration
- **FR-035**: System shall log security-relevant events for monitoring

## Success Criteria

- **SC-001**: Response latency is under 3 seconds for 95% of queries
- **SC-002**: Answer accuracy is 90% or higher based on textbook content validation
- **SC-003**: All responses include 100% accurate source citations to textbook content
- **SC-004**: Text selection feature works on all 4 textbook pages without issues
- **SC-005**: Navigation links are 100% accurate and point to correct textbook locations
- **SC-006**: System supports 100 concurrent users without performance degradation (on min 1GB RAM, 1vCPU infrastructure)
- **SC-007**: Zero security vulnerabilities detected in security assessment
- **SC-008**: System correctly refuses 95% or more of off-topic queries

## Key Entities

### ContentChunk
- id: Unique identifier for the content chunk
- content: The actual text content
- chapter: Chapter identifier where this content belongs
- lesson: Lesson identifier within the chapter
- section: Section within the lesson
- url: URL to the specific location in the textbook
- embedding: 384-dimensional vector embedding of the content

### ChatMessage
- id: Unique identifier for the message
- role: Role of the message (user/system/assistant)
- content: The actual message content
- sources: List of source references used in the response
- timestamp: When the message was created

### ChatSession
- session_id: Unique identifier for the conversation session
- messages: List of messages in the session
- created_at: When the session was created
- current_page: Current page URL where the chat was initiated

## Assumptions

- The textbook content is already available and properly structured in Docusaurus
- Students have basic familiarity with chat interfaces
- Internet connectivity is available for API calls to Qdrant and Gemini
- The Qdrant Cloud free tier (1GB) will be sufficient for the content embeddings
- The Gemini 1.5 Flash free tier usage limits will be adequate for expected usage

## Constraints

- Implementation must use only free services to maintain $0 cost
- All responses must be grounded in textbook content only (no external knowledge)
- Must integrate seamlessly with existing Docusaurus textbook structure
- Performance must meet standard web application expectations
- Must comply with privacy regulations (GDPR, CCPA) - no personal data storage, session-only data retention

## Appendix A: API Contract

### POST /api/chat
Request body:
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

Response: Server-Sent Events stream with JSON messages containing:
- response text chunks
- source citations
- navigation links
- session information

### GET /api/health
Returns health status of the chatbot service.

## Appendix B: Content Indexing Strategy

The textbook content will be chunked into 50-60 semantic units for optimal retrieval. Each chunk will be:
- Approximately 200-500 words of coherent content
- Associated with chapter, lesson, and section metadata
- Converted to embeddings using Qdrant FastEmbed (BAAI/bge-small-en-v1.5, 384 dimensions)
- Stored in Qdrant Cloud with proper metadata for retrieval

## Appendix C: Environment Variables

- GEMINI_API_KEY: API key for Gemini 1.5 Flash access
- QDRANT_URL: URL for Qdrant Cloud instance
- QDRANT_API_KEY: API key for Qdrant Cloud access
- FRONTEND_URL: Allowed origin for CORS (for Docusaurus integration)

## Clarifications

### Session 2025-12-16

- Q: Which privacy regulations apply and how should user data be handled? → A: Must comply with GDPR and CCPA - no personal data storage, session-only data retention
- Q: How should text selection be implemented across textbook pages? → A: Use mouseup/touchend events with floating "Ask about this" button appearing after 500ms delay
- Q: What infrastructure assumptions apply to the 100 concurrent users requirement? → A: Minimum 1GB RAM, 1vCPU infrastructure for performance targets
- Q: What are the session management requirements for conversation continuity? → A: Sessions persist 24 hours with in-memory storage (optional Redis for scaling)

## Appendix D: Deployment Options

Multiple deployment options will be supported:
- Docker: For local development and containerized deployment
- Render: For easy cloud deployment with free tier
- Railway: For modern deployment experience
- Hugging Face Spaces: For ML-focused demos and sharing