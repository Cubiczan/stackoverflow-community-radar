from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class Question:
    question_id: int
    title: str
    body: str
    tags: list[str] = field(default_factory=list)
    score: int = 0
    answer_count: int = 0
    view_count: int = 0
    is_answered: bool = False
    accepted_answer_id: int | None = None
    link: str = ""
    owner: str = "community"
    source: str = "sample"
    creation_date: datetime | None = None
    last_activity_date: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        if self.creation_date is not None:
            data["creation_date"] = self.creation_date.isoformat()
        if self.last_activity_date is not None:
            data["last_activity_date"] = self.last_activity_date.isoformat()
        return data


@dataclass(slots=True)
class ClusterSummary:
    name: str
    tags: list[str]
    question_ids: list[int]
    unanswered_count: int
    average_score: float
    average_priority: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class AnswerBrief:
    question_id: int
    title: str
    priority: float
    focus: str
    suggested_angle: str
    outline: list[str]
    community_note: str
    related_questions: list[int] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
