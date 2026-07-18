#!/usr/bin/env python3
"""Run one sanitized runtime cycle without executing external actions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from runtime.context import parse_timestamp  # noqa: E402
from runtime.loop import LoopPolicy, run_cycle  # noqa: E402
from runtime.state import load_json_object  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=str(ROOT / "examples/runtime-input.json"))
    parser.add_argument("--task", help="override the task kind in the synthetic input")
    parser.add_argument("--now", help="optional ISO timestamp for a deterministic run")
    parser.add_argument("--destination", default="example:non-production")
    parser.add_argument("--approved", action="store_true")
    args = parser.parse_args(argv)

    payload = load_json_object(args.input)
    now = parse_timestamp(args.now) if args.now else None
    if args.now and now is None:
        parser.error("--now must be a valid ISO timestamp")
    task = dict(payload.get("task") or {})
    if args.task:
        task["kind"] = args.task

    cycle = run_cycle(
        payload.get("records", []),
        payload.get("milestones", []),
        payload.get("completion", {}),
        now=now,
        task=task,
        policy=LoopPolicy(destination=args.destination),
        approved=args.approved,
    )
    print(json.dumps(cycle, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
