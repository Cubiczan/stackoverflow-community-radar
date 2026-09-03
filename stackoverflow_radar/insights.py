from __future__ import annotations

from collections import Counter

from .models import AnswerBrief, Question


def priority_score(question: Question) -> float:
    score = 0.0
    if not question.is_answered:
        score += 40.0
    score += max(0.0, 14.0 - question.answer_count * 5.0)
    score += min(question.view_count / 120.0, 20.0)
    score += max(0.0, 12.0 - question.score * 2.5)
    if question.accepted_answer_id is not None:
        score -= 18.0
    return round(score, 2)


def rank_questions(questions: list[Question]) -> list[Question]:
    return sorted(
        questions,
        key=lambda question: (
            -priority_score(question),
            question.is_answered,
            question.answer_count,
            -question.view_count,
        ),
    )


def build_answer_brief(question: Question, related_questions: list[Question] | None = None) -> AnswerBrief:
    related_questions = related_questions or []
    focus = question.tags[0] if question.tags else "general"
    suggested_angle = _suggest_angle(question)
    outline = _outline_for(question, related_questions)
    community_note = (
        "High-priority unanswered thread. Keep the answer specific, reproducible, and linked to an idiomatic pattern."
        if not question.is_answered
        else "Already answered, but worth tightening if the accepted solution is incomplete."
    )
    return AnswerBrief(
        question_id=question.question_id,
        title=question.title,
        priority=priority_score(question),
        focus=focus,
        suggested_angle=suggested_angle,
        outline=outline,
        community_note=community_note,
        related_questions=[item.question_id for item in related_questions[:5]],
    )


def _suggest_angle(question: Question) -> str:
    tags = {tag.lower() for tag in question.tags}
    if "python" in tags and "sqlalchemy" in tags:
        return "Explain the ORM mechanism, show the query pattern, and give a safe eager-loading example."
    if "reactjs" in tags or "hooks" in tags:
        return "Frame the lifecycle issue, show the stable hook pattern, and explain why the rerender happens."
    if "rust" in tags:
        return "Lead with ownership rules, then show the smallest lifetime-safe refactor."
    if "postgresql" in tags:
        return "Tie the answer to planner behavior and make the index tradeoff explicit."
    if "typescript" in tags:
        return "Show a type-level pattern that preserves inference without over-constraining the generic."
    return "Answer with the minimal reproducible pattern, a short explanation, and one caveat."


def _outline_for(question: Question, related_questions: list[Question]) -> list[str]:
    tag_counts = Counter(tag for item in related_questions for tag in item.tags)
    top_related_tag = tag_counts.most_common(1)[0][0] if tag_counts else None
    if top_related_tag not in question.tags:
        top_related_tag = question.tags[0] if question.tags else "general"
    return [
        f"State the core rule or pattern for {top_related_tag}",
        "Show a minimal example that compiles or runs",
        "Explain the common mistake and how to avoid it",
        "Add one practical variant the asker can apply immediately",
    ]
