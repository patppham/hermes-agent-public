#!/usr/bin/env python3
"""Build a bounded context projection from synthetic input records."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from runtime.context import build_context, parse_timestamp  # noqa: E402
from runtime.state import load_json_object  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=str(ROOT / "examples/runtime-input.json"))
    parser.add_argument("--now", help="optional ISO timestamp for a deterministic run")
    parser.add_argument("--max-age-hours", type=int, default=24)
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args(argv)

    payload = load_json_object(args.input)
    now = parse_timestamp(args.now) if args.now else None
    if args.now and now is None:
        parser.error("--now must be a valid ISO timestamp")
    projection = build_context(
        payload.get("records", []),
        now=now,
        max_age_hours=args.max_age_hours,
        limit=args.limit,
    )
    print(json.dumps(projection, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
