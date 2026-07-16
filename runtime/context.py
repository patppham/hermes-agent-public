"""Build small, deterministic context objects from fresh input records."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Iterable


CANCELLED_STATUSES = {"cancelled", "canceled", "declined", "deleted"}
CANCELLED_PREFIXES = ("cancelled:", "canceled:")


def parse_timestamp(value: Any) -> datetime | None:
    """Parse an ISO timestamp as UTC, returning ``None`` for invalid input."""
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, str) and value.strip():
        try:
            parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
        except ValueError:
            return None
    else:
        return None

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _is_cancelled(record: dict[str, Any]) -> bool:
    status = str(record.get("status", "")).strip().lower()
    title = str(record.get("title", "")).strip().lower()
    if status in CANCELLED_STATUSES or title.startswith(CANCELLED_PREFIXES):
        return True

    attendees = record.get("attendees")
    return bool(
        isinstance(attendees, list)
        and attendees
        and all(
            isinstance(attendee, dict)
            and str(attendee.get("response", "")).lower() == "declined"
            for attendee in attendees
        )
    )


def _project(record: dict[str, Any], timestamp: datetime) -> dict[str, Any]:
    """Keep only fields intended for a bounded model-facing context."""
    projected = {
        "id": record.get("id"),
        "source": record.get("source", "unknown"),
        "title": record.get("title", ""),
        "summary": record.get("summary", ""),
        "timestamp": timestamp.isoformat().replace("+00:00", "Z"),
        "status": record.get("status", "unknown"),
    }
    return {key: value for key, value in projected.items() if value not in (None, "")}


def build_context(
    records: Iterable[dict[str, Any]],
    *,
    now: datetime | None = None,
    max_age_hours: int = 24,
    limit: int = 20,
) -> dict[str, Any]:
    """Return a bounded context and explicit source-quality counters.

    Disabled, stale, cancelled, malformed, and over-limit records never reach
    the returned ``items`` list. No values are invented for missing fields.
    """
    if max_age_hours < 0 or limit < 0:
        raise ValueError("max_age_hours and limit must be non-negative")

    current = parse_timestamp(now) or datetime.now(timezone.utc)
    counters = {
        "received": 0,
        "included": 0,
        "disabled": 0,
        "invalid": 0,
        "stale": 0,
        "cancelled": 0,
        "over_limit": 0,
    }
    candidates: list[tuple[datetime, dict[str, Any]]] = []
    cutoff = current - timedelta(hours=max_age_hours)

    for record in records:
        counters["received"] += 1
        if not isinstance(record, dict):
            counters["invalid"] += 1
            continue
        if record.get("enabled", True) is False:
            counters["disabled"] += 1
            continue
        timestamp = parse_timestamp(record.get("timestamp") or record.get("updated_at"))
        if timestamp is None:
            counters["invalid"] += 1
            continue
        if timestamp < cutoff or timestamp > current:
            counters["stale"] += 1
            continue
        if _is_cancelled(record):
            counters["cancelled"] += 1
            continue
        candidates.append((timestamp, _project(record, timestamp)))

    candidates.sort(key=lambda item: (item[0], str(item[1].get("id", ""))), reverse=True)
    included = candidates[:limit]
    counters["included"] = len(included)
    counters["over_limit"] = max(0, len(candidates) - len(included))

    return {
        "generated_at": current.isoformat().replace("+00:00", "Z"),
        "window_hours": max_age_hours,
        "items": [item for _, item in included],
        "source_status": counters,
    }
