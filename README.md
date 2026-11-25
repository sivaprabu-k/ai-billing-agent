# Autonomous AI Billing & Dispute Resolution System

An AI-powered billing and dispute resolution platform designed to automate billing investigations, analyze invoice discrepancies, retrieve billing policies, and recommend appropriate resolutions using Agentic AI.

The system combines **FastAPI, React, LangChain, LangGraph, Gemini, PostgreSQL, and RAG** to provide an intelligent and transparent billing management experience.

---

## Project Overview

The Autonomous AI Billing & Dispute Resolution System helps businesses manage billing operations and investigate customer disputes through an AI-powered workflow.

Instead of manually investigating every billing issue, users can interact with an AI billing assistant that can:

- Investigate invoice discrepancies.
- Analyze subscription and usage information.
- Calculate overage charges.
- Retrieve relevant billing and refund policies.
- Recommend dispute resolutions.
- Initiate credit adjustment requests.
- Request human approval for high-value adjustments.
- Maintain audit records of billing operations.

Financial calculations and authorization decisions are handled by deterministic backend logic rather than relying on LLM-generated financial values.

---

## Key Features

### 1. Authentication & Authorization
- User registration and login.
- JWT access and refresh tokens.
- Session management.
- Password hashing and password changes.
- Protected API endpoints.
- User-specific resource access.

### 2. Subscription Management
- Manage subscription plans.
- Track customer subscriptions.
- Configure pricing and usage limits.
- Monitor subscription status.

### 3. Usage Tracking
- Record customer usage.
- Track included usage limits.
- Calculate additional usage.
- Identify overage charges.

### 4. Invoice Management
- Generate invoices.
- Maintain invoice line items.
- Calculate subscription and overage charges.
- Investigate invoice discrepancies.

### 5. AI Billing Analyst
- Retrieve customer billing information.
- Analyze usage and invoice records.
- Perform deterministic billing calculations.
- Identify billing inconsistencies.

### 6. Policy Research with RAG
- Retrieve billing policies.
- Search refund and cancellation policies.
- Retrieve overage pricing rules.
- Provide policy-grounded recommendations with references.

### 7. AI Dispute Resolution
- Investigate billing disputes.
- Compare invoice amounts with calculated charges.
- Classify dispute types.
- Recommend suitable resolutions.

### 8. Credit & Refund Management
- Validate credit requests.
- Apply financial approval rules.
- Require human approval for high-value adjustments.
- Simulate credit transactions.
- Maintain transaction history.

### 9. Audit Logging
- Record important billing operations.
- Track credit adjustments.
- Maintain investigation history.
- Support operational transparency.

### 10. Observability
- Monitor AI execution.
- Track LLM calls and latency.
- Monitor token usage and errors.
- Evaluate AI responses using Langfuse.

---

## Technology Stack

| Category | Technologies |
|---|---|
| Frontend | React, TypeScript |
| Styling | Tailwind CSS v4 |
| Icons | Lucide React |
| Charts | Recharts |
| Routing | React Router |
| Backend | Python, FastAPI |
| AI Model | Google Gemini 2.5 Flash |
| AI Framework | LangChain |
| Agent Orchestration | LangGraph |
| Database | PostgreSQL |
| Vector Database | PostgreSQL + pgvector |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Validation | Pydantic |
| Authentication | JWT |
| Password Hashing | Argon2 |
| RAG | Embeddings, Vector Search, Hybrid Retrieval |
| Observability | Langfuse |
| Deployment | Docker (planned) |

---

## System Architecture

The application follows a modular architecture with separate frontend, backend, AI orchestration, and database layers.

```text
                 React Frontend
                       |
                       |
                 FastAPI Backend
                       |
              Authentication Layer
                       |
                API Router Layer
                       |
              Business Service Layer
                       |
          +------------+------------+
          |            |            |
      Billing      Subscription   Invoice
      Services       Services     Services
          |            |            |
          +------------+------------+
                       |
                Agentic AI Layer
                       |
                Supervisor Agent
                       |
          +------------+------------+
          |            |            |
       Billing       Policy       Dispute
       Analyst      Research     Resolution
          Agent       Agent        Agent
          |            |            |
          +------------+------------+
                       |
                 Credit Agent
                       |
               Human Approval
                       |
          +------------+------------+
          |                         |
      PostgreSQL                pgvector
   Structured Data            Policy Data
          |
       Langfuse
     Observability
```

