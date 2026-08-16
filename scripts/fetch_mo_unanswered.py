"""
Pull MathOverflow unanswered / no-accepted questions related to Ramanujan
and write a curated intake list for the knowledge graph.

MO /unanswered ~= questions with no upvoted or accepted answer (SE definition).
We additionally pull answers=0 and tagged:ramanujan for research intake.
"""

from __future__ import annotations

import json
import re
import ssl
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "kg" / "mo_unanswered_ramanujan.json"

# Prefer threads that look like open formula / meaning / proof problems
PRIORITY_PATTERNS = [
    r"unprov",
    r"conjectur",
    r"mysterious",
    r"unknown",
    r"open\b",
    r"lost notebook",
    r"meaning",
    r"interpret",
    r"new\?",
    r"already known",
    r"proven\?",
    r"prove",
    r"identity",
    r"continued fraction",
    r"1/\\?pi",
    r"mock theta",
    r"entry\b",
    r"notebook",
]

NOISE_PATTERNS = [
    r"jokes",
    r"crowdsourced",
    r"unconventional education",
    r"demystifying complex",
    r"equality vs\. isomorphism",
    r"list of",
]


def get(path: str, **params):
    params.setdefault("site", "mathoverflow.net")
    params.setdefault("pagesize", 50)
    url = f"https://api.stackexchange.com/2.3{path}?{urllib.parse.urlencode(params)}"
    ctx = ssl._create_unverified_context()
    with urllib.request.urlopen(url, timeout=60, context=ctx) as r:
        return json.load(r)


def score_relevance(title: str, tags: list[str]) -> int:
    t = title.lower()
    score = 0
    if "ramanujan" in tags or "ramanujan" in t:
        score += 5
    for p in PRIORITY_PATTERNS:
        if re.search(p, t, re.I):
            score += 3
    for p in NOISE_PATTERNS:
        if re.search(p, t, re.I):
            score -= 10
    return score


def slim(it: dict) -> dict:
    return {
        "question_id": it["question_id"],
        "title": it["title"],
        "score": it["score"],
        "answer_count": it.get("answer_count", 0),
        "link": it["link"],
        "tags": it.get("tags", []),
        "creation_date": it.get("creation_date"),
        "relevance": score_relevance(it["title"], it.get("tags", [])),
    }


def main() -> None:
    zero = get(
        "/search/advanced",
        tagged="ramanujan",
        accepted="False",
        answers=0,
        sort="votes",
        order="desc",
    )
    no_accepted = get(
        "/search/advanced",
        tagged="ramanujan",
        accepted="False",
        sort="votes",
        order="desc",
    )

    zero_items = [slim(it) for it in zero.get("items", [])]
    noacc_items = [slim(it) for it in no_accepted.get("items", [])]
    zero_items.sort(key=lambda x: (-x["relevance"], -x["score"]))
    noacc_items.sort(key=lambda x: (-x["relevance"], -x["score"]))

    curated = [x for x in zero_items if x["relevance"] >= 5][:25]

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_url": "https://mathoverflow.net/unanswered",
        "note": (
            "MO /unanswered is site-wide. This file is the Ramanujan-tagged subset "
            "for KG intake, ranked toward open formula / meaning questions."
        ),
        "curated_for_kg": curated,
        "tagged_ramanujan_zero_answers": zero_items,
        "tagged_ramanujan_no_accepted": noacc_items,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")

    print(f"Wrote {OUT}")
    print(f"Curated KG intake ({len(curated)}):")
    for it in curated[:15]:
        print(f"  [{it['score']}|rel {it['relevance']}] {it['title']}")
        print(f"    {it['link']}")


if __name__ == "__main__":
    main()
