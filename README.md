# Stack Overflow Community Radar

Rank unanswered Stack Overflow questions, map tag clusters, and draft answer briefs from a local community graph.

## What it does

1. Ingest Stack Overflow questions from the Stack Exchange API or bundled sample data.
2. Rank unanswered questions by community urgency.
3. Cluster questions by tag overlap and topic proximity.
4. Generate answer briefs for community contributions.

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

## Run the app

```powershell
streamlit run streamlit_app.py
```

## Data flow

1. `stackoverflow_radar.client` fetches or loads questions.
2. `stackoverflow_radar.graph` builds the local topic graph.
3. `stackoverflow_radar.insights` ranks questions and drafts briefs.
4. `streamlit_app.py` renders the dashboard.

## Notes

- The app falls back to bundled sample questions if the API is unavailable.
- The repo is safe to use offline for development and demos.
