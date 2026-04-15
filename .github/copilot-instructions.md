# Project AI Instructions

- Inspect the relevant files and project structure before editing.
- Define the smallest useful verification step before changing non-trivial code.
- Prefer adding or updating regression tests for reproducible failures.
- After each meaningful change, run the narrowest relevant tests first.
- If a test or verification step fails, debug the root cause, implement a maintainable fix, rerun the failing check, and continue until green or blocked.
- Do not weaken tests, delete coverage, suppress errors, or use hacky fallbacks just to get a passing result unless explicitly asked.
- Default all user-facing replies and progress updates to Thai.
- Use English only when the user explicitly asks for English, or when preserving code, commands, file paths, API names, and other technical identifiers.
- Keep replies concise, direct, and technical. Avoid generic assistant filler.
- Do not expose chain-of-thought or long internal reasoning. Summarize only the decision or result that matters.
- Default to short answers and short progress updates unless the user explicitly asks for detail.
- Never print raw MCP tool JSON or pseudo-tool calls in the final reply. If a tool should be used, call it. If a tool cannot be used, explain that in normal language.
- When the user asks to create, scaffold, edit, or fix code, perform the code change directly instead of stopping at explanation or sample snippets unless snippets are explicitly requested.
- Do not claim that you cannot create code or cannot modify files if the workspace tools can do it.
- If the user asks to run, preview, or demonstrate the result, execute the narrowest relevant command when possible and report the concrete outcome.
- For multi-step tasks, provide brief progress updates so the user can see what is being inspected, changed, and verified.
- Keep clean architecture boundaries intact according to [docs/clean-architecture.md](../docs/clean-architecture.md).
- For frontend work, follow [docs/frontend-standards.md](../docs/frontend-standards.md) and treat UX/UI polish as part of the acceptance criteria.
