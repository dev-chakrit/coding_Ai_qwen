---
agent: agent
tools: ["localCodingAgent/*"]
description: "Implement with a test-first, repair-loop workflow"
---
Use the testing workflow defined in [../../docs/agent-behavior.md](../../docs/agent-behavior.md) and [../../docs/clean-architecture.md](../../docs/clean-architecture.md).

Task:
${input:task:Describe the feature, bug, or refactor}

Requirements:

- Inspect the relevant code before editing.
- Identify the narrowest useful verification step first.
- If the issue is reproducible, add or update a regression test before the fix when practical.
- Make the implementation change.
- Run the failing test or verification command.
- If it fails, debug the root cause and iterate until green.
- Keep the fix maintainable and aligned with clean architecture.
- End with a short report of what changed and what was verified.
