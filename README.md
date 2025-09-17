# 🛒 E-Commerce Management System

One-stop admin dashboard and REST API for managing a simple e-commerce store. Built with:

- Backend: FastAPI (Python) + MySQL
- Frontend: React (Create React App)
- Authentication: hashed passwords with passlib/bcrypt

Table of contents

- Project overview
- Quick start (local)
- Backend (detailed)

  - Prerequisites
  - Environment
  - Install & run
  - Database setup
  - API overview & examples
- Frontend (detailed)
  - Prerequisites
  - Install & run
  - Build for production
- Development notes
  - Testing
  - Linting & formatting
- Troubleshooting
- Contribution & License

Project status

- Status: Final project / learning demo
- Not production-ready: contains simplified auth and direct DB access patterns.

Quick start (local)

1) Clone the repository

```bash
git clone https://github.com/fredxotic/DataBase---Final-Project.git
cd "DataBase - FinalProject"
```

1) Backend (FastAPI)

Prerequisites

- Python 3.9+ installed
- MySQL server available (local or remote)

Install dependencies and run

```bash
cd backend
# create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# create .env from .env.example and fill in DB credentials
# example (Linux/macOS):
# cp .env.example .env
# then edit .env and set DB_HOST, DB_USER, DB_PASS, DB_NAME

# Run migrations / create schema (SQL file provided)
# Import using mysql client or a GUI tool:
# mysql -u <user> -p < database < ecommerce_store.sql

## Project overview

A modern full-stack e-commerce admin and API for managing users, products, and categories. The repo includes:

- `backend/` — FastAPI application, SQL schema, and Python dependencies
- `frontend/` — React admin dashboard built with Create React App

This project was created as a final academic assignment and is intended for learning and local development.

## Quick start (local)

1. Clone the repository

```bash
git clone https://github.com/fredxotic/DataBase---Final-Project.git
cd "DataBase - FinalProject"
```

2. Start the backend and frontend (instructions below)

---

## Backend (FastAPI)

### Prerequisites

- Python 3.9+
- MySQL server (local or remote)

### Environment

Copy the environment template and fill in your DB credentials:

```bash
cd backend
cp .env.example .env
# Edit .env and set DB_HOST, DB_PORT (default 3306), DB_USER, DB_PASSWORD, DB_NAME
```

### Install & run

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If `pip` fails due to a typo in `requirements.txt` (see Troubleshooting), install `python-dotenv` manually:

```bash
pip install python-dotenv
```

Import the database schema and run the app:

```bash
# import schema into MySQL (replace placeholders)
# mysql -u <user> -p < database < ecommerce_store.sql

uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Database setup

The SQL schema is available at `backend/ecommerce_store.sql`. Use `mysql` CLI or your preferred GUI to import this file into a MySQL database referenced by your `.env`.

### API overview

- Base URL (development): `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`

Common endpoints (verify exact routes in `backend/main.py`):

- `GET /products` — list products
- `GET /products/{id}` — get product
- `POST /products` — create product
- `PUT /products/{id}` — update product
- `DELETE /products/{id}` — delete product
- `GET /users`, `POST /users`, `PUT /users/{id}` — user CRUD

Authentication: passwords are hashed with `passlib`/`bcrypt`. For production, replace with token-based auth (JWT/OAuth2) and serve via HTTPS.

---

## Frontend (React)

### Install & run

```bash
cd frontend
npm install
npm start
```

The dev server runs at `http://localhost:3000` and should call the backend API at `http://localhost:8000` depending on frontend service configuration.

### Build for production

```bash
cd frontend
npm run build
# artifacts -> frontend/build
```

---

## Development notes

- High-level structure:
  - `backend/` — FastAPI app and SQL schema
  - `frontend/src/` — React components, pages, and services

- Helpful scripts:
  - Backend: `uvicorn main:app --reload`
  - Frontend: `npm start`, `npm run build`

- Testing:
  - Frontend: Run `cd frontend && npm test` (CRA test runner)
  - Backend: Add `pytest` tests under `backend/tests/` and run `pytest` after installing test dependencies

- Linting & formatting: Consider adding `black`, `ruff` for Python and `prettier`, `eslint` for JS.

---

## Troubleshooting

- pip install fails:
  - Ensure virtualenv is activated.
  - If you see an error related to `python-dotenv==1.0.0s`, that's a typo in `backend/requirements.txt`. Update the file to `python-dotenv==1.0.0` or install `python-dotenv` manually.

- MySQL connection refused:
  - Confirm MySQL server is running and credentials in `.env` are correct.
  - Check `DB_HOST` and `DB_PORT` (default 3306).

- Frontend cannot reach backend:
  - Ensure backend is running on `localhost:8000` and that CORS is enabled in FastAPI.

---

## Security notes

- Never commit `.env` with real credentials.
- Use HTTPS and secret management in production.
- Replace demo auth with a production-ready auth flow before exposing services publicly.

---

## Contact

Project owner: `fredxotic` (GitHub)
