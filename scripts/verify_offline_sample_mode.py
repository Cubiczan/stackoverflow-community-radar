#!/usr/bin/env python3
"""Offline, dependency-free proof of the README's sample-mode claims.

Imports the radar package with the standard library only (`requests` is
imported lazily inside `StackExchangeClient.fetch_questions`, so module import
performs no network access and needs no third-party packages), loads the
bundled sample data, ranks it twice from opposite input orders, and fail-closes
(exit 1) unless every check holds:

- every sample question reports source == "sample"
- the ranked order is identical regardless of input order (determinism)
- the top-ranked question is unanswered
- a force-sample client fetch returns bundled data
- the topic graph, clusters, and an answer brief all build offline

Exit 0 only when every check holds.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from stackoverflow_radar.client import StackExchangeClient  # noqa: E402
from stackoverflow_radar.graph import (  # noqa: E402
    build_topic_graph,
    cluster_questions,
    summarize_graph,
)
from stackoverflow_radar.insights import build_answer_brief, rank_questions  # noqa: E402
from stackoverflow_radar.sample_data import load_sample_questions  # noqa: E402


def main() -> int:
    questions = load_sample_questions()
    if not questions:
        print("FAIL: load_sample_questions returned no data")
        return 1
    if any(q.source != "sample" for q in questions):
        print("FAIL: sample data carries a non-sample source label")
        return 1

    forward = rank_questions(questions)
    backward = rank_questions(list(reversed(questions)))
    if [q.question_id for q in forward] != [q.question_id for q in backward]:
        print("FAIL: ranking is order-dependent — not deterministic")
        return 1
    if forward[0].is_answered:
        print("FAIL: top-ranked question is answered — priority queue broken")
        return 1

    client = StackExchangeClient()
    forced = client.fetch_questions(force_sample=True)
    if not forced or any(q.source != "sample" for q in forced):
        print("FAIL: force-sample fetch did not return bundled data")
        return 1

    graph = build_topic_graph(forward)
    summary = summarize_graph(graph)
    if summary["questions"] != len(forward) or summary["tags"] <= 0:
        print(f"FAIL: graph summary inconsistent: {summary}")
        return 1

    clusters = cluster_questions(forward)
    if not clusters:
        print("FAIL: no clusters produced from sample data")
        return 1

    brief = build_answer_brief(forward[0], related_questions=forward[1:3])
    if not brief.outline:
        print("FAIL: answer brief has no outline")
        return 1

    print(
        f"offline sample mode verified: {len(forward)} questions, "
        f"{summary['tags']} tags, {summary['edges']} edges, {len(clusters)} "
        "clusters — ranked deterministically with no network access"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
