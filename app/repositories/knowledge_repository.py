
import json
from pathlib import Path
from typing import Any

from app.core.config import settings


class KnowledgeRepository:
    def __init__(self, file_path: str | None = None):
        self.file_path = Path(
            file_path or settings.knowledge_base_path
        )

    def get_all(self) -> list[dict[str, Any]]:
        if not self.file_path.exists():
            return []

        with self.file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("Knowledge base must contain a JSON list.")

        return data

    def search(self, query: str, limit: int = 3) -> list[dict[str, Any]]:
        """Simple keyword search for the local demo."""
        query_terms = set(query.lower().split())
        scored_results = []

        for document in self.get_all():
            searchable_text = " ".join(
                [
                    str(document.get("title", "")),
                    str(document.get("content", "")),
                    str(document.get("source", "")),
                ]
            ).lower()

            score = sum(
                1 for term in query_terms
                if term in searchable_text
            )

            if score > 0:
                scored_results.append((score, document))

        scored_results.sort(key=lambda item: item[0], reverse=True)
        return [document for _, document in scored_results[:limit]]
