from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def log_step(step: int, tool: str, args: dict[str, Any], result: Any) -> None:
    """Registra un paso del agente en JSON Lines."""
    log_dir = Path(__file__).resolve().parents[2] / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        "ts": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "step": step,
        "tool": tool,
        "args": args,
        "result_summary": str(result)[:200],
    }

    log_file = log_dir / "agent_run.jsonl"
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
