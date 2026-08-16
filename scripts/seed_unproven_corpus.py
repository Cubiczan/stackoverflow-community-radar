"""
Seed a curated corpus of Ramanujan formulae that remain unproved,
obscure in meaning, or were long open (with provenance).

Primary anchors:
- https://mathoverflow.net/unanswered — live feed of open MO questions
  (Ramanujan-tagged slice → fetch_mo_unanswered.py / mo_starter_workset)
- MathOverflow 377092 (Berndt: no unproved claims; residual = no assigned meaning)
- Wolfram Blog 2013 (historically open → filled)
- Berndt volumes' "unable to prove / interpret" remarks (mined from LlamaParse)
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "kg" / "seed_unproven.json"

SEED = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "purpose": (
        "Bootstrap a KG for (1) Berndt meaning-gap residuals in the notebooks and "
        "(2) open MathOverflow questions in the Ramanujan orbit from the unanswered feed."
    ),
    "research_stance": {
        "proved_status": (
            "As of Berndt's 2019–2020 statements (via MathOverflow 377092 / Baez), "
            "there are no remaining Ramanujan claims that are neither proved nor disproved. "
            "The 2019 Berndt–Li–Zaharescu paper closed the last Lost Notebook identity."
        ),
        "open_research_target": (
            "Two parallel tracks: (A) notebook statements to which Berndt could not "
            "attach meaning; (B) live open problems from MathOverflow's unanswered "
            "queue, filtered to Ramanujan-related threads."
        ),
        "mo_unanswered_feed": "https://mathoverflow.net/unanswered",
    },
    "sources": [
        {
            "id": "mo-unanswered",
            "title": "MathOverflow — Unanswered questions",
            "url": "https://mathoverflow.net/unanswered",
            "notes": (
                "Primary live feed for open research questions. Site-wide unanswered "
                "(no upvoted/accepted answer). This project ingests the Ramanujan-tagged "
                "slice via scripts/fetch_mo_unanswered.py → data/kg/mo_unanswered_ramanujan.json "
                "and curates starters in mo_starter_workset.json."
            ),
            "role": "primary_open_problem_feed",
        },
        {
            "id": "mo-377092",
            "title": "The unproved formulas of Ramanujan",
            "url": "https://mathoverflow.net/questions/377092/the-unproved-formulas-of-ramanujan",
            "notes": (
                "Baez asked Berndt: remaining unproved claims? Answer: none. "
                "But: 'There are some statements to which we have not been able to attach meaning.'"
            ),
        },
        {
            "id": "baez-azimuth-2020",
            "title": "Ramanujan’s Last Formula (Azimuth)",
            "url": "https://johncarlosbaez.wordpress.com/2020/11/27/ramanujans-last-formula/",
            "notes": "Write-up of the MO consultation with Berndt; frames the meaning-gap residual.",
        },
        {
            "id": "berndt-li-zaharescu-2019",
            "title": "The final problem: an identity from Ramanujan’s lost notebook",
            "url": "https://www.math.ucdavis.edu/~junxian/paper/finalproblempaper.pdf",
            "notes": (
                "JLMS 2019 — proved the last outstanding Lost Notebook identity "
                "(Entry 1.2 / Bessel-type claim). Status=resolved control."
            ),
        },
        {
            "id": "wolfram-2013",
            "title": "After 100 Years, Ramanujan Gap Filled",
            "url": "https://blog.wolfram.com/2013/05/01/after-100-years-ramanujan-gap-filled/",
            "notes": (
                "Elegant closed form for an incomplete Rogers–Ramanujan continued-fraction "
                "value Ramanujan left unfinished; historically open → filled."
            ),
        },
        {
            "id": "quora-unsolved",
            "title": "Where can I find a list of the unsolved problems of Ramanujan?",
            "url": "https://www.quora.com/Where-can-I-find-a-list-of-the-unsolved-problems-of-Ramanujan",
            "notes": "Secondary; often conflates unproved with unexplained. Verify against Berndt.",
        },
        {
            "id": "berndt-notebooks-i-v",
            "title": "Berndt, Ramanujan's Notebooks Parts I–V (Springer)",
            "url": None,
            "notes": (
                "Primary corpus in this repo. Mine commentary for meaning-gaps and hedges."
            ),
        },
    ],
    "entries": [
        {
            "id": "open:no-assigned-meaning",
            "status": "no_assigned_meaning",
            "label": "Berndt residual: statements without attached meaning (to be mined)",
            "volume_hint": None,
            "chapter_hint": None,
            "entry_hint": None,
            "statement": None,
            "evidence": [
                {
                    "source_id": "mo-377092",
                    "quote": (
                        "To the best of my knowledge, there are no claims or conjectures "
                        "remaining. There are some statements to which we have not been "
                        "able to attach meaning."
                    ),
                    "note": "Berndt via Baez on MO — primary research target for this KG.",
                }
            ],
            "tags": ["needs_mining", "meaning_gap", "priority"],
        },
        {
            "id": "resolved:lost-notebook-final-2019",
            "status": "historically_open_now_proved",
            "label": "Lost Notebook final identity (Berndt–Li–Zaharescu 2019)",
            "volume_hint": "lost-notebook",
            "chapter_hint": None,
            "entry_hint": "Entry 1.2",
            "statement": None,
            "evidence": [
                {
                    "source_id": "berndt-li-zaharescu-2019",
                    "quote": None,
                    "note": "Last unproved Lost Notebook claim; now proved.",
                }
            ],
            "tags": ["resolved", "control", "lost_notebook"],
        },
        {
            "id": "resolved:wolfram-gap-2013",
            "status": "historically_incomplete_now_filled",
            "label": "Wolfram 2013 Rogers–Ramanujan S(q) elegant value",
            "volume_hint": "lost-notebook",
            "chapter_hint": None,
            "entry_hint": None,
            "statement": None,
            "evidence": [
                {
                    "source_id": "wolfram-2013",
                    "quote": None,
                    "note": "Incomplete equation completed with elegant closed form.",
                }
            ],
            "tags": ["resolved", "control", "continued_fractions"],
        },
        {
            "id": "candidate:mock-theta-asymptotic-letter",
            "status": "disputed_or_partial",
            "label": "Mock theta asymptotic claim in Ramanujan→Hardy letter (Watson 1936)",
            "volume_hint": "letters",
            "chapter_hint": None,
            "entry_hint": None,
            "statement": (
                "Asymptotic expansion for a mock-theta-type series as t→0+ with "
                "infinitely many nonzero a_k (see Watson JLMS 1936 pp.57–58)."
            ),
            "evidence": [
                {
                    "source_id": "mo-377092",
                    "quote": None,
                    "note": (
                        "MO answer flagged this letter claim as possibly still not fully proved; "
                        "treat carefully vs Berndt's global 'no remaining claims' statement."
                    ),
                }
            ],
            "tags": ["letters", "mock_theta", "needs_verification"],
        },
    ],
    "mining_cues": [
        # Highest priority: meaning-gap language (Berndt residual category)
        r"unable to discern the meaning",
        r"unable to attach meaning",
        r"attach meaning",
        r"discern the meaning",
        r"do not know the meaning",
        r"meaning of which we are unable",
        r"meaning is unclear",
        r"significance is unclear",
        r"no interpretation",
        r"interpretation is unclear",
        r"not clear what Ramanujan",
        r"Ramanujan's intention",
        r"purpose is unclear",
        r"devoid of meaning",
        r"is meaningless",
        # Proof / correction hedges
        r"unable to prove",
        r"we have not been able to prove",
        r"we cannot prove",
        r"we have been unable",
        r"we are unable",
        r"unable to offer a corrected",
        r"unable to find any formula",
        r"unproved",
        r"unproven",
        r"remains open",
        r"obscure",
        r"mysterious",
        # Weaker / noisy — kept for recall, filtered downstream
        r"incomplete",
        r"no proof",
        r"we do not know",
        r"cannot explain",
    ],
    "cue_priority": {
        "meaning_gap": [
            "unable to discern the meaning",
            "unable to attach meaning",
            "attach meaning",
            "discern the meaning",
            "do not know the meaning",
            "meaning of which we are unable",
            "meaning is unclear",
            "significance is unclear",
            "no interpretation",
            "interpretation is unclear",
            "not clear what Ramanujan",
            "Ramanujan's intention",
            "purpose is unclear",
            "devoid of meaning",
            "is meaningless",
        ],
        "unproved_or_incorrect": [
            "unable to prove",
            "we have not been able to prove",
            "we cannot prove",
            "unable to offer a corrected",
            "unable to find any formula",
            "unproved",
            "unproven",
            "remains open",
        ],
    },
}


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(SEED, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
