# Quickstart: Workflow Integration

**Feature**: Workflow Integration  
**Version**: 1.0.0  
**Date**: 2025-12-23

## Overview

The Workflow Integration feature provides a unified API endpoint to trigger the textbook content generation workflow, integrating Content Architect, Lesson Template Generator, Technical Writer, validation scripts, error handling, edge case handling, RAG indexing, and frontend synchronization.

## Prerequisites

- Backend API running on `http://localhost:8000`
- Authentication token (JWT) for API access
- Existing workflow components available:
  - Content Architect subagent (`.claude/agents/content-architect.md`)
  - Lesson Template Generator skill (`.claude/skills/lesson-template-generator/SKILL.md`)
  - Technical Writer agent (`.claude/agents/technical-writer.md`)
- Error handler, edge case handler, and validation scripts in `specs/book-writing/scripts/`
- RAG indexing service configured and accessible

## Installation & Setup

### 1. Verify Backend API is Running

```bash
# Check health endpoint
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### 2. Obtain Authentication Token

```bash
# Login to get JWT token (example)
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'
```

Save the token from the response for use in API requests.

### 3. Verify Workflow Components

Ensure the following components are available:
- Content Architect: `.claude/agents/content-architect.md`
- Lesson Template Generator: `.claude/skills/lesson-template-generator/SKILL.md`
- Technical Writer: `.claude/agents/technical-writer.md`
- Error handler: `specs/book-writing/scripts/error-handler.py`
- Edge case handler: `specs/book-writing/scripts/edge-case-handler.py`
- Validation scripts: `specs/book-writing/scripts/validate-*.py`

## Basic Usage

### 1. Create Content Generation Job

```bash
curl -X POST http://localhost:8000/api/content/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "chapters": ["1", "2", "3"],
    "lessons": ["1", "2"],
    "target_word_count": 800,
    "priority": "normal"
  }'
```

**Response (202 Accepted)**:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "message": "Content generation job created",
  "estimated_completion_time": 300
}
```

### 2. Check Job Status

Poll the status endpoint every 30 seconds:

```bash
curl -X GET http://localhost:8000/api/content/generate/550e8400-e29b-41d4-a716-446655440000 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response (200 OK)** - In Progress:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "in_progress",
  "progress": 45.5,
  "current_step": "Generating content for lesson 1.2",
  "created_at": "2025-12-23T10:00:00Z",
  "started_at": "2025-12-23T10:00:01Z",
  "component_statuses": {
    "content_architect": "completed",
    "template_generator": "completed",
    "technical_writer": "in_progress"
  }
}
```

**Response (200 OK)** - Completed:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress": 100.0,
  "current_step": "Content generation completed",
  "created_at": "2025-12-23T10:00:00Z",
  "started_at": "2025-12-23T10:00:01Z",
  "completed_at": "2025-12-23T10:05:15Z",
  "results": {
    "total_lessons": 6,
    "successful_lessons": 6,
    "failed_lessons": 0,
    "content_locations": [
      "frontend/textbook-content/chapter-1-introduction/lesson-1-what-is-physical-ai.md",
      "frontend/textbook-content/chapter-1-introduction/lesson-2-history-and-evolution.md"
    ],
    "generation_time": 245.3
  },
  "validation_results": {
    "overall_status": "passed",
    "word_count_validation": {
      "status": "passed",
      "target_word_count": 800,
      "actual_word_count": 812,
      "variance": 1.5
    },
    "source_validation": {
      "status": "passed",
      "authoritative_sources": 4,
      "min_required": 3
    }
  },
  "indexing_status": "completed",
  "sync_status": "completed"
}
```

### 3. Cancel Job (if needed)

```bash
curl -X POST http://localhost:8000/api/content/generate/550e8400-e29b-41d4-a716-446655440000/cancel \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Advanced Usage

### With Research Guidance

Provide specific research guidance for each lesson:

```bash
curl -X POST http://localhost:8000/api/content/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "chapters": ["1"],
    "lessons": ["1", "2"],
    "research_guidance": {
      "1.1": "Focus on embodied intelligence definition and sensor-motor integration. Examples: Tesla Optimus, Figure 01.",
      "1.2": "Cover history from Brooks 1991 paper to modern robots. Include Boston Dynamics Atlas."
    },
    "target_word_count": 800
  }'
```

### Handling Errors

**Error Response (400 Bad Request)**:
```json
{
  "error": "validation_error",
  "message": "Invalid chapters format",
  "details": {
    "field": "chapters",
    "issue": "Chapters must be non-empty"
  }
}
```

**Error Response (429 Rate Limit Exceeded)**:
```json
{
  "error": "rate_limit_exceeded",
  "message": "Too many content generation requests. Please try again later.",
  "details": {
    "retry_after": 3600
  }
}
```

