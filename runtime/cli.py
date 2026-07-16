"""Small read-only demo CLI for the public runtime patterns."""

from __future__ import annotations

import argparse
import json

from .context import parse_timestamp
from .loop import LoopPolicy, run_cycle
from .state import load_json_object


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="synthetic runtime input JSON")
    parser.add_argument("--max-age-hours", type=int, default=24)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--now", help="optional ISO timestamp for deterministic demos")
    parser.add_argument("--approved", action="store_true", help="authorize the synthetic delivery")
    parser.add_argument("--destination", default="example:non-production")
    args = parser.parse_args(argv)

    payload = load_json_object(args.input)
    now = parse_timestamp(args.now) if args.now else None
    if args.now and now is None:
        parser.error("--now must be a valid ISO timestamp")
    cycle = run_cycle(
        payload.get("records", []),
        payload.get("milestones", []),
        payload.get("completion", {}),
        now=now,
        task=payload.get("task"),
        policy=LoopPolicy(
            destination=args.destination,
            max_age_hours=args.max_age_hours,
            context_limit=args.limit,
        ),
        approved=args.approved,
    )
    print(json.dumps(cycle, indent=2, sort_keys=True))
    return 0
