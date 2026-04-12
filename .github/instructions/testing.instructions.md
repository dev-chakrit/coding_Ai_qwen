---
name: Testing and Repair Loop
description: Test-first and repair-loop workflow for implementation work
applyTo: "**/*"
---
# Testing and Repair Loop

- Before a non-trivial change, identify the relevant tests or verification commands.
- For bugs with a clear reproduction path, prefer writing or updating a regression test first.
- After each meaningful edit, run the narrowest relevant verification step.
- If verification fails, inspect the failure output, fix the real cause, and rerun until the result is stable.
- Do not stop with red tests unless there is a concrete blocker that you clearly explain.
- Do not make tests pass by deleting assertions, muting failures, or lowering quality.
