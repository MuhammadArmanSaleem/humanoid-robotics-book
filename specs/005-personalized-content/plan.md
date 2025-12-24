# Personalized Content Implementation Plan

## Summary

This plan outlines the implementation of a comprehensive personalized content delivery system that adapts textbook content based on user background, preferences, and learning goals. The system will integrate with the existing RAG chatbot to provide customized learning experiences for students in the Physical AI & Humanoid Robotics textbook.

## Technical Approach

### Backend Architecture
- **Framework**: FastAPI with Python 3.11+
- **Database**: PostgreSQL with asyncpg for async operations
- **Authentication**: JWT tokens with bcrypt password hashing
- **Package Manager**: uv in api/ directory
- **Dependencies**: psycopg2-binary, passlib, bcrypt, python-jose, python-multipart

### Frontend Architecture
- **Framework**: React with TypeScript
- **Integration**: Docusaurus theme swizzling
- **Styling**: CSS Modules for scoped styles
- **State Management**: React Context API for auth state

### Personalization Engine
- **LLM Integration**: Gemini 1.5 Flash via OpenAI Agents SDK
- **Content Adaptation**: Based on user background and preferences
- **Caching**: PostgreSQL-based caching for personalized content
- **Real-time**: On-demand personalization with caching fallback

## Project Structure

```
api/ (backend)
├── src/
│   ├── main.py (FastAPI app with all routes)
│   ├── config.py (database and auth settings)
│   ├── models.py (Pydantic models for auth and personalization)
│   ├── database/ (connection and models)
│   │   └── models.py (SQLAlchemy models)
│   ├── services/
│   │   ├── auth_service.py (user registration/login)
│   │   ├── personalization_service.py (content adaptation)
│   │   └── user_service.py (user profile and background)
│   └── utils/
│       ├── auth.py (JWT utilities)
│       └── db.py (database utilities)
├── scripts/ (migration and setup scripts)
├── requirements.txt (dependencies)
└── .env.example (environment variables)

docs/ (frontend)
├── src/
│   ├── contexts/ (React Context providers)
│   │   └── AuthContext.tsx (authentication state management)
│   ├── pages/ (auth pages)
│   │   ├── signup.tsx (signup page component)
│   │   └── signin.tsx (signin page component)
│   ├── components/ (auth UI components)
│   │   └── NavbarAuth/ (navbar auth dropdown)
│   └── theme/ (Docusaurus overrides)
│       └── Root.jsx (global providers)
```

## Implementation Phases

### Phase 0: Research & Setup (2-3 hours)
- [ ] Set up PostgreSQL database (local/Cloud)
- [ ] Verify PostgreSQL connection and asyncpg compatibility
- [ ] Install authentication dependencies with uv
- [ ] Create .env.example with DATABASE_URL and JWT_SECRET_KEY
- [ ] Set up database models and connection utilities
- [ ] Test basic database operations

### Phase 1: User Authentication & Background Collection (4-5 hours) - P0
- [ ] Create Pydantic models for authentication (SignupRequest, SigninRequest, UserResponse)
- [ ] Implement user registration with bcrypt password hashing
- [ ] Create JWT token generation and validation utilities
- [ ] Implement login/logout functionality with proper session management
- [ ] Create user background collection (software/hardware experience, programming languages, etc.)
- [ ] Implement database CRUD operations for users and backgrounds
- [ ] Add authentication middleware for protected routes
- [ ] Test all auth endpoints and database operations

### Phase 2: Frontend Authentication UI (3-4 hours) - P0
- [ ] Create AuthContext with signup, signin, signout functions
- [ ] Implement signup page with form validation and background collection
- [ ] Implement signin page with proper error handling
- [ ] Create user profile dropdown in navbar
- [ ] Integrate auth state with Docusaurus theme swizzling
- [ ] Add password visibility toggles with eye icons
- [ ] Implement responsive design for auth UI
- [ ] Test frontend auth flow with backend integration

### Phase 3: Content Personalization Engine (3-4 hours) - P1
- [ ] Create personalization service using Gemini API
- [ ] Implement content adaptation based on user background
- [ ] Add caching layer for personalized content
- [ ] Create personalization rules engine
- [ ] Implement "Personalize for Me" button functionality
- [ ] Add difficulty adjustment based on experience levels
- [ ] Implement programming language customization for examples
- [ ] Test personalization accuracy and performance

### Phase 4: Learning Path Generation (2-3 hours) - P2
- [ ] Create learning path algorithm based on user goals
- [ ] Implement prerequisite checking for content sequencing
- [ ] Add progress tracking for learning paths
- [ ] Create visualization for learning path progress
- [ ] Implement path adaptation based on user progress
- [ ] Add multiple path options for different goals
- [ ] Test learning path generation and adaptation

### Phase 5: Progress Tracking & Adaptation (2-3 hours) - P3
- [ ] Implement user progress tracking system
- [ ] Create progress synchronization across devices
- [ ] Add content adaptation based on progress history
- [ ] Implement bookmarking functionality
- [ ] Create progress summary and analytics
- [ ] Add performance-based content recommendations
- [ ] Test progress tracking accuracy and synchronization

### Phase 6: Integration & Polish (2-3 hours)
- [ ] Integrate personalization with existing RAG chatbot
- [ ] Add proper error handling and validation
- [ ] Implement security measures (rate limiting, input validation)
- [ ] Optimize database queries and add proper indexing
- [ ] Add comprehensive logging and monitoring
- [ ] Perform final testing and bug fixes
- [ ] Update documentation and deployment configuration

