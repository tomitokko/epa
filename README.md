# AI-Powered KSB Reviewer MVP

This repository contains a minimal proof of concept for an AI-assisted reviewer
that helps apprenticeship students check their project evidence against the
Knowledge, Skills and Behaviours (KSBs) required by their standard.

## Structure

- `backend/` – FastAPI service with a `/review` endpoint
- `data/standards.json` – example apprenticeship standard and KSB rubric
- `frontend/` – very small web page to interact with the API

## Running locally

1. Install dependencies (FastAPI and Uvicorn):
   ```bash
   pip install fastapi uvicorn pydantic
   ```
2. Start the API server from the `backend` directory:
   ```bash
   uvicorn main:app --reload
   ```
3. Open `frontend/index.html` in your browser and run a review.

The API performs extremely simple checks against the mock data. It searches the
text for each required KSB tag and basic pass/distinction keywords. It then
returns feedback as JSON, which the web page displays.

This is **not** production ready but illustrates the MVP flow described in the
prompt.
