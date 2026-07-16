"""A provider-neutral Observe -> Verify -> Decide -> Act -> Learn loop."""

from __future__ import annotations

import copy
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Iterable

from .context import build_context, parse_timestamp
from .delivery import DeliveryPolicy
from .outcomes import summarize_cycle
from .routing import choose_lane
from .state import apply_repairs, find_repairs


DecisionFn = Callable[[dict[str, Any]], Iterable[dict[str, Any]]]


@dataclass(frozen=True)
class LoopPolicy:
    """Safety and boundedness settings for one cycle."""

    destination: str = "example:non-production"
    production: bool = False
    require_explicit_approval: bool = True
    max_proposals: int = 3
    max_age_hours: int = 24
    context_limit: int = 20

    def __post_init__(self) -> None:
        if self.max_proposals < 0 or self.max_age_hours < 0 or self.context_limit < 0:
            raise ValueError("loop limits must be non-negative")


def _utc_now(value: datetime | None) -> datetime:
    current = parse_timestamp(value) or datetime.now(timezone.utc)
    return current


def _verification(context: dict[str, Any], repairs: list[dict[str, Any]]) -> dict[str, Any]:
    counters = context["source_status"]
    warnings: list[str] = []
    if counters["invalid"]:
        warnings.append("Some inputs were malformed and were excluded.")
    if counters["stale"]:
        warnings.append("Some inputs were outside the freshness window.")
    if counters["cancelled"]:
        warnings.append("Cancelled or declined inputs were excluded.")

    safe_to_decide = bool(counters["included"] or repairs)
    return {
        "status": "ready" if safe_to_decide else "quiet",
        "safe_to_decide": safe_to_decide,
        "warnings": warnings,
        "filtered_before_decision": max(0, counters["received"] - counters["included"]),
    }


def _default_decision(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    """Return a safe demo proposal; real deployments inject judgment here."""
    context_items = snapshot["context"]["items"]
    if not context_items:
        return []
    return [
        {
            "id": "bounded-brief",
            "kind": "briefing",
            "title": "Prepare a brief from verified signals",
            "reason": f"{len(context_items)} fresh signal(s) passed the verification boundary.",
            "requires_approval": True,
        }
    ]


def _normalize_proposals(
    proposals: Iterable[dict[str, Any]],
    *,
    limit: int,
) -> list[dict[str, Any]]:
    bounded: list[dict[str, Any]] = []
    for proposal in proposals:
        if not isinstance(proposal, dict):
            continue
        proposal_id = str(proposal.get("id", "")).strip()
        title = str(proposal.get("title", "")).strip()
        if not proposal_id or not title:
            continue
        bounded.append(
            {
                "id": proposal_id,
                "kind": str(proposal.get("kind", "action")).strip() or "action",
                "title": title,
                "reason": str(proposal.get("reason", "")).strip(),
                "requires_approval": bool(proposal.get("requires_approval", True)),
            }
        )
        if len(bounded) >= limit:
            break
    return bounded


def _delivery_result(policy: LoopPolicy, proposals: list[dict[str, Any]], approved: bool) -> dict[str, Any]:
    if not proposals:
        return {
            "status": "quiet",
            "destination": None,
            "executed": False,
        }

    requires_approval = policy.require_explicit_approval or any(
        proposal["requires_approval"] for proposal in proposals
    )
    if requires_approval and not approved:
        return {
            "status": "awaiting_approval",
            "destination": None,
            "executed": False,
            "approval_required": True,
        }

    destination = DeliveryPolicy(
        policy.destination,
        production=policy.production,
        require_explicit_approval=requires_approval,
    ).authorize(approved=approved)
    return {
        "status": "authorized",
        "destination": destination,
        "executed": False,
        "approval_required": requires_approval,
    }


def run_cycle(
    records: Iterable[dict[str, Any]],
    milestones: Iterable[dict[str, Any]],
    completion: dict[str, Any],
    *,
    now: datetime | None = None,
    task: dict[str, Any] | None = None,
    policy: LoopPolicy | None = None,
    decide: DecisionFn | None = None,
    approved: bool = False,
) -> dict[str, Any]:
    """Run one bounded cycle without calling providers or executing actions.

    ``decide`` receives only the verified, bounded snapshot. A real runtime can
    inject its model callback there; this package keeps the integration seam
    public while leaving credentials and external action adapters private.
    """
    current = _utc_now(now)
    selected_policy = policy or LoopPolicy()
    task_spec = dict(task or {})
    task_kind = str(task_spec.get("kind", "briefing")).strip() or "briefing"

    context = build_context(
        records,
        now=current,
        max_age_hours=selected_policy.max_age_hours,
        limit=selected_policy.context_limit,
    )
    repairs = find_repairs(milestones, completion)
    verification = _verification(context, repairs)
    route = choose_lane(
        task_kind,
        complexity=str(task_spec.get("complexity", "low")),
        needs_judgment=task_spec.get("needs_judgment"),
    )

    snapshot = {
        "context": context,
        "verification": verification,
        "state": {"repairs": repairs},
        "task": task_spec,
        "route": route,
    }
    decision_invoked = bool(verification["safe_to_decide"])
    if decision_invoked:
        raw_proposals = decide(snapshot) if decide else _default_decision(snapshot)
    else:
        raw_proposals = []
    proposals = _normalize_proposals(raw_proposals, limit=selected_policy.max_proposals)

    act = _delivery_result(selected_policy, proposals, approved)
    repaired_completion = (
        apply_repairs(completion, repairs, now=current)
        if repairs
        else copy.deepcopy(completion)
    )
    learn = {
        "repairs": repairs,
        "completion": repaired_completion,
    }
    if proposals and act["status"] == "awaiting_approval":
        status = "needs_approval"
    elif proposals:
        status = "authorized"
    elif repairs:
        status = "state_reconciled"
    else:
        status = "quiet"

    cycle = {
        "generated_at": current.isoformat().replace("+00:00", "Z"),
        "status": status,
        "observe": context,
        "verify": verification,
        "decide": {
            "invoked": decision_invoked,
            "route": route,
            "proposals": proposals,
        },
        "act": act,
        "learn": learn,
        "trace": [
            {"stage": "observe", "status": "complete"},
            {"stage": "verify", "status": verification["status"]},
            {"stage": "decide", "status": "invoked" if decision_invoked else "skipped"},
            {"stage": "act", "status": act["status"]},
            {"stage": "learn", "status": "complete"},
        ],
    }
    cycle["outcome"] = summarize_cycle(cycle)
    return cycle
