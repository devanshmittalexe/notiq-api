<div align="center">

<!-- Animated Typing Header (self-hosted SVG — works on GitHub) -->
<img src="./assets/header.svg" alt="NoteIQ — Personal Notes REST API" width="800"/>

<br/>

<!-- Badges Row 1 -->
<img src="https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/FastAPI-Latest-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
<img src="https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white"/>
<img src="https://img.shields.io/badge/Docker-Latest-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>

<br/>

<!-- Badges Row 2 -->
<img src="https://img.shields.io/badge/Deployed_on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white"/>
<img src="https://img.shields.io/badge/Database-Neon-00E699?style=for-the-badge&logo=postgresql&logoColor=white"/>
<img src="https://img.shields.io/badge/Auth-JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white"/>
<img src="https://img.shields.io/badge/Status-Live-brightgreen?style=for-the-badge"/>

<br/><br/>

<!-- Animated wave divider -->
<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=header&text=&fontSize=0"/>

</div>

---

## 🚀 Live Demo

> ⚡ **API Base URL:** [`https://notiq-api.onrender.com`](https://notiq-api.onrender.com)
> 
> 📖 **Interactive Docs (Swagger):** [`https://notiq-api.onrender.com/docs`](https://notiq-api.onrender.com/docs)
>
> 🌐 **Frontend:** Hosted via GitHub Pages

> [!NOTE]
> Render's free tier spins down after 15 minutes of inactivity. A splash screen with an animated robot mascot greets you while the server wakes up (typically 30–60 seconds).

---

## ✨ What Makes It Special

> *"Beyond basic CRUD — Noteiq has JWT authentication, bcrypt password hashing with salt, rate limiting to prevent abuse, and soft delete with 30-day trash recovery. These are patterns you find in production APIs, not tutorial projects."*

```
✅  JWT-based stateless authentication        ✅  bcrypt password hashing with salt
✅  PostgreSQL + SQLAlchemy ORM               ✅  Docker containerization
✅  Rate limiting (slowapi)                   ✅  Soft delete with 30-day recovery
✅  Modular, scalable folder structure        ✅  Cloud-deployed with auto CI/CD
✅  Animated frontend (GitHub Pages)          🔄  Public note sharing (In Progress)
```

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology | Purpose |
|-------|-----------|---------|
| 🐍 **Language** | Python 3.13 | Primary language |
| ⚡ **Framework** | FastAPI | REST API framework with auto-docs |
| 🗄️ **Database** | PostgreSQL 16 | Persistent relational storage |
| 🔗 **ORM** | SQLAlchemy + Alembic | DB management & migrations |
| ✅ **Validation** | Pydantic v2 | Request schema validation |
| 🔐 **Auth** | PyJWT / python-jose | JWT token creation & verification |
| 🔑 **Hashing** | passlib[bcrypt] 4.0.1 | Secure password hashing |
| 🚦 **Rate Limiting** | slowapi | Abuse & brute-force protection |
| 🖥️ **Server** | uvicorn | ASGI server |
| 🐳 **Infra** | Docker | Containerized deployment |
| ☁️ **Hosting** | Render.com | Free-tier cloud hosting |
| 🐘 **Cloud DB** | Neon (neon.tech) | Serverless PostgreSQL |

</div>

---

## 📁 Project Structure

```
notiq-api/
├── app/
│   ├── __init__.py          # Makes app a Python package
│   ├── main.py              # App setup, CORS, rate limiter, router registration
│   ├── database.py          # SQLAlchemy engine, session, Base
│   ├── models.py            # DB table definitions (User, Note)
│   ├── schemas.py           # Pydantic models (NoteCreate, UserCreate)
│   ├── auth.py              # Password hashing + JWT functions
│   ├── dependencies.py      # get_current_user() auth guard
│   └── routers/
│       ├── __init__.py
│       ├── auth_router.py   # /auth/register, /auth/login
│       └── notes.py         # All /notes endpoints
├── index.html               # Frontend UI (GitHub Pages)
├── Dockerfile               # Docker container definition
├── .dockerignore
├── .env                     # ⚠️ Never committed
├── .gitignore
└── requirements.txt
```

---

## 🔌 API Endpoints

### 🔐 Authentication

| Method | Route | Rate Limit | Description |
|--------|-------|-----------|-------------|
| `POST` | `/auth/register` | 5 / min | Create a new user account |
| `POST` | `/auth/login` | 10 / min | Login and receive a JWT token |

**Register:**
```json
// POST /auth/register
// Request:
{ "email": "user@example.com", "password": "mypassword" }

// Response 200:
{ "message": "User registered successfully", "email": "user@example.com" }
```

**Login:**
```
// POST /auth/login  (form-data, not JSON — OAuth2 standard)
username: user@example.com
password: mypassword

// Response 200:
{ "access_token": "eyJhbGci...", "token_type": "bearer" }
```

---

### 📝 Notes  *(All require `Authorization: Bearer <token>`)*

| Method | Route | Rate Limit | Description |
|--------|-------|-----------|-------------|
| `GET` | `/notes` | 60 / min | Get all notes for the logged-in user |
| `GET` | `/notes/{id}` | 60 / min | Get a specific note by ID |
| `POST` | `/notes` | 30 / min | Create a new note |
| `PUT` | `/notes/{id}` | 30 / min | Update an existing note |
| `DELETE` | `/notes/{id}` | 30 / min | Permanently delete a note |

---

## 🔒 Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    REQUEST LIFECYCLE                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Client  ──►  Rate Limiter (slowapi)                        │
│                    │                                        │
│                    ▼                                        │
│           FastAPI Router matches endpoint                   │
│                    │                                        │
│                    ▼                                        │
│         Depends(get_current_user) runs:                     │
│           • Extract Bearer token from header                │
│           • verify_access_token() → decode JWT              │
│           • Query users table for user_id                   │
│           • 401 if invalid/expired                          │
│                    │                                        │
│                    ▼                                        │
│         Depends(get_db) → DB session created                │
│                    │                                        │
│                    ▼                                        │
│         Endpoint runs → SQLAlchemy → Neon PostgreSQL        │
│                    │                                        │
│                    ▼                                        │
│         JSON response returned to client ✅                  │
└─────────────────────────────────────────────────────────────┘
```

### 🛡️ Threat Model

| Threat | Protection |
|--------|-----------|
| Password storage breach | bcrypt hashing — hashes cannot be reversed |
| Rainbow table attacks | bcrypt salt — same password ≠ same hash |
| Brute force login | Rate limit: 10/min + bcrypt slowness (~100ms/check) |
| Token interception | HTTPS on Render encrypts all traffic |
| Token forgery | HS256 signature with `SECRET_KEY` — cannot be faked |
| Accessing others' notes | All queries filter by `user_id` |
| API abuse / DoS | slowapi rate limiting on all endpoints |
| Credentials in code | `.env` excluded via `.gitignore` |

---

## 🗃️ Database Schema

```sql
-- users table
CREATE TABLE users (
    id          SERIAL PRIMARY KEY,
    email       VARCHAR UNIQUE NOT NULL,
    password    VARCHAR NOT NULL,   -- bcrypt hash
    created_at  TIMESTAMPTZ DEFAULT now()
);

-- notes table
CREATE TABLE notes (
    id          SERIAL PRIMARY KEY,
    title       VARCHAR NOT NULL,
    content     VARCHAR NOT NULL,
    user_id     INTEGER REFERENCES users(id) NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT now(),
    updated_at  TIMESTAMPTZ,        -- auto-updated on edit
    deleted_at  TIMESTAMPTZ         -- soft delete field
);
```

**Relationship:** One user → many notes (one-to-many via `user_id` foreign key)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.13+
- PostgreSQL (or a [Neon](https://neon.tech) free account)
- Docker (optional, for containerized run)

### Local Development

```bash
# 1. Clone the repo
git clone https://github.com/devanshmittalexe/notiq-api.git
cd notiq-api

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env and add your DATABASE_URL and SECRET_KEY

# 5. Run the server
uvicorn app.main:app --reload

# 6. Open interactive docs
# http://localhost:8000/docs
```

### Docker

```bash
# Build the image
docker build -t notiq-api .

# Run the container
docker run -p 8000:8000 \
  -e DATABASE_URL=your_neon_connection_string \
  -e SECRET_KEY=your_secret_key \
  notiq-api
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | Neon PostgreSQL connection string (`postgresql://...`) |
| `SECRET_KEY` | JWT signing secret — keep private, never commit |

---

## 🌿 Git Workflow

```
dev  ──►  qa  ──►  main  ──►  Render Auto-Deploy
 ▲
 └── All active development happens here
     Never commit directly to main.
```

```bash
# Feature development flow
git checkout dev
git add . && git commit -m "feat: your feature description"
git push origin dev

# Promote to QA
git checkout qa && git merge dev && git push origin qa

# Deploy to production
git checkout main && git merge qa && git push origin main
# ☁️ Render detects the push and auto-rebuilds the Docker container
```

---

## 🏗️ Development Journey

<details>
<summary><b>Phase 1 — CRUD with Fake Data ✅</b></summary>

Built all 5 CRUD endpoints using a Python list as a fake in-memory database. Learned FastAPI basics, Pydantic models, HTTP methods, and endpoint routing.

**Problem discovered:** Data was lost on every server restart → solved in Phase 2.
</details>

<details>
<summary><b>Phase 2 — PostgreSQL + SQLAlchemy ✅</b></summary>

Replaced the in-memory list with a real PostgreSQL database on Neon. Created `database.py` for connection management and `models.py` for table definitions.

**Issues resolved:** Supabase account banned → switched to Neon. `.env` accidentally pushed → `git rm --cached .env` + password reset. Neon cold start drops → `pool_pre_ping=True`.
</details>

<details>
<summary><b>Phase 3 — JWT Authentication ✅</b></summary>

Added user registration, login, and protected routes. Every notes endpoint now requires a valid JWT. Each user only sees their own notes.

**Issues resolved:** bcrypt version incompatibility → pinned `bcrypt==4.0.1`. `SECRET_KEY` was `None` → added `load_dotenv()` to `auth.py`. Missing `user_id` column → dropped and recreated tables in Neon.
</details>

<details>
<summary><b>Phase 4 — Modular Folder Structure ✅</b></summary>

Refactored from a single `main.py` into a professional modular structure matching real production codebases. No new features — purely an architectural improvement.

**Issues resolved:** Circular import between `notes.py` ↔ `main.py` → created `dependencies.py`.
</details>

<details>
<summary><b>Phase 5 — Docker + Render Deployment ✅</b></summary>

Containerized the app with Docker and deployed to Render's free tier. The API is now publicly accessible with automatic HTTPS.

**Issues resolved:** CORS error from frontend → added `CORSMiddleware`. Render free tier cold starts → splash screen with animated robot mascot.
</details>

<details>
<summary><b>Extras — Rate Limiting + Soft Delete ✅</b></summary>

Added `slowapi` rate limiting to all endpoints. Implemented soft delete with `deleted_at` timestamp for 30-day trash recovery.
</details>

---

## 🎨 Frontend Features

The `index.html` frontend (hosted on GitHub Pages) includes:

- 🤖 **Animated robot mascot** — floats, bounces on success, shakes on error
- 👀 **Eyes close when typing password**, look around when typing email
- ⌨️ **Typing effect** on dashboard — cycles through phrases
- 🎉 **Confetti animation** when a note is created
- 🌙 **Dark / Light mode toggle** — preference saved in `localStorage`
- ⏳ **Splash screen** — animated robot walks while server wakes up
- 🔍 **Real-time search** — client-side note filtering
- 🃏 **Staggered card animations** on the notes grid

---

## 📊 HTTP Status Codes

| Code | Meaning in Notiq |
|------|-----------------|
| `200 OK` | Request succeeded |
| `400 Bad Request` | Email already registered |
| `401 Unauthorized` | Invalid token or credentials |
| `404 Not Found` | Note doesn't exist or belongs to another user |
| `422 Unprocessable Entity` | Request body validation failed |
| `429 Too Many Requests` | Rate limit exceeded |

---

## 🔭 What's Next — UBdoc

Notiq was the learning vehicle. **UBdoc** is the next project: an AI Code Intelligence Agent that connects to GitHub via webhooks and automatically generates documentation, code review comments, and code insights for every pull request.

Skills carried over from Notiq → FastAPI routing, PostgreSQL + SQLAlchemy, JWT auth, Docker, dependency injection, and modular folder structure.

---

<div align="center">

<!-- Animated footer wave -->
<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=footer"/>

**Built with FastAPI, PostgreSQL, Docker, and a lot of debugging.**

[![GitHub](https://img.shields.io/badge/GitHub-devanshmittalexe-181717?style=for-the-badge&logo=github)](https://github.com/devanshmittalexe/notiq-api)
[![Live API](https://img.shields.io/badge/Live_API-notiq--api.onrender.com-46E3B7?style=for-the-badge&logo=render)](https://notiq-api.onrender.com)
[![Swagger Docs](https://img.shields.io/badge/Swagger-Docs-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)](https://notiq-api.onrender.com/docs)

*Thanks for checking out NoteIQ! ⭐ Star the repo if you found it useful.*

</div>