"""Deterministic completion reconciliation and safe JSON persistence."""

from __future__ import annotations

import copy
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


def _milestone_map(milestones: Iterable[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        str(item["id"]): item
        for item in milestones
        if isinstance(item, dict) and item.get("id")
    }


def find_repairs(
    milestones: Iterable[dict[str, Any]],
    completion: dict[str, Any],
) -> list[dict[str, Any]]:
    """Find completion entries that lag behind canonical milestone state."""
    canonical = _milestone_map(milestones)
    current = completion.get("items", {})
    if not isinstance(current, dict):
        raise ValueError("completion.items must be an object")

    repairs = []
    for item_id, state in current.items():
        milestone = canonical.get(str(item_id))
        if not milestone or not isinstance(state, dict):
            continue
        if milestone.get("status") == "done" and state.get("status") != "done":
            repairs.append(
                {
                    "item_id": str(item_id),
                    "label": milestone.get("title", str(item_id)),
                    "from_status": state.get("status"),
                    "to_status": "done",
                }
            )
    return sorted(repairs, key=lambda item: item["item_id"])


def apply_repairs(
    completion: dict[str, Any],
    repairs: Iterable[dict[str, Any]],
    *,
    now: datetime | None = None,
    actor: str = "state_audit",
) -> dict[str, Any]:
    """Return a repaired copy without mutating the caller's state."""
    repaired = copy.deepcopy(completion)
    items = repaired.setdefault("items", {})
    if not isinstance(items, dict):
        raise ValueError("completion.items must be an object")
    timestamp = now or datetime.now(timezone.utc)
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    timestamp_text = timestamp.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

    for repair in repairs:
        item_id = str(repair["item_id"])
        items[item_id] = {
            "status": "done",
            "label": repair.get("label", item_id),
            "updated_at": timestamp_text,
            "actor": actor,
            "audit_reason": "Canonical milestone is done; reconciled completion state.",
        }
    return repaired


def load_json_object(path: str | os.PathLike[str]) -> dict[str, Any]:
    with open(path, encoding="utf-8") as source:
        data = json.load(source)
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object: {path}")
    return data


def atomic_write_json(path: str | os.PathLike[str], data: dict[str, Any]) -> None:
    """Write JSON beside the target, then replace it atomically."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as output:
            json.dump(data, output, indent=2, sort_keys=True)
            output.write("\n")
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
