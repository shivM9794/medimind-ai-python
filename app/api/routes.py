
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.config import settings
from app.schemas import (
    ChatRequest,
    ChatResponse,
    DashboardResponse,
    UploadResponse,
)
from app.services.assistant_service import AssistantService

router = APIRouter()
assistant_service = AssistantService()


@router.get("/health")
def health_check():
    return {"status": "ok", "application": settings.app_name}


@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard():
    # Demo values only; replace with authenticated database records.
    return DashboardResponse(
        patient_name="Demo Patient",
        upcoming_appointments=2,
        active_care_plans=1,
        recent_records=4,
    )


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        return assistant_service.ask(request.question)
    except Exception as exc:
        # Log full details securely in production; do not return secrets.
        raise HTTPException(
            status_code=500,
            detail="The assistant could not process your request.",
        ) from exc


@router.post("/documents", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    allowed_extensions = {".pdf", ".txt"}
    filename = Path(file.filename or "").name
    suffix = Path(filename).suffix.lower()

    if suffix not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are supported.",
        )

    content = await file.read()
    max_bytes = settings.max_upload_mb * 1024 * 1024

    if not content:
        raise HTTPException(status_code=400, detail="The file is empty.")

    if len(content) > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"Maximum upload size is {settings.max_upload_mb} MB.",
        )

    upload_dir = Path(settings.upload_directory)
    upload_dir.mkdir(parents=True, exist_ok=True)

    safe_name = f"{uuid4().hex}{suffix}"
    destination = upload_dir / safe_name
    destination.write_bytes(content)

    return UploadResponse(
        filename=filename,
        status="stored",
        message=(
            "File stored locally. It has not been parsed or indexed "
            "for retrieval yet."
        ),
    )
