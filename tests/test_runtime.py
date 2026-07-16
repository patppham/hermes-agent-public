import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from runtime.context import build_context
from runtime.delivery import DeliveryPolicy
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


if __name__ == "__main__":
    unittest.main()
