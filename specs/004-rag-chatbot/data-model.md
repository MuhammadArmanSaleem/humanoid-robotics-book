# RAG Chatbot Data Model

## Entity: ContentChunk

### Description
Represents a semantic chunk of textbook content that has been embedded for RAG retrieval.

### Fields
- **id** (string, required)
  - Unique identifier for the content chunk
  - Auto-generated UUID
  - Primary key for the entity

- **content** (string, required)
  - The actual text content (200-500 words)
  - Semantic unit of information from textbook
  - Stored as plain text

- **chapter** (string, required)
  - Chapter identifier where this content belongs
  - Format: "chapter-{number}-{slug}"
  - Used for navigation and organization

- **lesson** (string, required)
  - Lesson identifier within the chapter
  - Format: "lesson-{number}-{slug}"
  - Used for navigation and organization

- **section** (string, optional)
  - Section within the lesson (if applicable)
  - Used for more granular navigation

- **url** (string, required)
  - URL to the specific location in the textbook
  - Used for navigation links in responses
  - Format: relative path from textbook root

- **embedding** (float[384], required)
  - 384-dimensional vector embedding of the content
  - Generated using Qdrant FastEmbed (BAAI/bge-small-en-v1.5)
  - Used for semantic similarity search

### Relationships
- None (standalone entity for vector storage)

### Validation Rules
- content must be between 200 and 500 words
- chapter, lesson, and url must be valid formats
- embedding must be exactly 384 dimensions
- content cannot be empty or only whitespace

## Entity: ChatMessage

### Description
Represents a single message in a chat conversation between user and assistant.

### Fields
- **id** (string, required)
  - Unique identifier for the message
  - Auto-generated UUID

- **role** (enum, required)
  - Role of the message sender
  - Values: "user", "assistant", "system"
  - Determines message styling and behavior

- **content** (string, required)
  - The actual message content
  - Text content of the message

- **sources** (array of objects, optional)
  - Source references used in the response
  - Format: [{url: string, title: string, relevance: number}]

- **timestamp** (datetime, required)
  - When the message was created
  - ISO 8601 format
  - Used for ordering messages in conversation

### Relationships
- Belongs to a ChatSession (via session_id in context)

### Validation Rules
- role must be one of the allowed values
- content must not exceed 10,000 characters
- sources array items must have valid URL format
- timestamp must be in valid ISO 8601 format

## Entity: ChatSession

### Description
Represents a conversation session between user and the RAG chatbot.

### Fields
- **session_id** (string, required)
  - Unique identifier for the conversation session
  - Auto-generated UUID
  - Used to maintain conversation context

- **messages** (array of ChatMessage, required)
  - List of messages in the session
  - Maintains conversation history
  - Limited to last 50 messages to prevent memory issues

- **created_at** (datetime, required)
  - When the session was created
  - ISO 8601 format

- **current_page** (string, optional)
  - Current page URL where the chat was initiated
  - Used for context in responses

- **expires_at** (datetime, required)
  - When the session expires (24 hours after last activity)
  - ISO 8601 format
  - Used for automatic cleanup

### Relationships
- Contains multiple ChatMessage entities (via messages array)

### Validation Rules
- session_id must be unique
- messages array must not exceed 50 items
- created_at and expires_at must be in valid ISO 8601 format
- expires_at must be 24 hours after last activity
- current_page must be valid URL format if provided

## Indexes & Performance

### ContentChunk Indexes
- embedding (vector index for similarity search)
- chapter, lesson (composite index for navigation queries)
- url (unique index to prevent duplicates)

### ChatSession Indexes
- session_id (unique index for fast lookup)
- expires_at (expiration index for cleanup)

## Constraints
- ContentChunk embeddings must be 384-dimensional vectors
- ChatSession messages are limited to 50 most recent messages
- ChatSession expires after 24 hours of inactivity
- ContentChunk URLs must be unique to prevent duplication