
import json

from app.repositories.knowledge_repository import KnowledgeRepository
from app.services.assistant_service import AssistantService


def test_assistant_returns_relevant_information(tmp_path):
    knowledge_file = tmp_path / "knowledge.json"
    knowledge_file.write_text(
        json.dumps(
            [
                {
                    "id": "1",
                    "title": "Appointment preparation",
                    "source": "Test source",
                    "content": (
                        "Prepare a list of symptoms and current medications "
                        "before your medical appointment."
                    ),
                }
            ]
        ),
        encoding="utf-8",
    )

    repository = KnowledgeRepository(str(knowledge_file))
    service = AssistantService(repository=repository)

    result = service.ask("How should I prepare for an appointment?")

    assert "symptoms" in result.answer.lower()
    assert len(result.sources) == 1
    assert result.sources[0].title == "Appointment preparation"


def test_assistant_handles_no_matching_documents(tmp_path):
    knowledge_file = tmp_path / "knowledge.json"
    knowledge_file.write_text("[]", encoding="utf-8")

    service = AssistantService(
        repository=KnowledgeRepository(str(knowledge_file))
    )
    result = service.ask("Unrelated question")

    assert result.sources == []
    assert "could not find" in result.answer.lower()
