"""
Build a NetworkX knowledge graph from:
1. Seed unproven corpus
2. Phrase-mined Berndt commentary hits (meaning-gap prioritized)
3. Volume scaffolding from parse manifests
4. MathOverflow starter questions (mo_starter_workset.json)
5. Curated formula artifacts (formula_*.json, meaning_gaps_curated.json)
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import networkx as nx
from rich.console import Console

ROOT = Path(__file__).resolve().parents[1]
PARSED = ROOT / "data" / "parsed"
KG_DIR = ROOT / "data" / "kg"
SEED_PATH = KG_DIR / "seed_unproven.json"
MO_WORKSET = KG_DIR / "mo_starter_workset.json"
CURATED_GAPS = KG_DIR / "meaning_gaps_curated.json"

console = Console()


def load_seed() -> dict:
    if not SEED_PATH.exists():
        raise SystemExit("Missing seed file. Run: python scripts/seed_unproven_corpus.py")
    return json.loads(SEED_PATH.read_text(encoding="utf-8"))


def load_json(path: Path) -> dict | list | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


# Ranked tiers, most research value first. Drives sorting and truncation.
PRIORITY_ORDER = ["meaning_gap", "unproved_or_incorrect", "other"]


def build_cue_tiers(cue_priority: dict) -> dict[str, str]:
    """Map lowercased cue -> tier name from the seed's cue_priority block.

    Every tier the seed declares is honoured. Collapsing unlisted tiers into
    'other' would pool real signal ('unable to prove', 'unproved') with noise
    cues like 'incomplete', which matches 'incomplete elliptic integral' far
    more often than an incomplete proof.
    """
    tiers: dict[str, str] = {}
    for tier, tier_cues in cue_priority.items():
        for cue in tier_cues:
            tiers[cue.lower()] = tier
    return tiers


def compile_qualifiers(qualifiers: dict) -> dict[str, list[re.Pattern]]:
    return {
        name: [re.compile(p, re.I) for p in patterns]
        for name, patterns in (qualifiers or {}).items()
    }


def match_qualifiers(
    context: str, compiled: dict[str, list[re.Pattern]]
) -> dict[str, bool]:
    """Flags describing a hit, independent of its tier.

    Orthogonal on purpose: a passage can be both 'unproved' and a method gap
    (Berndt proved it, but not Ramanujan's way), or unproved and *not* one --
    the latter being the genuinely open case worth surfacing.
    """
    return {
        name: any(p.search(context) for p in patterns)
        for name, patterns in compiled.items()
    }


def mine_cues(
    markdown: str,
    cues: list[str],
    volume_id: str,
    *,
    cue_tiers: dict[str, str],
    qualifiers: dict[str, list[re.Pattern]] | None = None,
    window: int = 400,
) -> list[dict]:
    hits = []
    for cue in cues:
        pattern = re.compile(cue, re.IGNORECASE)
        for m in pattern.finditer(markdown):
            start = max(0, m.start() - window)
            end = min(len(markdown), m.end() + window)
            page = None
            page_m = list(re.finditer(r"<!-- page (\d+) -->", markdown[: m.start()]))
            if page_m:
                page = int(page_m[-1].group(1))
            priority = cue_tiers.get(cue.lower(), "other")
            # Best-effort Entry / Chapter anchors: prefer the last Entry
            # heading that appears before the cue (not an earlier chapter).
            before = markdown[max(0, m.start() - 2500) : m.start()]
            entry = None
            entry_matches = list(
                re.finditer(
                    r"(?:\*\*)?Entry\s+(\d+(?:\([ivxlc]+\))?(?:\([^)]+\))?)",
                    before,
                    re.I,
                )
            )
            if entry_matches:
                entry = entry_matches[-1].group(1).strip()
            chapter = None
            chapter_matches = list(re.finditer(r"Chapter\s+(\d+)", before, re.I))
            if chapter_matches:
                chapter = int(chapter_matches[-1].group(1))
            # Narrow window: the qualifier ("...by methods familiar to
            # Ramanujan", "...resorted to modular forms") trails the cue
            # closely. A wide window would match unrelated prose, since
            # "theory of modular forms" is common throughout these volumes.
            qual_context = markdown[max(0, m.start() - 100) : m.end() + 350]
            flags = match_qualifiers(qual_context, qualifiers or {})
            hits.append(
                {
                    "volume_id": volume_id,
                    "page": page,
                    "chapter": chapter,
                    "entry": entry,
                    "cue": cue,
                    "priority": priority,
                    **flags,
                    "span": markdown[start:end].replace("\n", " ").strip(),
                }
            )
    rank = {tier: i for i, tier in enumerate(PRIORITY_ORDER)}
    hits.sort(key=lambda h: (rank.get(h["priority"], len(rank)), h.get("page") or 0))
    return hits


def dedupe_meaning_gaps(hits: list[dict]) -> list[dict]:
    """Collapse overlapping meaning-gap cues on the same volume+page into one cluster."""
    buckets: dict[tuple, dict] = {}
    for h in hits:
        if h.get("priority") != "meaning_gap":
            continue
        key = (h["volume_id"], h.get("page"), h.get("entry") or "")
        if key not in buckets:
            buckets[key] = {
                **h,
                "cues": [h["cue"]],
                "spans": [h["span"]],
            }
        else:
            b = buckets[key]
            if h["cue"] not in b["cues"]:
                b["cues"].append(h["cue"])
            if h["span"] not in b["spans"]:
                b["spans"].append(h["span"])
            # Prefer richer entry/chapter
            if not b.get("entry") and h.get("entry"):
                b["entry"] = h["entry"]
            if not b.get("chapter") and h.get("chapter"):
                b["chapter"] = h["chapter"]
    curated = []
    for i, ((vol, page, entry), b) in enumerate(sorted(buckets.items())):
        slug_entry = re.sub(r"[^a-zA-Z0-9]+", "-", (entry or "unknown")).strip("-").lower() or "unknown"
        nid = f"gap:{vol}:p{page or 'na'}:{slug_entry}"
        curated.append(
            {
                "id": nid,
                "kind": "meaning_gap",
                "status": "no_assigned_meaning_candidate",
                "volume_id": vol,
                "page": page,
                "chapter": b.get("chapter"),
                "entry": b.get("entry"),
                "cues": b["cues"],
                "primary_cue": b["cues"][0],
                "span": b["spans"][0][:1200],
                "span_count": len(b["spans"]),
                "agent_packet": f"data/kg/agent_packets/{nid.replace(':', '_')}.md",
            }
        )
    return curated


def add_mo_nodes(G: nx.MultiDiGraph) -> int:
    workset = load_json(MO_WORKSET)
    # Prefer seed source id mo-unanswered when present
    feed_id = "mo-unanswered" if G.has_node("mo-unanswered") else "source:mo-unanswered"
    if not G.has_node(feed_id):
        G.add_node(
            feed_id,
            kind="source",
            title="MathOverflow — Unanswered questions",
            url="https://mathoverflow.net/unanswered",
            role="primary_open_problem_feed",
        )
    if not workset:
        console.print("[yellow]no MO workset[/yellow] (create data/kg/mo_starter_workset.json)")
        return 0

    n = 0
    for q in workset.get("questions", []):
        qid = f"mo:{q['question_id']}"
        G.add_node(
            qid,
            kind="mo_question",
            status=q.get("kg_status"),
            title=q.get("title"),
            score=q.get("score"),
            answer_count=q.get("answer_count"),
            link=q.get("link"),
            open_problem=q.get("open_problem"),
            priority=q.get("priority"),
            tags=q.get("tags", []),
            analysis_summary=(q.get("analysis") or "")[:500],
            feed="https://mathoverflow.net/unanswered",
        )
        G.add_edge(qid, feed_id, relation="from_unanswered_feed")
        for related in q.get("related_kg_nodes", []):
            if not G.has_node(related):
                G.add_node(related, kind="formula_cluster", label=related)
            G.add_edge(qid, related, relation="related_to")
        vol = (q.get("notebook_anchor") or {}).get("volume")
        if vol:
            vid = f"volume:{vol}" if not str(vol).startswith("volume:") else str(vol)
            if not G.has_node(vid):
                G.add_node(vid, kind="volume", title=vol, parsed=False)
            G.add_edge(qid, vid, relation="anchors_in")
        n += 1
    return n


def add_formula_artifacts(G: nx.MultiDiGraph) -> int:
    n = 0
    for path in sorted(KG_DIR.glob("formula_*.json")):
        formula = json.loads(path.read_text(encoding="utf-8"))
        fid = formula.get("id") or f"formula:{path.stem}"
        attrs = {k: v for k, v in formula.items() if k != "id"}
        attrs.setdefault("kind", "formula")
        G.add_node(fid, **attrs)
        for mid in formula.get("mo_questions", []) or []:
            mq = f"mo:{mid}" if not str(mid).startswith("mo:") else str(mid)
            if not G.has_node(mq):
                G.add_node(mq, kind="mo_question", title=f"MO {mid}")
            G.add_edge(fid, mq, relation="addresses_question")
        parent = formula.get("parent_thread")
        if parent:
            if not G.has_node(parent):
                G.add_node(parent, kind="mo_question", title=parent)
            G.add_edge(fid, parent, relation="from_thread")
        for related in formula.get("related_kg_nodes", []) or []:
            if related == fid:
                continue
            if not G.has_node(related):
                G.add_node(related, kind="formula_cluster", label=related)
            G.add_edge(fid, related, relation="related_to")
        vol = formula.get("volume")
        if vol:
            vid = f"volume:{vol}" if not str(vol).startswith("volume:") else str(vol)
            if G.has_node(vid):
                G.add_edge(fid, vid, relation="located_in")
        sketch = formula.get("elementary_proof_sketch")
        if sketch:
            sid = f"proof:{Path(sketch).stem}"
            G.add_node(
                sid,
                kind="proof_sketch",
                path=sketch,
                status="elementary_spine",
            )
            G.add_edge(fid, sid, relation="has_proof_sketch")
        n += 1
    return n


def add_curated_gaps(G: nx.MultiDiGraph, curated: list[dict]) -> None:
    for gap in curated:
        gid = gap["id"]
        G.add_node(
            gid,
            kind="meaning_gap",
            status=gap.get("status"),
            volume_id=gap.get("volume_id"),
            page=gap.get("page"),
            chapter=gap.get("chapter"),
            entry=gap.get("entry"),
            cues=gap.get("cues", []),
            primary_cue=gap.get("primary_cue"),
            span=(gap.get("span") or "")[:800],
            agent_packet=gap.get("agent_packet"),
        )
        vid = f"volume:{gap['volume_id']}"
        if G.has_node(vid):
            G.add_edge(gid, vid, relation="located_in")
        if G.has_node("open:no-assigned-meaning"):
            G.add_edge(gid, "open:no-assigned-meaning", relation="member_of_cluster")
        # Link high-signal Part I Entry 21 to meta MO thread
        if gap.get("entry") and str(gap["entry"]).startswith("21") and G.has_node("mo:377092"):
            G.add_edge(gid, "mo:377092", relation="exemplifies")


def build_graph(seed: dict, mined: list[dict], curated: list[dict]) -> nx.MultiDiGraph:
    G = nx.MultiDiGraph()
    G.graph["generated_at"] = datetime.now(timezone.utc).isoformat()
    G.graph["purpose"] = "Ramanujan notebooks - no-assigned-meaning / obscure KG"

    for src in seed.get("sources", []):
        G.add_node(src["id"], kind="source", **{k: v for k, v in src.items() if k != "id"})

    for entry in seed.get("entries", []):
        eid = entry["id"]
        G.add_node(
            eid,
            kind="formula_cluster",
            status=entry.get("status"),
            label=entry.get("label"),
            tags=entry.get("tags", []),
        )
        for ev in entry.get("evidence", []):
            sid = ev.get("source_id")
            if sid and G.has_node(sid):
                G.add_edge(eid, sid, relation="cited_in", note=ev.get("note"))

    for vol_dir in sorted(PARSED.glob("part-*")):
        if not vol_dir.is_dir():
            continue
        vid = vol_dir.name
        meta_path = vol_dir / "job.json"
        meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
        G.add_node(
            f"volume:{vid}",
            kind="volume",
            title=meta.get("title"),
            page_count=meta.get("page_count_written"),
            parsed=bool(meta),
        )

    for i, hit in enumerate(mined):
        nid = f"mine:{hit['volume_id']}:p{hit.get('page')}:{i}"
        status = (
            "candidate_no_assigned_meaning"
            if hit.get("priority") == "meaning_gap"
            else "candidate_unproved_or_obscure"
        )
        G.add_node(
            nid,
            kind="commentary_hit",
            status=status,
            priority=hit.get("priority", "other"),
            cue=hit["cue"],
            page=hit.get("page"),
            chapter=hit.get("chapter"),
            entry=hit.get("entry"),
            span=hit["span"][:800],
            volume_id=hit["volume_id"],
        )
        G.add_edge(nid, f"volume:{hit['volume_id']}", relation="located_in")
        G.add_edge(nid, "open:no-assigned-meaning", relation="member_of_cluster")

    mo_n = add_mo_nodes(G)
    formula_n = add_formula_artifacts(G)
    add_curated_gaps(G, curated)
    console.print(f"MO questions wired: {mo_n}; formula artifacts: {formula_n}; curated gaps: {len(curated)}")
    return G


def _graphml_safe(value):
    if value is None:
        return ""
    if isinstance(value, (list, dict, tuple, set)):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float, str)):
        return value
    return str(value)


def export_graph(G: nx.MultiDiGraph) -> None:
    KG_DIR.mkdir(parents=True, exist_ok=True)
    data = nx.node_link_data(G)
    (KG_DIR / "graph.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    H = nx.MultiDiGraph()
    H.graph.update({k: _graphml_safe(v) for k, v in G.graph.items()})
    for n, attrs in G.nodes(data=True):
        H.add_node(n, **{k: _graphml_safe(v) for k, v in attrs.items()})
    for u, v, attrs in G.edges(data=True):
        H.add_edge(u, v, **{k: _graphml_safe(a) for k, a in attrs.items()})
    nx.write_graphml(H, KG_DIR / "graph.graphml")
    summary = {
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "by_kind": {},
        "commentary_hits": sum(1 for _, a in G.nodes(data=True) if a.get("kind") == "commentary_hit"),
        "meaning_gaps": sum(1 for _, a in G.nodes(data=True) if a.get("kind") == "meaning_gap"),
        "mo_questions": sum(1 for _, a in G.nodes(data=True) if a.get("kind") == "mo_question"),
    }
    for _, attrs in G.nodes(data=True):
        k = attrs.get("kind", "unknown")
        summary["by_kind"][k] = summary["by_kind"].get(k, 0) + 1
    (KG_DIR / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    console.print(f"[green]KG[/green] {summary}")


def write_agent_packets(curated: list[dict]) -> None:
    """One markdown packet per curated gap for parallel agents."""
    out_dir = KG_DIR / "agent_packets"
    out_dir.mkdir(parents=True, exist_ok=True)
    for gap in curated:
        fname = gap["id"].replace(":", "_") + ".md"
        path = out_dir / fname
        path.write_text(
            "\n".join(
                [
                    f"# Agent packet: {gap['id']}",
                    "",
                    f"- volume: `{gap.get('volume_id')}`",
                    f"- page (parse marker): `{gap.get('page')}`",
                    f"- chapter (heuristic): `{gap.get('chapter')}`",
                    f"- entry (heuristic): `{gap.get('entry')}`",
                    f"- cues: {', '.join(gap.get('cues') or [])}",
                    "",
                    "## Task",
                    "1. Open `data/parsed/{volume}/full.md` around the page marker.",
                    "2. Identify the exact Entry / formula Berndt cannot interpret.",
                    "3. Extract clean LaTeX statement(s).",
                    "4. Classify: true meaning-gap vs divergent/false entry vs historical aside.",
                    "5. Note any MO/literature pointers; do not invent proofs.",
                    "6. Write findings to `data/kg/agent_reports/{id}.json` with keys:",
                    "   id, entry, statement_latex, classification, confidence, notes, sources.",
                    "",
                    "## Span",
                    gap.get("span") or "",
                    "",
                ]
            ).replace("{volume}", str(gap.get("volume_id"))).replace("{id}", gap["id"].replace(":", "_")),
            encoding="utf-8",
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-hits-per-volume", type=int, default=200)
    args = parser.parse_args()

    seed = load_seed()
    cues = seed.get("mining_cues", [])
    cue_tiers = build_cue_tiers(seed.get("cue_priority", {}))
    qualifiers = compile_qualifiers(seed.get("qualifiers", {}))
    mined: list[dict] = []

    for vol_dir in sorted(PARSED.glob("part-*")):
        md_path = vol_dir / "full.md"
        if not md_path.exists():
            console.print(f"[yellow]no markdown yet[/yellow] {vol_dir.name}")
            continue
        text = md_path.read_text(encoding="utf-8", errors="replace")
        hits = mine_cues(
            text, cues, vol_dir.name, cue_tiers=cue_tiers, qualifiers=qualifiers
        )
        if len(hits) > args.max_hits_per_volume:
            dropped = len(hits) - args.max_hits_per_volume
            console.print(
                f"[yellow]{vol_dir.name}: dropping {dropped} lowest-tier hits "
                f"(cap {args.max_hits_per_volume})[/yellow]"
            )
            hits = hits[: args.max_hits_per_volume]
        meaning_n = sum(1 for h in hits if h.get("priority") == "meaning_gap")
        unproved_n = sum(1 for h in hits if h.get("priority") == "unproved_or_incorrect")
        console.print(
            f"{vol_dir.name}: {len(hits)} hits "
            f"({meaning_n} meaning-gap, {unproved_n} unproved)"
        )
        mined.extend(hits)

    curated = dedupe_meaning_gaps(mined)
    (KG_DIR / "mined_hits.json").write_text(json.dumps(mined, indent=2), encoding="utf-8")
    CURATED_GAPS.write_text(json.dumps(curated, indent=2), encoding="utf-8")
    write_agent_packets(curated)
    raw_mg = sum(1 for h in mined if h.get("priority") == "meaning_gap")
    console.print(f"Curated meaning-gap clusters: {len(curated)} (from {raw_mg} raw hits)")

    G = build_graph(seed, mined, curated)
    export_graph(G)


if __name__ == "__main__":
    main()
