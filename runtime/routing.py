"""Small routing policy for deterministic work and judgment work."""

from __future__ import annotations


LOCAL_TASKS = frozenset({
    "projection",
    "reconcile",
    "triage",
    "health_check",
})
JUDGMENT_TASKS = frozenset({
    "briefing",
    "coach",
    "proposal",
    "scout",
})


def choose_lane(
    task: str,
    *,
    complexity: str = "low",
    needs_judgment: bool | None = None,
) -> dict[str, str]:
    """Return a provider-neutral lane decision.

    The public layer only chooses the kind of execution required. A private
    deployment can map ``local`` and ``judgment`` to its own providers.
    Unknown low-complexity work stays local until a caller opts into judgment.
    """
    normalized_task = str(task).strip().lower()
    normalized_complexity = str(complexity).strip().lower()
    if needs_judgment is None:
        needs_judgment = normalized_task in JUDGMENT_TASKS

    if needs_judgment or normalized_complexity in {"medium", "high"}:
        return {
            "lane": "judgment",
            "reason": "The task needs synthesis, prioritization, or a proposal.",
        }

    return {
        "lane": "local",
        "reason": (
            "The task is a known deterministic operation."
            if normalized_task in LOCAL_TASKS
            else "The task is bounded and can be handled deterministically."
        ),
    }
