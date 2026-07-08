# 🚀 CareerPrep AI - AI Powered Career Preparation Assistant

CareerPrep AI is an **Agentic AI-powered career preparation platform** that automatically generates personalized career preparation guides for different technical roles.

The system uses **Large Language Models (LLMs), Retrieval Augmented Generation (RAG), LangGraph multi-agent workflows, and vector databases** to provide structured interview preparation material including:

- Role introduction
- Required skills
- Learning roadmap
- Interview questions
- Projects recommendations
- Learning resources
- Career guidance
- Downloadable PDF preparation guides

---

# 🌟 Features

## 1. AI Career Guide Generation

Users provide a target role such as:

- AI Engineer
- Software Engineer
- Data Engineer
- DevOps Engineer
- Full Stack Developer

The system generates a complete preparation guide.

Generated content includes:

### Introduction
- Role overview
- Responsibilities
- Required technical skills
- Industry expectations

### Learning Roadmap
- Beginner concepts
- Intermediate skills
- Advanced topics
- Practical milestones

### Interview Preparation
- Technical interview questions
- Concept-based questions
- System design questions
- Role-specific questions

### Projects
- Beginner projects
- Intermediate projects
- Advanced portfolio projects

### Resources
- Documentation
- Courses
- Books
- Practice platforms

---

# 🏗️ System Architecture


```
                User
                 |
                 |
          React Frontend
                 |
                 |
          FastAPI Backend
                 |
                 |
          LangGraph Workflow
                 |
    --------------------------------
    |              |               |
Planner Agent   RAG Agents    PDF Generator
                    |
                    |
              AstraDB Vector DB
                    |
                    |
             LLM Providers
```

---

# 🧠 AI Technologies Used

## Large Language Models

The application uses LLMs for:

- Understanding user requirements
- Generating career guides
- Answer generation
- Content refinement


Supported providers:

- Groq LLM
- Hugging Face Models


---

# 🔗 LangChain

LangChain is used for:

- LLM orchestration
- Prompt management
- Retrieval pipelines
- Document processing
- Chain creation


Main components:

- Prompt Templates
- LLM Chains
- Retrievers
- Document loaders
- Output parsing


---

# 🔄 LangGraph Agent Workflow

CareerPrep AI uses LangGraph to build an agentic workflow.

The workflow consists of multiple specialized nodes.

## Workflow


```
User Query

      |
      ↓

Analyze Request Node

      |
      ↓

Parallel RAG Agents

      |
      |
      ├── Introduction Agent
      |
      ├── Roadmap Agent
      |
      ├── Interview Agent
      |
      ├── Projects Agent
      |
      └── Resources Agent


      |
      ↓

Merge Node

      |
      ↓

PDF Generator

      |
      ↓

Final Career Guide
```

---

# 🤖 AI Agents

## 1. Request Analyzer Agent

Responsibilities:

- Understand user requirements
- Identify target role
- Extract required sections


---

## 2. Introduction RAG Agent

Generates:

- Role overview
- Responsibilities
- Skills requirements


---

## 3. Roadmap RAG Agent

Creates:

- Learning path
- Required technologies
- Skill progression


---

## 4. Interview RAG Agent

Generates:

- Technical questions
- Conceptual questions
- Interview preparation material


---

## 5. Project Recommendation Agent

Provides:

- Portfolio projects
- Implementation ideas
- Difficulty levels


---

## 6. Resource Agent

Provides:

- Documentation
- Courses
- Books
- Learning resources


---

# 📚 Retrieval Augmented Generation (RAG)

CareerPrep AI uses RAG to improve response quality.

Instead of relying only on LLM knowledge:

```
User Query

    ↓

Retrieve Relevant Documents

    ↓

Context Injection

    ↓

LLM Generation

    ↓

Final Answer
```

Benefits:

- Reduces hallucination
- Provides domain-specific answers
- Uses updated knowledge
- Improves accuracy


---

# 🗄️ Vector Database

## AstraDB

CareerPrep AI uses:

**DataStax AstraDB**

as the vector database.


Used for:

- Storing document embeddings
- Semantic search
- Context retrieval


Architecture:


```
Documents

   ↓

Text Chunking

   ↓

Embedding Model

   ↓

AstraDB Vector Store

   ↓

Similarity Search

   ↓

LLM Context
```


