#!/usr/bin/env python3
"""Fail-closed check that the Streamlit entrypoint wires the full pipeline.

README claims `streamlit run streamlit_app.py` renders the dashboard: a
priority queue, a graph summary, topic clusters, and an answer brief. This
check statically parses `streamlit_app.py` and refuses (exit 1) unless the
entrypoint imports streamlit, wires all four pipeline surfaces from
`stackoverflow_radar`, defines `main()`, and guards the `main()` invocation
behind `if __name__ == "__main__"`. Stdlib-only by design: the
evidence-matrix CI job runs before any install step.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "streamlit_app.py"

REQUIRED_IMPORTS = {
    "streamlit",
    "stackoverflow_radar.client",
    "stackoverflow_radar.graph",
    "stackoverflow_radar.insights",
}
REQUIRED_CALLS = {
    "rank_questions",
    "build_topic_graph",
    "cluster_questions",
    "build_answer_brief",
    "main",
}


def main() -> int:
    if not APP.is_file():
        print("FAIL: streamlit_app.py is missing from the tree")
        return 1
    try:
        module = ast.parse(APP.read_text(encoding="utf-8"))
    except SyntaxError as exc:
        print(f"FAIL: streamlit_app.py does not parse: {exc}")
        return 1

    imports: set[str] = set()
    calls: set[str] = set()
    has_main_def = False
    has_main_guard = False
    for node in ast.walk(module):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            calls.add(node.func.id)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name == "main":
                has_main_def = True
        elif isinstance(node, ast.If):
            test = node.test
            if (
                isinstance(test, ast.Compare)
                and isinstance(test.left, ast.Name)
                and test.left.id == "__name__"
                and any(
                    isinstance(cmp, ast.Constant) and cmp.value == "__main__"
                    for cmp in test.comparators
                )
            ):
                has_main_guard = True

    problems: list[str] = []
    for name in sorted(REQUIRED_IMPORTS - imports):
        problems.append(f"missing import: {name}")
    for name in sorted(REQUIRED_CALLS - calls):
        problems.append(f"missing call: {name}()")
    if not has_main_def:
        problems.append("missing def main()")
    if not has_main_guard:
        problems.append('missing `if __name__ == "__main__":` guard')

    if problems:
        print("FAIL: streamlit entrypoint incomplete — " + "; ".join(problems))
        return 1

    print(
        "streamlit entrypoint verified: streamlit_app.py imports streamlit, "
        "wires client/graph/insights, and exposes the __main__ guard"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
