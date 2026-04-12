# Project AI Instructions

- Inspect the relevant files and project structure before editing.
- Define the smallest useful verification step before changing non-trivial code.
- Prefer adding or updating regression tests for reproducible failures.
- After each meaningful change, run the narrowest relevant tests first.
- If a test or verification step fails, debug the root cause, implement a maintainable fix, rerun the failing check, and continue until green or blocked.
- Do not weaken tests, delete coverage, suppress errors, or use hacky fallbacks just to get a passing result unless explicitly asked.
- For multi-step tasks, provide brief progress updates so the user can see what is being inspected, changed, and verified.
- Keep clean architecture boundaries intact according to [docs/clean-architecture.md](../docs/clean-architecture.md).
- For frontend work, follow [docs/frontend-standards.md](../docs/frontend-standards.md) and treat UX/UI polish as part of the acceptance criteria.
