# Workspace Agent Guide

This repository expects quality-first agent behavior.

## Delivery workflow

- Read the relevant files before editing.
- Decide what tests or verification steps prove the change.
- Prefer regression tests for reproducible bugs.
- Run tests after each meaningful change.
- If tests fail, debug the real cause and iterate until the failure is resolved or a concrete blocker is identified.
- Do not “fix” failures by weakening tests, hiding exceptions, or removing behavior unless that tradeoff is explicitly requested.
- For multi-step work, keep the user informed with short progress updates that describe the current action and the next step.

## Architecture

- Keep dependencies flowing inward as documented in `docs/clean-architecture.md`.
- Add new features as vertical slices when possible.
- Keep naming explicit so future agents can navigate the codebase quickly.

## Frontend quality bar

- Treat layout, spacing, typography, interaction states, and responsiveness as part of correctness.
- Use `docs/frontend-standards.md` when creating or editing UI.
- Favor coherent visual systems over ad hoc styling.
