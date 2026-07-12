# Streetwear E-Commerce Backend

This is the backend API for the streetwear e-commerce application. It is built with FastAPI, using Supabase (PostgreSQL) as the datastore.

## Tech Stack
- **Framework**: FastAPI
- **Server**: Uvicorn
- **Validation**: Pydantic v2
- **Logging**: Loguru
- **Database Client**: Supabase Python SDK
- **Testing**: Pytest

## Project Structure
```
server/
├── app/
│   ├── api/             # API Routers & Endpoints (organized by version)
│   ├── config/          # Environment configuration (Pydantic Settings)
│   ├── constants/       # Global constants & Enums
│   ├── core/            # Core system modules (logging, etc.)
│   ├── db/              # Database initialization & clients
│   ├── dependencies/    # FastAPI dependency injection functions
│   ├── exceptions/      # Custom exceptions & global handlers
│   ├── middleware/      # CORS and custom middleware
│   ├── repositories/    # Data access layer (Supabase repositories)
│   ├── schemas/         # Pydantic models for validation / serialization
│   ├── services/        # Business logic layer
│   ├── utils/           # Utility functions & helpers
│   └── main.py          # FastAPI application entrypoint
├── tests/               # Test suites (Pytest)
├── .env.example         # Template for environment variables
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Project tool configurations (Pytest, etc.)
└── README.md            # This documentation file
```

## Getting Started

### Prerequisites
- Python 3.12 or newer

### Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   # Update values in .env with your local credentials
   ```

### Running the Application
To run the server locally with reload enabled:
```bash
uvicorn app.main:app --reload
```

The API will be available at:
- Health status: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health) (and root `/health`)
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Running Tests
To run tests using Pytest:
```bash
pytest
```