**Job Failed Response**:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "failed",
  "progress": 35.0,
  "error": {
    "error_type": "component_failure",
    "component": "technical_writer",
    "message": "Failed to generate content for lesson 1.2: Insufficient sources",
    "recovery_suggestions": [
      "Provide more specific research guidance",
      "Check source availability",
      "Retry with different lesson specifications"
    ],
    "retryable": true,
    "occurred_at": "2025-12-23T10:02:30Z"
  }
}
```

## Python Client Example

```python
import requests
import time
from typing import Optional, Dict

class ContentGenerationClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def create_job(self, 
                   chapters: list,
                   lessons: Optional[list] = None,
                   research_guidance: Optional[Dict[str, str]] = None,
                   target_word_count: int = 800) -> str:
        """Create a content generation job and return job_id"""
        payload = {
            "chapters": chapters,
            "lessons": lessons,
            "research_guidance": research_guidance,
            "target_word_count": target_word_count
        }
        response = requests.post(
            f"{self.base_url}/api/content/generate",
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()["job_id"]
    
    def get_status(self, job_id: str) -> dict:
        """Get job status"""
        response = requests.get(
            f"{self.base_url}/api/content/generate/{job_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def wait_for_completion(self, job_id: str, poll_interval: int = 30) -> dict:
        """Wait for job completion, polling every poll_interval seconds"""
        while True:
            status = self.get_status(job_id)
            if status["status"] in ["completed", "failed", "cancelled"]:
                return status
            time.sleep(poll_interval)

# Usage
client = ContentGenerationClient(
    base_url="http://localhost:8000",
    token="YOUR_JWT_TOKEN"
)

job_id = client.create_job(
    chapters=["1", "2", "3"],
    lessons=["1", "2"],
    target_word_count=800
)

print(f"Job created: {job_id}")

final_status = client.wait_for_completion(job_id)
print(f"Job completed: {final_status['status']}")
if final_status["status"] == "completed":
    print(f"Generated {final_status['results']['successful_lessons']} lessons")
```

## JavaScript/TypeScript Client Example

```typescript
class ContentGenerationClient {
  constructor(
    private baseUrl: string,
    private token: string
  ) {}

  async createJob(
    chapters: string[],
    lessons?: string[],
    researchGuidance?: Record<string, string>,
    targetWordCount: number = 800
  ): Promise<string> {
    const response = await fetch(`${this.baseUrl}/api/content/generate`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        chapters,
        lessons,
        research_guidance: researchGuidance,
        target_word_count: targetWordCount
      })
    });
    
    if (!response.ok) {
      throw new Error(`Failed to create job: ${response.statusText}`);
    }
    
    const data = await response.json();
    return data.job_id;
  }

  async getStatus(jobId: string): Promise<any> {
    const response = await fetch(
      `${this.baseUrl}/api/content/generate/${jobId}`,
      {
        headers: {
          'Authorization': `Bearer ${this.token}`
        }
      }
    );
    
    if (!response.ok) {
      throw new Error(`Failed to get status: ${response.statusText}`);
    }
    
    return response.json();
  }

  async waitForCompletion(
    jobId: string,
    pollInterval: number = 30000
  ): Promise<any> {
    return new Promise((resolve) => {
      const poll = async () => {
        const status = await this.getStatus(jobId);
        if (['completed', 'failed', 'cancelled'].includes(status.status)) {
          resolve(status);
        } else {
          setTimeout(poll, pollInterval);
        }
      };
      poll();
    });
  }
}

// Usage
const client = new ContentGenerationClient(
  'http://localhost:8000',
  'YOUR_JWT_TOKEN'
);

const jobId = await client.createJob(
  ['1', '2', '3'],
  ['1', '2'],
  undefined,
  800
);

console.log(`Job created: ${jobId}`);

const finalStatus = await client.waitForCompletion(jobId);
console.log(`Job completed: ${finalStatus.status}`);
```

## Integration with Frontend

After content generation completes:

1. **Content is automatically indexed in RAG**: The generated content is indexed in Qdrant and searchable via the RAG chatbot
2. **Frontend auto-detects new content**: Docusaurus reads from `frontend/textbook-content/` directory
3. **Rebuild frontend** (if needed): For production, trigger Docusaurus rebuild:
   ```bash
   npm run build
   ```

## Environment Variables

Backend requires:
- `GEMINI_API_KEY`: Google Gemini API key (for RAG)
- `QDRANT_URL`: Qdrant Cloud URL
- `QDRANT_API_KEY`: Qdrant API key
- `FRONTEND_URL`: Frontend URL (for CORS)
- `JWT_SECRET`: JWT secret for authentication

## Next Steps

1. Implement the workflow orchestrator service
2. Create API route handlers
3. Integrate error and edge case handlers
4. Add validation service wrapper
5. Implement RAG indexing integration
6. Add frontend sync service

