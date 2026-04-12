---
agent: agent
tools: ["localCodingAgent/*"]
description: "Implement or refine UI with strong UX/UI quality"
---
Use [../../docs/frontend-standards.md](../../docs/frontend-standards.md) and [../../docs/agent-behavior.md](../../docs/agent-behavior.md) as the quality bar.

Task:
${input:task:Describe the screen, component, or visual problem}

Requirements:

- Inspect existing UI structure and styling before editing.
- Preserve the established product language unless the task is a redesign.
- Improve spacing, typography, alignment, and component rhythm deliberately.
- Consider interaction states, accessibility, and responsive behavior.
- Verify the result with the most relevant local checks available.
- If a visual or functional regression appears, fix it before stopping.
- End with a short report of what changed and how the UX/UI improved.
