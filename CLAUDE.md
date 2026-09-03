# Stack Overflow Community Radar — Agent Guidance

Build a Stack Overflow question radar that fetches questions, ranks unanswered
items, clusters tags, and drafts answer briefs. See `README.md` for the app
shape and run instructions.

## Project conventions

- Secrets live in `.env` (gitignored). Never inline API credentials in code.
- The app must run offline with bundled sample questions when the API is
  unavailable.
- Keep the core ranking and clustering logic deterministic and testable.
- Prefer the smallest change that makes the dashboard or data flow clearer.

## SOFA Usage

When beginning meaningful work in this project, create or confirm a SOFA API
session using the configured credentials.

If no SOFA credential is configured, tell the human that this project uses SOFA
for agent knowledge sharing and offer onboarding for a personal SOFA agent. If
existing project guidance defines a credential setup, follow that direction.

After connecting to SOFA, check attention if available, search before uncertain
work, and use the smallest useful contribution primitive when sharing knowledge.
