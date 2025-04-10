# Sherlock AI Assignment

[![Netlify Status](https://api.netlify.com/api/v1/badges/f3b0f434-f04e-498d-848c-91d228c28fa9/deploy-status)](https://app.netlify.com/sites/sherlockai/deploys)
[![backend - Docker Image CI](https://github.com/LOCKhart07/sherlock-ai-assignment/actions/workflows/backend-build-and-deploy.yaml/badge.svg)](https://github.com/LOCKhart07/sherlock-ai-assignment/actions/workflows/backend-build-and-deploy.yaml)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-sherlockai.lockhart.in-blue?style=flat&logo=globe)](https://sherlockai.lockhart.in/)

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-green.svg)](https://fastapi.tiangolo.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D.svg?logo=vue.js)](https://vuejs.org/)
[![Quasar](https://img.shields.io/badge/Quasar-2.x-1976D2.svg?logo=quasar)](https://quasar.dev/)

[![SQLite](https://img.shields.io/badge/SQLite-3.x-003B57.svg?logo=sqlite)](https://www.sqlite.org/)
[![Docker](https://img.shields.io/badge/Docker-20.10+-2496ED.svg?logo=docker)](https://www.docker.com/)

A full-stack web application built as part of the Sherlock AI interview process. The project demonstrates modern web development practices with a focus on security and user experience.

## Tags

- 🔐 Authentication & Authorization
- 🚀 Full-Stack Development
- 🎨 Modern UI/UX
- 🔄 CI/CD Pipeline
- 🐳 Docker Containerization
- 🛡️ Security Best Practices
- 📱 Responsive Design
- 🗃️ Database Management
- 🔍 API Development
- 🧪 Testing

## Tech Stack

- **Frontend**: Vue 3 + Quasar Framework
- **Backend**: FastAPI + SQLAlchemy
- **Authentication**: JWT + Google OAuth
- **Database**: SQLite
- **Deployment**: Docker + Netlify
- **Testing**: pytest
- **CI/CD**: GitHub Actions
- **Code Quality**: ESLint, Prettier
- **Version Control**: Git

## Quick Start

1. Clone the repository
2. Backend setup:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   uvicorn app:app --reload
   ```

3. Frontend setup:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Features

- User authentication with JWT and Google OAuth
- Modern, responsive UI with Quasar Framework
- RESTful API with FastAPI
- Secure password hashing with bcrypt
- Database migrations and testing setup
- Docker containerization for easy deployment
- Automated CI/CD pipeline
- Comprehensive test coverage
- Code quality tools integration
- Environment-based configuration

## Project Structure

```
.
├── frontend/           # Vue 3 + Quasar frontend
├── backend/           # FastAPI backend
│   ├── api/          # API endpoints
│   ├── core/         # Core functionality
│   ├── models/       # Database models
│   ├── schemas/      # Pydantic schemas
│   └── tests/        # Test suite
└── .github/          # GitHub Actions workflows
```