---

## Multi-Agent Architecture

The system is designed around five specialized AI agents.

| Agent | Responsibility |
|---|---|
| Billing Analyst Agent | Investigates invoices, subscriptions, and usage |
| Policy Research Agent | Retrieves relevant billing and refund policies using RAG |
| Dispute Resolution Agent | Analyzes disputes and recommends resolutions |
| Refund/Credit Agent | Validates and processes authorized credit adjustments |
| Supervisor Agent | Coordinates agents and manages workflow execution |

LangGraph is used to orchestrate agent execution, conditional routing, and human approval workflows.

---

## Project Structure

```text
ai-billing-agent/
│
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── workflows/
│   │   ├── tools/
│   │   ├── rag/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   ├── utils/
│   │   ├── config.py
│   │   └── main.py
│   │
│   ├── alembic/
│   │   └── versions/
│   ├── tests/
│   ├── .env.example
│   ├── requirements.txt
│   └── alembic.ini
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── types/
│   │   ├── utils/
│   │   ├── App.tsx
│   │   ├── App.css
│   │   └── index.css
│   ├── package.json
│   └── vite.config.ts
│
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites

Install the following:

- Python 3.13+
- Node.js and npm
- PostgreSQL 17+
- PostgreSQL pgvector extension
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/sivaprabu-k/ai-billing-agent.git

cd ai-billing-agent
```

### 2. Backend Setup

Navigate to the backend:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file inside the backend directory.

Configure the following variables:

```env
APP_NAME="AI Billing and Dispute Resolution System"
APP_VERSION="1.0.0"
DEBUG=True

GEMINI_API_KEY=your_gemini_api_key

DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5433/ai_billing_db

JWT_SECRET_KEY=your_secure_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_HOST=https://cloud.langfuse.com
```

Never commit your actual `.env` file or API keys.

### 4. Database Setup

Create the PostgreSQL database:

```sql
CREATE DATABASE ai_billing_db;
```

Enable pgvector:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Run database migrations:

```bash
alembic upgrade head
```

### 5. Start Backend Server

From the backend directory:

```bash
uvicorn app.main:app --reload
```

Backend URL:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

### 6. Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

---

## API Response Format

The backend follows a consistent global response structure.

```json
{
  "status": true,
  "data": {},
  "status_code": 200,
  "message": "Request successful"
}
```

---

## Financial Safety & Security

The system follows important financial and security principles:

- Use Python `Decimal` for monetary calculations.
- Store financial amounts using PostgreSQL `NUMERIC`.
- Never trust LLM-generated financial calculations.
- Validate user ownership before accessing billing records.
- Use authenticated user identity for database operations.
- Require human approval for adjustments exceeding configured limits.
- Maintain transaction and audit records.
- Protect credit operations against duplicate execution.
- Keep external payment processing separate from simulated credit adjustments.

---

## Development Roadmap

- [x] Project initialization and Git setup
- [x] Backend project structure
- [x] Frontend project initialization
- [x] Tailwind CSS v4 configuration
- [x] Database configuration
- [x] Authentication APIs
- [x] JWT access and refresh token implementation
- [x] User session management
- [x] Initial Alembic migration setup
- [ ] Complete frontend dashboard UI
- [ ] Customer management
- [ ] Subscription management
- [ ] Usage tracking
- [ ] Invoice generation
- [ ] Billing Analyst Agent
- [ ] Policy Research Agent with RAG
- [ ] Dispute Resolution Agent
- [ ] Refund/Credit Agent
- [ ] Supervisor Agent with LangGraph
- [ ] Human approval workflow
- [ ] Langfuse observability and evaluations
- [ ] Frontend and backend integration
- [ ] Testing and Docker deployment

---

## Future Enhancements

- Automated billing anomaly detection.
- Advanced dispute classification.
- Hybrid retrieval and reranking.
- Automated policy evaluation.
- AI-powered billing analytics.
- Comprehensive agent evaluation.
- Production payment gateway integration.

---

## Author

**Siva Prabu**

Python Full Stack Developer | AI & Agentic AI Enthusiast

GitHub: https://github.com/sivaprabu-k

---

## License

This project is developed for learning, demonstration, and portfolio purposes. A formal license can be added before public distribution.