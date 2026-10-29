
from fastapi import FastAPI

app = FastAPI(
    title="MediMind AI",
    description="AI-powered healthcare assistant",
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "app": "MediMind AI",
        "message": "Welcome to MediMind AI!",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