## Key Technical Decisions

### Decision 1: JWT Tokens vs Server-Side Sessions
- **Chosen**: JWT tokens with 7-day expiration
- **Rationale**: Stateless, scales better, no session table queries
- **Trade-off**: Can't revoke tokens before expiry (mitigated by short expiration)

### Decision 2: PostgreSQL Arrays vs JSON for Programming Languages
- **Chosen**: PostgreSQL arrays with proper adapter registration
- **Rationale**: Type-safe, efficient querying, native database support
- **Alternative**: JSON column (rejected - less type-safe for array operations)

### Decision 3: bcrypt Version Pinning
- **Chosen**: bcrypt==4.0.1 (pinned version)
- **Rationale**: Latest bcrypt versions have compatibility issues with passlib
- **Trade-off**: Pinned version vs auto-updates (chose stability)

### Decision 4: User Profile vs Dropdown Menu
- **Chosen**: User dropdown menu with quick actions
- **Rationale**: Better UX, quick access to common actions (language toggle, theme toggle, sign out)
- **Benefit**: All user actions in one accessible location

## Non-Functional Requirements

### Performance
- Authentication requests: <500ms response time
- Personalized content generation: <2s response time
- Database operations optimized for 100+ concurrent users
- Caching layer to reduce LLM API calls

### Security
- bcrypt password hashing (12 rounds)
- JWT tokens with proper validation
- HTTP-only cookies to prevent XSS
- Parameterized SQL queries to prevent injection
- Rate limiting for auth endpoints (60 requests/minute)

### Scalability
- Async database operations with connection pooling
- Caching layer for personalized content
- Stateless authentication with JWT
- Proper database indexing for performance

## Deployment Strategy

### Backend Deployment
- **Docker**: Multi-stage build with security optimizations
- **Render**: Free tier with environment variable configuration
- **Railway**: Nixpacks build configuration
- **Hugging Face Spaces**: Docker SDK compatibility

### Database Setup
- **PostgreSQL**: Cloud service or local setup
- **Migration**: Automated schema setup with proper initialization
- **Connection Pooling**: Proper asyncpg connection management

## Risk Analysis

### Risk 1: JWT Token Revocation
- **Impact**: High - Can't immediately revoke compromised tokens
- **Probability**: Medium - Tokens are stateless
- **Mitigation**: Short 7-day expiration, implement token blacklist in future if needed

### Risk 2: Database Connection Issues
- **Impact**: High - Authentication and personalization require database
- **Probability**: Low - Using proven asyncpg library
- **Mitigation**: Connection pooling, proper error handling, fallback mechanisms

### Risk 3: LLM API Costs
- **Impact**: Medium - Personalization uses Gemini API
- **Probability**: Medium - Caching reduces but doesn't eliminate API calls
- **Mitigation**: Aggressive caching, usage monitoring, fallback content

### Risk 4: bcrypt Compatibility
- **Impact**: Medium - Authentication fails if incompatible
- **Probability**: Low - Using pinned version
- **Mitigation**: Version pinning, compatibility testing

## Evaluation Criteria

### Testing Approach
- **Unit Tests**: Service layer functionality (pytest + pytest-asyncio)
- **Integration Tests**: API endpoint validation (pytest + TestClient)
- **Frontend Tests**: Component and integration tests (Jest + React Testing Library)
- **Security Tests**: Authentication and authorization validation
- **Performance Tests**: Load testing for concurrent users

### Success Metrics
- All auth endpoints return correct status codes (200, 201, 401, 404)
- User registration and login work correctly with proper validation
- Session management persists across page refreshes
- Content personalization adapts based on user background (90%+ accuracy)
- Database operations optimized for <500ms response time
- No security vulnerabilities in auth flow
- Responsive design works on all device sizes

## Dependencies & Versioning

### Backend Dependencies
- FastAPI: >=0.104.1
- PostgreSQL: >=13.0 (with asyncpg support)
- bcrypt: ==4.0.1 (pinned for passlib compatibility)
- passlib: >=1.7.4
- python-jose: >=3.3.0 (with cryptography)
- psycopg2-binary: >=2.9.9
- python-multipart: >=0.0.6

### Frontend Dependencies
- React: >=18.0.0
- TypeScript: >=4.9.0
- Docusaurus: >=3.0.0

## Operational Readiness

### Monitoring
- API response times and error rates
- Database connection pool metrics
- Authentication success/failure rates
- Personalization cache hit rates

### Logging
- Authentication events (login, logout, registration)
- Personalization requests and results
- Error logging with proper sanitization
- Performance metrics logging

### Maintenance
- Database backup procedures
- Cache invalidation strategies
- Token rotation mechanisms
- Dependency update procedures

## Time Estimates

- **Phase 0**: 2-3 hours (Setup and configuration)
- **Phase 1**: 4-5 hours (Core auth implementation)
- **Phase 2**: 3-4 hours (Frontend UI implementation)
- **Phase 3**: 3-4 hours (Personalization engine)
- **Phase 4**: 2-3 hours (Learning paths)
- **Phase 5**: 2-3 hours (Progress tracking)
- **Phase 6**: 2-3 hours (Integration and polish)
- **Total**: 18-25 hours

## Zero-Cost Architecture

- PostgreSQL: Free tier options available (Neon, Supabase)
- FastAPI: Open source
- Authentication: Self-hosted with JWT
- Content personalization: Using existing Gemini API (free tier)
- Frontend: Static hosting (GitHub Pages with Docusaurus)
- No additional recurring costs beyond existing infrastructure