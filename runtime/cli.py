"""Small read-only demo CLI for the public runtime patterns."""

from __future__ import annotations

import argparse
import json

from .context import build_context
from .state import find_repairs, load_json_object


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="synthetic runtime input JSON")
    parser.add_argument("--max-age-hours", type=int, default=24)
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args(argv)

    payload = load_json_object(args.input)
    context = build_context(
        payload.get("records", []),
        max_age_hours=args.max_age_hours,
        limit=args.limit,
    )
    repairs = find_repairs(payload.get("milestones", []), payload.get("completion", {}))
    print(json.dumps({"context": context, "repairs": repairs}, indent=2, sort_keys=True))
    return 0
