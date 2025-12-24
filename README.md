# Physical AI & Humanoid Robotics Textbook

A comprehensive textbook and learning platform for Physical AI and Humanoid Robotics with personalized content delivery.

## 🏗️ Project Structure

```
.
├── backend/                    # FastAPI backend with authentication & personalization
│   ├── src/
│   │   ├── main.py            # Main application
│   │   ├── config.py          # Configuration settings
│   │   ├── models.py          # Pydantic models
│   │   ├── database/          # SQLAlchemy models
│   │   ├── services/          # Business logic services
│   │   ├── routes/            # API route definitions
│   │   └── utils/             # Utility functions
│   ├── scripts/               # Database scripts
│   ├── requirements.txt       # Python dependencies
│   └── .env.example          # Environment variables template
├── frontend/                  # Textbook content (Docusaurus docs)
│   └── textbook-content/      # Chapter and lesson markdown files
├── src/                       # Frontend React components
│   ├── components/            # Reusable UI components
│   ├── contexts/              # React Context providers
│   ├── pages/                 # Auth pages (signup, signin)
│   ├── theme/                 # Docusaurus theme overrides
│   └── css/                   # Custom CSS
├── docusaurus.config.js       # Docusaurus configuration
├── sidebars.ts               # Documentation sidebar configuration
└── package.json              # Node.js dependencies
```

## 🚀 Getting Started

### Prerequisites

- Node.js (v18 or higher)
- Python 3.11+
- PostgreSQL database
- Google Gemini API key
- Qdrant Cloud account

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your actual values
```

4. Run database migrations:
```bash
python scripts/create_tables.py
```

5. Start the backend server:
```bash
uvicorn src.main:app --reload
```

### Frontend Setup

1. Install Node.js dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run start
```

## 🔐 Authentication Features

- User registration with background information
- Secure login/logout with JWT tokens
- Password visibility toggles
- User profile dropdown with settings
- Language toggle (English/Urdu)
- Theme toggle (Light/Dark)

## 🎯 Personalization Engine

- Content adaptation based on user background
- Programming language preference customization
- Experience level-based difficulty adjustment
- Learning path generation
- Progress tracking

## 🌐 API Endpoints

### Authentication
- `POST /api/auth/signup` - User registration
- `POST /api/auth/signin` - User login
- `POST /api/auth/signout` - User logout
- `GET /api/auth/me` - Get current user

### User Management
- `GET /api/user/background` - Get user background
- `PUT /api/user/background` - Update user background

### Personalization
- `POST /api/personalize/{content_id}` - Get personalized content
- `GET /api/personalize/learning-path` - Get learning path

## 📚 Textbook Content

The textbook is organized into chapters and lessons:

- **Chapter 1**: Introduction to Physical AI
- **Chapter 2**: Fundamentals of Humanoid Robotics
- **Chapter 3**: Advanced Topics

Each chapter contains multiple lessons covering specific topics in depth.

## 🚀 Deployment

### Backend
The backend can be deployed to:
- Render (free tier)
- Railway
- Hugging Face Spaces
- Any platform supporting Python/FastAPI

### Frontend
The frontend (Docusaurus) can be deployed to:
- GitHub Pages
- Netlify
- Vercel
- Any static hosting service

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.