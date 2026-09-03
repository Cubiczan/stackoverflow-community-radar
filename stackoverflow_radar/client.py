from __future__ import annotations

from typing import Any, Iterable

from .config import Settings
from .models import Question
from .sample_data import load_sample_questions


class StackExchangeClient:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings.from_env()

    def fetch_questions(
        self,
        *,
        tags: list[str] | None = None,
        query: str | None = None,
        page_size: int | None = None,
        force_sample: bool = False,
        use_sample_fallback: bool = True,
    ) -> list[Question]:
        page_size = page_size or self.settings.pagesize
        if force_sample:
            return self._filtered_sample(tags=tags, query=query)
        try:
            import importlib

            requests = importlib.import_module("requests")
        except Exception:
            return self._filtered_sample(tags=tags, query=query)

        params: dict[str, Any] = {
            "site": self.settings.site,
            "pagesize": page_size,
            "order": "desc",
            "sort": "activity",
            "filter": "withbody",
        }
        if self.settings.stack_exchange_key:
            params["key"] = self.settings.stack_exchange_key
        if self.settings.stack_exchange_access_token:
            params["access_token"] = self.settings.stack_exchange_access_token
        if tags:
            params["tagged"] = ";".join(tags)
        if query:
            params["q"] = query

        endpoint = "https://api.stackexchange.com/2.3/search/advanced"
        try:
            response = requests.get(endpoint, params=params, timeout=20)
            response.raise_for_status()
            payload = response.json()
            items = payload.get("items", []) if isinstance(payload, dict) else []
            questions = [self._from_api_item(item) for item in items]
            if questions:
                return questions
        except Exception:
            if not use_sample_fallback:
                raise
        return self._filtered_sample(tags=tags, query=query)

    def _filtered_sample(self, *, tags: list[str] | None, query: str | None) -> list[Question]:
        questions = load_sample_questions()
        if tags:
            wanted = {tag.lower() for tag in tags}
            questions = [q for q in questions if wanted.intersection({tag.lower() for tag in q.tags})]
        if query:
            needle = query.lower()
            questions = [q for q in questions if needle in q.title.lower() or needle in q.body.lower()]
        return questions

    def _from_api_item(self, item: dict[str, Any]) -> Question:
        owner = item.get("owner") or {}
        return Question(
            question_id=int(item.get("question_id", 0)),
            title=str(item.get("title", "")),
            body=str(item.get("body", "")),
            tags=list(item.get("tags", [])),
            score=int(item.get("score", 0)),
            answer_count=int(item.get("answer_count", 0)),
            view_count=int(item.get("view_count", 0)),
            is_answered=bool(item.get("is_answered", False)),
            accepted_answer_id=item.get("accepted_answer_id"),
            link=str(item.get("link", "")),
            owner=str(owner.get("display_name", "community")),
            source="stackexchange",
        )
