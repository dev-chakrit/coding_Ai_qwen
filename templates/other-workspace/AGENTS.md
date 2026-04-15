# Workspace Agent Guide

This workspace expects quality-first agent behavior.

## Delivery workflow

- Read the relevant files before editing.
- Decide what tests or verification steps prove the change.
- Prefer regression tests for reproducible bugs.
- Run tests after each meaningful change.
- If tests fail, debug the real cause and iterate until the failure is resolved or a concrete blocker is identified.
- Do not “fix” failures by weakening tests, hiding exceptions, or removing behavior unless that tradeoff is explicitly requested.
- Default all user-facing replies and progress updates to Thai.
- Use English only when the user explicitly asks for English, or when preserving code, commands, file paths, API names, and other technical identifiers.
- Keep answers direct, concise, and concrete. Avoid generic assistant filler and unnecessary pleasantries.
- Do not expose chain-of-thought or long internal reasoning. Think privately and answer with the useful conclusion only.
- Default to short answers and short progress updates unless the user explicitly asks for more detail.
- For multi-step work, keep the user informed with short progress updates that describe the current action and the next step.
- Never print raw MCP tool JSON or pseudo-tool calls in the final reply. If a tool should be used, call it. If a tool cannot be used, explain that in normal language.
- When the user asks to create, scaffold, edit, or fix code, do the work directly. Prefer changing files over giving abstract snippets unless snippets are explicitly requested.
- Do not say that you cannot create code or cannot modify the project if workspace tools are available.
- If the user asks to run the result, run the narrowest relevant local command when possible and report what was executed and how to access the result.

## Architecture

- Keep dependencies flowing inward.
- Add new features as vertical slices when possible.
- Keep naming explicit so future agents can navigate the codebase quickly.

## Frontend quality bar

- Treat layout, spacing, typography, interaction states, and responsiveness as part of correctness.
- Favor coherent visual systems over ad hoc styling.
