# 🛒 E-Commerce Management System

One-stop admin dashboard and REST API for managing a simple e-commerce store. Built with:

- Backend: FastAPI (Python) + MySQL
- Frontend: React (Create React App)
- Authentication: hashed passwords with passlib/bcrypt
This README contains everything a developer needs to get the project running locally, how the code is organized, API examples, deployment notes, and troubleshooting tips.

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
- Not production-ready: contains simplified auth and direct DB access patterns. Review and harden before public deployment.

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

# Start FastAPI (development)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Notes

- `backend/requirements.txt` pins versions used during development (FastAPI, Uvicorn, mysql-connector-python, python-dotenv, pydantic, passlib, bcrypt).
- If using a different MySQL driver (e.g. PyMySQL or SQLAlchemy), update the code accordingly.

Database schema

- The SQL schema is provided at `backend/ecommerce_store.sql` — import it into your MySQL server to create tables and sample data.

API overview

- Base URL (development): `http://localhost:8000`
- Interactive docs (Swagger): `http://localhost:8000/docs`
- Common endpoints (examples — check `backend/main.py` for exact routes):
      - `GET /products` — list products
      - `GET /products/{id}` — get product
      - `POST /products` — create product
      - `PUT /products/{id}` — update product
      - `DELETE /products/{id}` — delete product
      - `GET /users`, `POST /users`, `PUT /users/{id}` — user CRUD

Authentication

- Passwords are hashed using `passlib`/`bcrypt` (see backend code). The project contains basic auth flows suitable for demos. For production, switch to token-based auth (JWT/OAuth2) and HTTPS.

Frontend (React)

Prerequisites

- Node.js 14+ (the package.json lists dependencies compatible with CRA and React 19)

Install & run (development)

```bash
cd frontend
npm install
npm start
```

- The dev server runs on `http://localhost:3000` by default and should proxy or call the API at `http://localhost:8000` depending on the frontend configuration.

Build for production

```bash
cd frontend
npm run build
# build artifacts will be in frontend/build
```

Development notes

- File structure (high-level)
  - `backend/` — FastAPI app and SQL schema
  - `frontend/src/` — React app with components, pages, and service helpers

- Helpful scripts
  - Backend: `uvicorn main:app --reload`
  - Frontend: `npm start`, `npm run build`

Testing

- Frontend: CRA test runner exists; run `cd frontend && npm test`.
- Backend: add pytest-based tests into `backend/tests/` and run `pytest` from the repo root after installing test dependencies.

Linting & formatting

- Add `black`/`ruff` for Python and `prettier`/`eslint` for JS if you want consistent formatting (not included by default).

Troubleshooting

- Issue: `pip install -r requirements.txt` fails
    - Double-check you activated the virtualenv.
    - The `requirements.txt` contains `python-dotenv==1.0.0s` — that looks like a typo. If pip errors, open `backend/requirements.txt` and change `python-dotenv==1.0.0s` to `python-dotenv==1.0.0` or run `pip install python-dotenv` separately.

- Issue: MySQL connection refused
    - Confirm MySQL server is running and credentials in `.env` are correct.
    - Check `DB_HOST`, `DB_PORT` (default 3306), `DB_USER`, `DB_PASSWORD`, `DB_NAME`.

- Issue: Frontend can't reach backend
    - Ensure backend is running on `localhost:8000` and CORS is enabled in the FastAPI app (see `main.py`).

Security notes
- Do not commit `.env` files containing production credentials.
- Use HTTPS and a proper secret management process in production.
- Replace demo auth with OAuth2/JWT flow and salted password hashing best practices before deploying publicly.

Contribution & License
- This repository was created as a final project / learning assignment. Contributions are welcome for learning purposes, but please open issues or PRs and allow maintainers to review.

License
- MIT License — see `LICENSE` file if present.

Recommended next steps (optional improvements)
- Add unit and integration tests for backend routes (pytest + testcontainers/mysql).
- Add Dockerfiles for backend and frontend and a `docker-compose.yml` that brings up MySQL, backend, and frontend for easy local development.
- Add CI (GitHub Actions) for tests and linting.

Acknowledgements
- Built as an academic final project combining FastAPI and React.

Contact
- Project owner: fredxotic (GitHub)
# 🛒 E-Commerce Management System

A modern, full-stack e-commerce solution built with FastAPI (Python), React, and MySQL. This project features a robust backend API and a responsive admin dashboard for managing all store data.

🚀 Features
FastAPI Backend: A secure and efficient RESTful API.

User Management: Full CRUD operations for user data.

Product & Category Management: Dynamic CRUD operations for products and their categories.

Password Hashing: Secure storage of user credentials using passlib.

React Admin Dashboard: A clean and user-friendly interface.

Intuitive UI: Easily manage products, users, and categories from a single dashboard.

Real-time Interaction: Seamlessly connects with the backend API to reflect changes instantly.

Clean Design: A minimal and responsive layout for a great user experience.

💻 Tech Stack
Backend

Frontend

Database







Python 3.9+

Node.js 14+



📁 Project Structure
/
├── backend/                   # FastAPI backend application
│   ├── main.py               # Core API logic and endpoints
│   ├── ecommerce_store.sql   # SQL schema for the database
│   ├── requirements.txt      # Python dependencies
│   └── .env.example          # Template for environment variables
│
└── frontend/                  # React admin dashboard
    ├── src/                   # React source files
    │   ├── components/
    │   └── pages/
    ├── package.json
    └── README.md

🚀 Quick Start Guide
Follow these simple steps to get the application running on your local machine.

1. Backend Setup
Navigate to the backend folder:

cd backend

Install Python dependencies:

pip install -r requirements.txt

Set up your MySQL database and create a new database with the schema provided in ecommerce_store.sql.

Create a .env file from the .env.example template and add your database credentials.

Run the FastAPI server:

uvicorn main:app --reload

2. Frontend Setup
Open a new terminal and navigate to the frontend folder:

cd frontend

Install Node.js dependencies:

npm install

Run the React app:

npm start

With both servers running, the React application at http://localhost:3000 will automatically connect to your API at http://localhost:8000.

🤝 Contributing & Support
This project is a final assignment and is not actively seeking contributions. For any questions, please reach out to the project owner.

📄 License
This project is licensed under the MIT License.