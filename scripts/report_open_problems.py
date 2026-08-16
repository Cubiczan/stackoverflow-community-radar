"""Emit a reviewable catalogue of Berndt's open commentary.

Two tiers, kept separate because they are different research questions:

  meaning_gap            Berndt could not determine what Ramanujan *meant*.
  unproved_or_incorrect  The statement is understood but unproved, or wrong.

Hits are clustered by (volume, page, entry) since several cues often fire on
one passage. Output is markdown for human review -- these are candidates, not
conclusions; the surrounding passage still has to be read.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HITS = ROOT / "data" / "kg" / "mined_hits.json"
OUT = ROOT / "data" / "kg" / "OPEN_PROBLEMS.md"

TIERS = [
    ("meaning_gap", "No assigned meaning", "Berndt states he could not discern what the entry means."),
    ("unproved_or_incorrect", "Unproved or incorrect", "The statement is understood but unproved, or shown false."),
]

VOLUME_TITLES = {
    "part-1": "Part I",
    "part-2": "Part II",
    "part-3": "Part III",
    "part-4": "Part IV",
    "part-5": "Part V",
}

# Display maths in the span: $$...$$ blocks first, then inline $...$
DISPLAY_RE = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
INLINE_RE = re.compile(r"(?<!\$)\$([^$]{12,})\$(?!\$)")


def extract_formulas(span: str, limit: int = 3) -> list[str]:
    out = [m.group(1).strip() for m in DISPLAY_RE.finditer(span)]
    if not out:
        out = [m.group(1).strip() for m in INLINE_RE.finditer(span)]
    seen, uniq = set(), []
    for f in out:
        f = " ".join(f.split())
        if f not in seen:
            seen.add(f)
            uniq.append(f)
    return uniq[:limit]


def cluster(hits: list[dict]) -> list[dict]:
    buckets: dict[tuple, dict] = {}
    for h in hits:
        key = (h["volume_id"], h.get("page"), h.get("entry"))
        b = buckets.setdefault(
            key,
            {
                "volume_id": h["volume_id"],
                "page": h.get("page"),
                "entry": h.get("entry"),
                "chapter": h.get("chapter"),
                "cues": [],
                "spans": [],
            },
        )
        if h["cue"] not in b["cues"]:
            b["cues"].append(h["cue"])
        if h["span"] not in b["spans"]:
            b["spans"].append(h["span"])
        b["chapter"] = b["chapter"] or h.get("chapter")
        b["method_gap"] = b.get("method_gap") or bool(h.get("method_gap"))
    return sorted(
        buckets.values(),
        key=lambda b: (b["volume_id"], b["page"] or 0),
    )


def render(tier_key: str, title: str, blurb: str, clusters: list[dict]) -> list[str]:
    lines = [f"## {title}", "", f"_{blurb}_", "", f"**{len(clusters)} clusters.**", ""]
    by_vol: dict[str, list[dict]] = defaultdict(list)
    for c in clusters:
        by_vol[c["volume_id"]].append(c)

    for vol in sorted(by_vol):
        lines.append(f"### {VOLUME_TITLES.get(vol, vol)}")
        lines.append("")
        for c in by_vol[vol]:
            where = f"p. {c['page']}" if c["page"] else "page unknown"
            if c["entry"]:
                where += f", Entry {c['entry']}"
            if c["chapter"]:
                where += f" (Ch. {c['chapter']})"
            lines.append(f"#### {where}")
            lines.append("")
            lines.append(f"Cues: {', '.join(f'`{x}`' for x in c['cues'])}")
            if c.get("method_gap"):
                lines.append("")
                lines.append(
                    "**Method gap** — Berndt proved this, but not by means available "
                    "to Ramanujan. Open question is a proof in Ramanujan's style, "
                    "not the result itself."
                )
            lines.append("")

            formulas = extract_formulas(c["spans"][0])
            if formulas:
                lines.append("Formula(s) in context:")
                lines.append("")
                for f in formulas:
                    lines.append("```latex")
                    lines.append(f)
                    lines.append("```")
                lines.append("")

            excerpt = " ".join(c["spans"][0].split())
            if len(excerpt) > 700:
                excerpt = excerpt[:700] + " ..."
            lines.append(f"> {excerpt}")
            lines.append("")
    return lines


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args()

    hits = json.loads(HITS.read_text(encoding="utf-8"))

    lines = [
        "# Ramanujan's Notebooks — Open Commentary Catalogue",
        "",
        "Mined from Bruce Berndt's commentary across all five volumes. Each entry is a",
        "**candidate** flagged by a phrase cue; the surrounding passage must still be read",
        "before treating it as an open problem.",
        "",
    ]

    counts = {}
    for key, title, blurb in TIERS:
        tier_hits = [h for h in hits if h.get("priority") == key]
        clusters = cluster(tier_hits)
        counts[key] = (len(clusters), len(tier_hits))
        lines.extend(render(key, title, blurb, clusters))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {args.out}")
    for key, title, _ in TIERS:
        n_clusters, n_hits = counts[key]
        print(f"  {title}: {n_clusters} clusters from {n_hits} raw hits")


if __name__ == "__main__":
    main()
