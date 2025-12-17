# Quick Start Guide

## Backend Setup
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
# Create .env file and add your OPENAI_API_KEY
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

## Frontend Setup  
cd frontend
npm install
npm run dev

## Access
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
