# Personal Notes Manager - Flask Backend

A Flask REST API for managing personal notes with JWT authentication.

## Quick Start

The service auto-initializes a local SQLite database on first run and serves OpenAPI docs at `/docs`.

Health check:
- GET `/` -> `{ "message": "Healthy" }`

API base path: `/api`

## Auth Endpoints

- POST `/api/auth/signup`
  - Body: `{ "email": "user@example.com", "password": "yourpassword" }`
  - 201: `{ "id": 1, "email": "user@example.com", "created_at": "..." }`

- POST `/api/auth/login`
  - Body: `{ "email": "user@example.com", "password": "yourpassword" }`
  - 200: `{ "access_token": "<JWT>" }`

- GET `/api/auth/me`
  - Header: `Authorization: Bearer <JWT>`
  - 200: `{ "id": 1, "email": "user@example.com", "created_at": "..." }`

## Notes Endpoints

- GET `/api/notes`
  - Header: `Authorization: Bearer <JWT>`
  - 200: `[ { "id": 1, "title": "...", "content": "...", ... } ]`

- POST `/api/notes`
  - Header: `Authorization: Bearer <JWT>`
  - Body: `{ "title": "My note", "content": "..." }`
  - 201: `{ "id": 1, "title": "My note", "content": "...", ... }`

- GET `/api/notes/<id>`
  - Header: `Authorization: Bearer <JWT>`

- PUT `/api/notes/<id>`
  - Header: `Authorization: Bearer <JWT>`
  - Body: `{ "title": "New title", "content": "Updated content" }`

- DELETE `/api/notes/<id>`
  - Header: `Authorization: Bearer <JWT>`
  - 204: No content

## Environment Variables

Provide a `.env` in the backend container root or set environment vars:

- `FLASK_SECRET_KEY` - Flask secret key (required for secure sessions)
- `JWT_SECRET_KEY` - JWT signing secret
- `DATABASE_URL` - SQLAlchemy URL (default: SQLite at app.db)
- `CORS_ORIGINS` - Allowed CORS origins (default: `*`)

See `.env.example` for a template.

## OpenAPI Docs

Interactive docs available at `/docs`. OpenAPI JSON at `/openapi.json`.

## Notes

- Passwords are hashed using Werkzeug security utilities.
- JWTs are issued via `flask-jwt-extended`.
- Database is created automatically on first request/app startup.
