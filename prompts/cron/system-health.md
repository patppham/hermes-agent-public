---
id: system-health
lane: local
audience: local
---
# Runtime health

Run deterministic checks and report the layers separately:

- job execution and last-error state;
- source freshness and projection validity;
- delivery success versus delivery configuration; and
- process or endpoint liveness.

Treat intentionally disabled or parked components as expected when the private
configuration says so. Do not call a green scheduler timestamp healthy when a
job has an error, a source is stale, or delivery failed. Report a small,
actionable diagnosis with the owning component and the safest next check.

Do not restart services, enable sidecars, send alerts, or change configuration
from this contract. Recovery and notification remain explicit private adapters.
