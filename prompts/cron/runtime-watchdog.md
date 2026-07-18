---
id: runtime-watchdog
lane: local
audience: local
---
# Runtime watchdog

Run the deterministic allowlisted health and recovery checks for the local
runtime. Separate dashboard, gateway, worker, and delivery observations. Use
bounded retries and idempotent recovery, and record what was checked and what
changed.

Do not start disabled or parked sidecars, enable experimental integrations,
change credentials, or send a production message. Escalate only a persistent,
well-classified failure through the private alert adapter. Return `NO_OUTPUT`
when the runtime is healthy.
