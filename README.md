# Sherlock AI Assignment

[![Netlify Status](https://api.netlify.com/api/v1/badges/f3b0f434-f04e-498d-848c-91d228c28fa9/deploy-status)](https://app.netlify.com/sites/sherlockai/deploys)
[![backend - Docker Image CI](https://github.com/LOCKhart07/sherlock-ai-assignment/actions/workflows/backend-build-and-deploy.yaml/badge.svg)](https://github.com/LOCKhart07/sherlock-ai-assignment/actions/workflows/backend-build-and-deploy.yaml)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-sherlockai.lockhart.in-blue?style=flat&logo=globe)](https://sherlockai.lockhart.in/)

A full-stack web application built as part of the Sherlock AI interview process. The project demonstrates modern web development practices with a focus on security and user experience.

## Tech Stack

- **Frontend**: Vue 3 + Quasar Framework
- **Backend**: FastAPI + SQLAlchemy
- **Authentication**: JWT + Google OAuth
- **Database**: SQLite
- **Deployment**: Docker + Netlify

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