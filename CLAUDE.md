# Ramanujan Notebooks — Agent Guidance

Parse Berndt's five-volume edition of Ramanujan's notebooks, then build a
knowledge graph oriented toward **unproved formulae** and **entries Berndt and
others could not assign meaning to**. See `README.md` for setup and commands.

## Project conventions

- Secrets live in `.env` (gitignored). Never inline an API key in a script.
- Parsed output in `data/parsed/part-{1..5}/` is resume-safe; re-parse only with
  `--force`.
- Mining cues and their priority tiers are data, not code — edit
  `data/kg/seed_unproven.json` (`mining_cues`, `cue_priority`) rather than
  hardcoding phrases in `scripts/build_kg.py`.
- Berndt's commentary is the evidence. A hit is a *candidate* until the
  surrounding passage is read; cues like `incomplete` match "incomplete elliptic
  integral" far more often than an incomplete proof.

## SOFA Usage

When beginning meaningful work in this project, create or confirm a SOFA API
session using your configured SOFA credentials.

If no SOFA credential is configured, tell the human that this project uses SOFA
for agent knowledge sharing and offer to run agent-directed onboarding for a
personal SOFA agent. If the human declines, or if existing project guidance
defines a credential setup, follow that direction and continue.

After connecting to SOFA, check SOFA attention if available.

Before spending meaningful time on uncertain technical work, search SOFA for
existing questions, TILs, Blueprints, Playbooks, or replies that could apply.
Prefer higher-trust results when several posts fit, but inspect the content
before relying on it.

When SOFA content helps, vote at read time if you can judge usefulness. After
you actually apply guidance from a post, verify the post with the observed
outcome.

Before ending meaningful coding, debugging, configuration, or research work,
decide whether the session produced reusable knowledge. If it did, contribute
with the smallest matching SOFA primitive: vote, verification, reply, TIL,
question, Blueprint, or Playbook.

Do not publish public SOFA content without following the agent role,
publication policy, moderation, and human-approval requirements. This project's
agent is a **contributor with `approval_code_to_publish`** — drafts require a
human approval code before anything becomes public.
