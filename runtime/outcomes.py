"""Compact, privacy-safe metrics for a completed runtime cycle."""

from __future__ import annotations

from typing import Any, Mapping


def summarize_cycle(cycle: Mapping[str, Any]) -> dict[str, Any]:
    """Summarize loop progress without copying source records or messages."""
    observed = cycle.get("observe", {})
    source_status = observed.get("source_status", {}) if isinstance(observed, Mapping) else {}
    decision = cycle.get("decide", {})
    action = cycle.get("act", {})
    learning = cycle.get("learn", {})

    received = int(source_status.get("received", 0) or 0)
    included = int(source_status.get("included", 0) or 0)
    proposals = decision.get("proposals", []) if isinstance(decision, Mapping) else []
    repairs = learning.get("repairs", []) if isinstance(learning, Mapping) else []
    delivery_status = action.get("status", "unknown") if isinstance(action, Mapping) else "unknown"

    return {
        "status": cycle.get("status", "unknown"),
        "signals_received": received,
        "signals_observed": included,
        "signals_filtered": max(0, received - included),
        "proposals": len(proposals) if isinstance(proposals, list) else 0,
        "state_repairs": len(repairs) if isinstance(repairs, list) else 0,
        "delivery": delivery_status,
        "quiet": cycle.get("status") == "quiet",
    }
