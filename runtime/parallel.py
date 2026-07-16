"""Bounded, provider-neutral fan-out for background work lanes."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Mapping


TaskFn = Callable[[], Any]


def run_parallel(
    tasks: Mapping[str, TaskFn],
    *,
    max_workers: int = 3,
) -> dict[str, dict[str, Any]]:
    """Run named tasks with a small worker cap and stable result ordering.

    Results are returned to the caller and never persisted by this package.
    Exception messages are intentionally omitted so a provider or connector
    cannot accidentally turn a private error string into a public trace.
    """
    if max_workers < 1:
        raise ValueError("max_workers must be positive")
    normalized = dict(sorted(tasks.items(), key=lambda item: str(item[0])))
    if any(not isinstance(name, str) or not name.strip() for name in normalized):
        raise ValueError("task names must be non-empty strings")
    if any(not callable(task) for task in normalized.values()):
        raise ValueError("tasks must be callable")
    if not normalized:
        return {}

    with ThreadPoolExecutor(max_workers=min(max_workers, len(normalized))) as pool:
        futures = {name: pool.submit(task) for name, task in normalized.items()}
        results: dict[str, dict[str, Any]] = {}
        for name, future in futures.items():
            try:
                results[name] = {"status": "ok", "result": future.result()}
            except Exception as exc:  # noqa: BLE001 - return a safe error class only
                results[name] = {"status": "error", "error_type": type(exc).__name__}
        return results
