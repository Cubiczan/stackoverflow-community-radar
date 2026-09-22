# Stack Overflow Community Radar

Rank unanswered Stack Overflow questions, map tag clusters, and draft answer briefs from a local community graph.

## About

This repo is a lightweight community radar for Stack Overflow. It pulls live
questions when credentials are available, falls back to bundled sample data
when offline, and turns the result into a small topic graph plus answer
briefs. The focus is on deterministic ranking and simple, inspectable outputs
that can be used for research, curation, or content planning.

## What it does

1. Ingest Stack Overflow questions from the Stack Exchange API or bundled sample data.
2. Rank unanswered questions by a deterministic urgency score.
3. Cluster questions by tag overlap and topic proximity.
4. Generate answer briefs for community contributions.
5. Render the result in a Streamlit dashboard.

## Setup

```powershell
python -m venv .venv
python -m pip install -r requirements.txt
```

Put API settings in `.env`:

```
STACK_EXCHANGE_KEY=...
STACK_EXCHANGE_ACCESS_TOKEN=...
STACK_OVERFLOW_SITE=stackoverflow
```

If you do not have API credentials, the app still runs in sample mode.

## Run the app

```powershell
streamlit run streamlit_app.py
```

## Dashboard

The dashboard shows:

1. A priority queue of unanswered or lightly answered questions.
2. A graph summary with tag connectivity.
3. Topic clusters grouped by leading tags.
4. An answer brief with suggested angle and outline.

## Data flow

1. `stackoverflow_radar.client` fetches or loads questions.
2. `stackoverflow_radar.graph` builds the local topic graph.
3. `stackoverflow_radar.insights` ranks questions and drafts briefs.
4. `streamlit_app.py` renders the dashboard.

## Project layout

- `stackoverflow_radar/client.py` - Stack Exchange fetch and offline fallback
- `stackoverflow_radar/graph.py` - topic graph and cluster summaries
- `stackoverflow_radar/insights.py` - priority scoring and answer briefs
- `stackoverflow_radar/sample_data.py` - bundled offline data set
- `streamlit_app.py` - dashboard entry point

## Notes

- The app falls back to bundled sample questions if the API is unavailable.
- The repo is safe to use offline for development and demos.
- The core logic is deterministic so the sample mode can be tested without network access.

## Evidence matrix

Every capability claim in this file is backed by `evidence/matrix.yaml`; CI
refuses builds while any row is unverifiable. The fail-closed verifier
(`tools/verify_evidence_matrix.py`, vendored byte-identical from the
`consensus-hardening-protocol` standard kit, `EVIDENCE_MATRIX_VERIFIER_VERSION`
1.0.0) runs before any install step on every pull request and on pushes to
`main`.
