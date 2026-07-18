---
name: system-health
description: Report runtime execution and delivery health without restarting services blindly.
---

# System health

## Contract

- Distinguish job execution, source freshness, delivery, and service health.
- Report the last known failure class and the affected contract.
- Treat intentionally parked or disabled components as expected state.
- Prefer a deterministic check or dry run before invoking a model.
- Never start a sidecar, repair a production route, or send an alert without
  an explicit private policy.
