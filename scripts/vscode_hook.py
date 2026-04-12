from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from local_coding_agent.vscode_hooks import process_hook_event


def main() -> int:
    payload = json.load(sys.stdin)
    profile = os.getenv("LOCAL_CODING_AGENT_HOOK_PROFILE", "")
    workspace_root = Path(payload.get("cwd") or os.getcwd()).resolve()
    result = process_hook_event(payload, workspace_root=workspace_root, profile=profile)
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
