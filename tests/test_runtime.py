import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from runtime.context import build_context
from runtime.delivery import DeliveryPolicy
from runtime.loop import LoopPolicy, run_cycle
from runtime.parallel import run_parallel
from runtime.state import apply_repairs, atomic_write_json, find_repairs, load_json_object


NOW = datetime(2026, 7, 16, 12, tzinfo=timezone.utc)


class ContextTests(unittest.TestCase):
    def test_context_filters_stale_disabled_and_cancelled_records(self):
        records = [
            {
                "id": "valid",
                "source": "example",
                "title": "Valid record",
                "timestamp": "2026-07-16T11:00:00Z",
            },
            {
                "id": "stale",
                "source": "example",
                "title": "Stale record",
                "timestamp": "2026-07-14T11:00:00Z",
            },
            {
                "id": "disabled",
                "source": "example",
                "title": "Disabled record",
                "timestamp": "2026-07-16T11:00:00Z",
                "enabled": False,
            },
            {
                "id": "cancelled",
                "source": "example",
                "title": "Canceled: record",
                "timestamp": "2026-07-16T10:00:00Z",
            },
        ]

        result = build_context(records, now=NOW, max_age_hours=24)

        self.assertEqual([item["id"] for item in result["items"]], ["valid"])
        self.assertEqual(
            result["source_status"],
            {
                "received": 4,
                "included": 1,
                "disabled": 1,
                "invalid": 0,
                "stale": 1,
                "cancelled": 1,
                "over_limit": 0,
            },
        )

    def test_context_is_bounded_and_deterministic(self):
        records = [
            {"id": "b", "timestamp": "2026-07-16T10:00:00Z"},
            {"id": "a", "timestamp": "2026-07-16T10:00:00Z"},
            {"id": "c", "timestamp": "2026-07-16T09:00:00Z"},
        ]

        result = build_context(records, now=NOW, limit=2)

        self.assertEqual([item["id"] for item in result["items"]], ["b", "a"])
        self.assertEqual(result["source_status"]["over_limit"], 1)


class StateTests(unittest.TestCase):
    def test_reconcile_and_apply_repairs(self):
        milestones = [{"id": "one", "title": "One", "status": "done"}]
        completion = {"items": {"one": {"status": "open"}}}

        repairs = find_repairs(milestones, completion)
        repaired = apply_repairs(completion, repairs, now=NOW)

        self.assertEqual(repairs[0]["item_id"], "one")
        self.assertEqual(repaired["items"]["one"]["status"], "done")
        self.assertEqual(completion["items"]["one"]["status"], "open")

    def test_atomic_json_write_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "state.json"
            atomic_write_json(target, {"ok": True})
            self.assertEqual(load_json_object(target), {"ok": True})


class DeliveryTests(unittest.TestCase):
    def test_delivery_requires_approval(self):
        policy = DeliveryPolicy("example:non-production")

        with self.assertRaises(PermissionError):
            policy.authorize()
        self.assertEqual(policy.authorize(approved=True), "example:non-production")

    def test_empty_destination_is_rejected(self):
        with self.assertRaises(ValueError):
            DeliveryPolicy(" ").authorize(approved=True)


class LoopTests(unittest.TestCase):
    def test_cycle_waits_for_approval_and_reconciles_state(self):
        records = [
            {
                "id": "signal-1",
                "source": "synthetic-calendar",
                "title": "Review the launch checklist",
                "timestamp": "2026-07-16T11:00:00Z",
            }
        ]
        milestones = [{"id": "launch", "title": "Launch checklist", "status": "done"}]
        completion = {"items": {"launch": {"status": "open"}}}

        cycle = run_cycle(
            records,
            milestones,
            completion,
            now=NOW,
            task={"kind": "briefing", "needs_judgment": True},
        )

        self.assertEqual(cycle["status"], "needs_approval")
        self.assertEqual(cycle["decide"]["route"]["lane"], "judgment")
        self.assertEqual(cycle["act"]["status"], "awaiting_approval")
        self.assertEqual(cycle["act"]["destination"], None)
        self.assertEqual(cycle["learn"]["repairs"][0]["item_id"], "launch")
        self.assertEqual(cycle["learn"]["completion"]["items"]["launch"]["status"], "done")
        self.assertEqual(cycle["outcome"]["signals_observed"], 1)

    def test_cycle_skips_decision_when_no_fresh_signal_exists(self):
        def should_not_run(snapshot):
            raise AssertionError(f"decision callback received empty snapshot: {snapshot}")

        cycle = run_cycle(
            [{"id": "old", "timestamp": "2026-07-14T11:00:00Z"}],
            [],
            {"items": {}},
            now=NOW,
            decide=should_not_run,
        )

        self.assertEqual(cycle["status"], "quiet")
        self.assertFalse(cycle["decide"]["invoked"])
        self.assertEqual(cycle["outcome"]["delivery"], "quiet")

    def test_approved_cycle_authorizes_but_does_not_execute(self):
        cycle = run_cycle(
            [{"id": "signal-1", "timestamp": "2026-07-16T11:00:00Z"}],
            [],
            {"items": {}},
            now=NOW,
            policy=LoopPolicy(destination="example:non-production"),
            approved=True,
        )

        self.assertEqual(cycle["status"], "authorized")
        self.assertEqual(cycle["act"]["destination"], "example:non-production")
        self.assertFalse(cycle["act"]["executed"])


class ParallelTests(unittest.TestCase):
    def test_parallel_tasks_have_stable_safe_results(self):
        results = run_parallel(
            {
                "ok": lambda: "synthetic result",
                "failed": lambda: 1 / 0,
            },
            max_workers=2,
        )

        self.assertEqual(list(results), ["failed", "ok"])
        self.assertEqual(results["ok"], {"status": "ok", "result": "synthetic result"})
        self.assertEqual(results["failed"], {"status": "error", "error_type": "ZeroDivisionError"})


if __name__ == "__main__":
    unittest.main()