Advantages:

- Cloud hosted
- Scalable
- Production ready
- No local storage dependency


---

# 🔎 Search Integration

## Tavily Search API

Used for:

- Finding updated interview information
- Fetching latest resources
- External knowledge retrieval


---

# 🖥️ Backend Technology Stack

## FastAPI

Backend framework used for:

- REST APIs
- Request handling
- API routing
- Backend services


Backend structure:

```
backend/

│
├── app/
│
├── api/
│   ├── guide.py
│   └── health.py
│
├── nodes/
│   ├── roadmap_RAG.py
│   ├── interview_RAG.py
│   ├── projects_RAG.py
│   └── resources_RAG.py
│
├── retrievers/
│
├── services/
│
├── schemas/
│
├── prompts/
│
├── graph.py
│
└── main.py
```

---

# 🎨 Frontend Technology Stack

Frontend is built using:

## React

Used for:

- UI components
- State management
- User interaction


## Vite

Used as:

- Development server
- Build tool


## TypeScript

Used for:

- Type safety
- Better maintainability


## Tailwind CSS

Used for:

- Responsive UI
- Styling


## Additional Libraries

### React Query

Used for:

- API state management
- Data fetching


### Axios

Used for:

- Backend API communication


### Framer Motion

Used for:

- Animations


### React Markdown

Used for:

- Rendering generated guides


---

# 📄 PDF Generation

The system generates downloadable career preparation PDFs.

Generated guides include:

- Structured sections
- Markdown conversion
- Professional formatting


Example:

```
AI_Engineer_Career_Guide.pdf
Software_Engineer_Career_Guide.pdf
```

---

# 🔐 Environment Variables

Create:

```
.env
```

Example:

```env

# AstraDB
ASTRA_DB_API_ENDPOINT=
ASTRA_DB_APPLICATION_TOKEN=
ASTRA_DB_NAMESPACE=


# LLM
GROQ_API_KEY=

# HuggingFace
HF_TOKEN=

# Search
TAVILY_API_KEY=

```

Never commit `.env` to GitHub.

---

# ⚙️ Installation

## Clone Repository


```bash
git clone https://github.com/Noore-hira/CareerPrep_AI.git

cd CareerPrep_AI
```


---

# Backend Setup


Navigate:

```bash
cd backend
```


Create environment:

```bash
python -m venv .venv
```


Activate:

Windows:

```bash
.venv\Scripts\activate
```


Install dependencies:


```bash
pip install -r requirements.txt
```


Run backend:


```bash
uvicorn app.main:app --reload
```


Backend runs:

```
http://localhost:8000
```


Swagger documentation:

```
http://localhost:8000/docs
```


---

# Frontend Setup


Navigate:

```bash
cd frontend
```


Install dependencies:

```bash
pnpm install
```


Run:

```bash
pnpm dev
```


Frontend runs:

```
http://localhost:5173
```


---

# 🚀 Deployment


## Backend Deployment

Backend can be deployed on:

- Render
- AWS
- Google Cloud
- Azure


Production command:


```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```


Environment variables are configured through deployment platform.


---

## Frontend Deployment

Frontend can be deployed on:

- Vercel
- Netlify


Production build:

```bash
pnpm build
```


---

# 🔒 Security

Implemented:

- Environment variable protection
- API key isolation
- CORS configuration


Production CORS:

```python
allow_origins=[
"https://your-frontend-domain.com"
]
```

---

# 📈 Future Improvements

Possible enhancements:

- User authentication
- Saved career paths
- Progress tracking
- AI mock interviewer
- Voice interview simulation
- Resume analysis
- LinkedIn profile analysis
- Personalized learning plans
- Multi-language support


---

# 👨‍💻 Author

Developed as an AI Engineering project demonstrating:

- Generative AI
- Agentic workflows
- RAG systems
- LLM applications
- Full-stack AI development


---

# ⭐ Tech Stack Summary

| Category | Technology |
|-|-|
| Frontend | React, TypeScript, Vite, Tailwind CSS |
| Backend | FastAPI |
| AI Framework | LangChain |
| Agent Framework | LangGraph |
| Vector Database | AstraDB |
| LLM | Groq / HuggingFace |
| Search | Tavily |
| API Communication | Axios |
| PDF Generation | Python PDF Libraries |
| Deployment | Render + Vercel |

