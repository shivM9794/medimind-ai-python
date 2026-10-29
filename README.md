
# MediMind AI

A Python-first healthcare information assistant demo.

## Stack

- Streamlit: user interface
- FastAPI: backend REST API
- Pydantic Settings: configuration
- Local JSON: starter knowledge repository
- Amazon Bedrock: optional language model adapter
- Pytest: unit tests
- Docker: backend container

## Run locally

Create and activate a virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

Create the environment file:

    cp .env.example .env

Run the API in terminal 1:

    uvicorn app.main:app --reload

Run the UI in terminal 2:

    source .venv/bin/activate
    streamlit run ui/Home.py

Open:

- UI: http://localhost:8501
- API documentation: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/api/health

## Run tests

    pytest -q

## Current limitations

- Local keyword retrieval is not semantic vector search.
- Uploaded files are stored but not parsed or indexed.
- Dashboard values are sample data.
- Authentication and database persistence are not implemented.
- Bedrock is optional and requires AWS setup.
- This project is a learning demo, not a clinical system.

Never use real patient records in this unprotected development app.
