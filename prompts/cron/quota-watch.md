---
id: quota-watch
lane: local
audience: local
---
# Provider quota watch

Run a deterministic usage check through the private provider adapter. Compare
usage and reset metadata with configured thresholds, preserving unknown and
unavailable states. Report only the provider-neutral status, threshold crossed,
and next diagnostic step.

Do not print tokens, credentials, account identifiers, raw headers, or full
request payloads. Do not change providers, throttle unrelated jobs, or send an
alert from this contract. Return `NO_OUTPUT` when usage is within bounds.
