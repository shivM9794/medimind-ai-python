
from app.core.config import settings
from app.repositories.knowledge_repository import KnowledgeRepository
from app.schemas import ChatResponse, SourceReference
from app.services.bedrock_adapter import BedrockAdapter


DISCLAIMER = (
    "This is general health information, not a medical diagnosis. "
    "Consult a qualified healthcare professional for personal medical advice."
)


class AssistantService:
    def __init__(self, repository=None, bedrock=None):
        self.repository = repository or KnowledgeRepository()
        self.bedrock = bedrock

    def ask(self, question: str) -> ChatResponse:
        question = question.strip()

        if not question:
            return ChatResponse(answer="Please enter a question.")

        documents = self.repository.search(question, limit=3)

        if not documents:
            return ChatResponse(
                answer=(
                    "I could not find relevant information in the "
                    "available knowledge base. Please consult a qualified "
                    "healthcare professional for personal medical guidance."
                ),
                sources=[],
                disclaimer=DISCLAIMER,
            )

        context = "\n\n".join(
            f"{doc.get('title', 'Information')}: "
            f"{doc.get('content', '')}"
            for doc in documents
        )

        if settings.use_bedrock:
            adapter = self.bedrock or BedrockAdapter()
            answer = adapter.generate(question, context)
        else:
            answer = (
                "Information found in the local knowledge base:\n\n"
                f"{context}\n\n"
                "Please discuss personal symptoms or treatment decisions "
                "with a qualified healthcare professional."
            )

        sources = [
            SourceReference(
                title=doc.get("title", "Untitled document"),
                source=doc.get("source", "Unknown source"),
                excerpt=doc.get("content", "")[:500],
            )
            for doc in documents
        ]

        return ChatResponse(
            answer=answer,
            sources=sources,
            disclaimer=DISCLAIMER,
        )
