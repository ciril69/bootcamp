# BACKEND PROMPT – PHASE 1
## FastAPI Backend Scaffolding

The frontend for this project is already complete.

IMPORTANT:
- Do NOT modify, rename, move, or delete anything inside the existing frontend project.
- Do NOT create frontend files.
- Build only the backend and connect to the existing frontend through REST APIs.

---

## Objective

Create a clean, scalable FastAPI backend for a demo men's streetwear e-commerce application.

The backend should be production-ready in architecture while keeping the implementation lightweight.

Technology

- Python 3.12+
- FastAPI
- Pydantic v2
- Uvicorn
- Supabase (PostgreSQL)
- Supabase Python SDK
- python-dotenv
- Loguru
- HTTPX
- Pytest

Do **not** implement database models, SQL, business logic, or API routes yet. This phase is only about project scaffolding.

---

# Folder Structure

Create the following structure.

```
server/
│
├── app/
│   │
│   ├── api/
│   │   └── v1/
│   │
│   ├── core/
│   │
│   ├── config/
│   │
│   ├── db/
│   │
│   ├── dependencies/
│   │
│   ├── middleware/
│   │
│   ├── repositories/
│   │
│   ├── schemas/
│   │
│   ├── services/
│   │
│   ├── utils/
│   │
│   ├── constants/
│   │
│   ├── exceptions/
│   │
│   └── main.py
│
├── tests/
│
├── .env.example
├── .gitignore
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

# Configure FastAPI

Create the FastAPI application.

Include:

- Application title
- Version
- Description
- API prefix placeholder
- Swagger
- ReDoc

Configure startup and shutdown events.

---

# Environment Configuration

Load configuration from environment variables.

Prepare variables for

```
APP_NAME

APP_ENV

DEBUG

API_PREFIX

SUPABASE_URL

SUPABASE_ANON_KEY

SUPABASE_SERVICE_ROLE_KEY

DATABASE_URL

CORS_ORIGINS
```

No secrets should be hardcoded.

---

# Logging

Configure Loguru.

Create centralized logging.

Log:

- Startup
- Shutdown
- Unexpected exceptions

Do not log secrets.

---

# CORS

Create configurable CORS middleware.

Allow localhost during development.

Allow configurable production origins.

---

# Exception Handling

Create a global exception handler.

Return errors using

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message"
  }
}
```

---

# Health Endpoint

Implement only one endpoint.

GET

```
/health
```

Returns

```json
{
    "status":"healthy"
}
```

---

# Dependency Structure

Create placeholders for

- Database dependency
- Configuration dependency
- Future authentication dependency

No implementation yet.

---

# Repository Layer

Create empty repository classes.

- ProductRepository
- CategoryRepository
- CartRepository
- OrderRepository
- ContactRepository

---

# Service Layer

Create empty services.

- ProductService
- CategoryService
- CartService
- OrderService
- ContactService

No business logic.

---

# Schema Layer

Create placeholder Pydantic schemas.

- Product
- Category
- Cart
- Order
- Contact

No fields yet.

---

# API Routers

Create empty routers.

products.py

categories.py

cart.py

orders.py

contact.py

health.py

Only register them.

No endpoints except /health.

---

# Documentation

Swagger should work immediately.

```
/docs
```

ReDoc

```
/redoc
```

---

# Deliverable

Generate the complete project scaffolding, configuration, middleware, logging, environment setup, router registration, and health endpoint.

Do NOT implement:

- Database
- Models
- SQL
- Supabase integration
- API endpoints
- Business logic

Those will be completed in later phases.