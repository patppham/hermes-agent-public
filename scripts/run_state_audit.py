#!/usr/bin/env python3
"""Preview deterministic completion repairs for synthetic state."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from runtime.context import parse_timestamp  # noqa: E402
from runtime.state import apply_repairs, find_repairs, load_json_object  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=str(ROOT / "examples/runtime-input.json"))
    parser.add_argument("--now", help="optional ISO timestamp for a deterministic run")
    parser.add_argument("--apply", action="store_true", help="include the repaired copy in output")
    args = parser.parse_args(argv)

    payload = load_json_object(args.input)
    now = parse_timestamp(args.now) if args.now else None
    if args.now and now is None:
        parser.error("--now must be a valid ISO timestamp")
    completion = payload.get("completion", {})
    repairs = find_repairs(payload.get("milestones", []), completion)
    result = {"repairs": repairs, "repair_count": len(repairs)}
    if args.apply:
        result["completion"] = apply_repairs(completion, repairs, now=now)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
