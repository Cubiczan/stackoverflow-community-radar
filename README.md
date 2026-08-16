# Ramanujan Notebooks — Parse, Index & Knowledge Graph

Parse Bruce Berndt’s five-volume edition of Ramanujan’s notebooks with LlamaParse, then build a knowledge graph on two tracks:

1. **Berndt meaning-gaps** — statements without assigned meaning in the notebooks  
2. **MathOverflow unanswered** — live open questions from [mathoverflow.net/unanswered](https://mathoverflow.net/unanswered) (Ramanujan-tagged slice)

## Research stance

Per Berndt (via [MO 377092](https://mathoverflow.net/questions/377092/the-unproved-formulas-of-ramanujan)):

- No remaining *unproved* Ramanujan claims (Lost Notebook final identity proved 2019).
- Residual research target: statements editors **could not attach meaning** to.

In parallel, treat **[MO unanswered](https://mathoverflow.net/unanswered)** as the primary live feed for open Ramanujan-adjacent problems (1/π series, CFs, motives, etc.).

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Put your key in `.env` (gitignored):

```
LLAMA_CLOUD_API_KEY=llx-...
```

## Parse all five volumes

```powershell
$env:PYTHONIOENCODING="utf-8"
python scripts/parse_notebooks.py
```

Outputs: `data/parsed/<volume>/full.md` + `job.json`. Resume-safe (`--force` to redo). Default tier: `agentic`.

## Seed + MO unanswered + build KG

```powershell
python scripts/seed_unproven_corpus.py
python scripts/fetch_mo_unanswered.py   # refresh from mathoverflow.net/unanswered
python scripts/build_kg.py              # Berndt mining + MO starter + formula_*.json
```

Key outputs under `data/kg/`:

| File | Role |
|------|------|
| `mo_unanswered_ramanujan.json` | Ramanujan slice of MO unanswered |
| `mo_starter_workset.json` / `MO_STARTER.md` | Curated queue from that feed |
| `meaning_gaps_curated.json` | Deduped Berndt meaning-gap clusters |
| `proof_sketches/mo462327_elementary.md` | Elementary CF sketch |
| `formula_mo514194_s*.json` | Split 1/π² series nodes |
| `graph.json` / `graph.graphml` | Full KG |

## Sources

- **[MathOverflow unanswered](https://mathoverflow.net/unanswered)** — primary open-problem feed  
- [The unproved formulas of Ramanujan](https://mathoverflow.net/questions/377092/the-unproved-formulas-of-ramanujan)  
- [Wolfram: Ramanujan gap filled](https://blog.wolfram.com/2013/05/01/after-100-years-ramanujan-gap-filled/)  
- [Berndt–Li–Zaharescu 2019](https://www.math.ucdavis.edu/~junxian/paper/finalproblempaper.pdf)  
- Berndt, *Ramanujan’s Notebooks* Parts I–V (local PDFs)
