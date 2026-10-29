
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(min_length=2, max_length=2000)


class SourceReference(BaseModel):
    title: str
    source: str
    excerpt: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceReference] = Field(default_factory=list)
    disclaimer: str = (
        "This assistant provides general information, not a diagnosis "
        "or a substitute for a qualified healthcare professional."
    )


class DashboardResponse(BaseModel):
    patient_name: str
    upcoming_appointments: int
    active_care_plans: int
    recent_records: int


class UploadResponse(BaseModel):
    filename: str
    status: str
    message: str
