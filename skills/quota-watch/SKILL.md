# Provider-neutral quota watch

Use this skill for deterministic usage and reset checks.

The private adapter may report normalized usage, limits, reset time, and a
threshold status. The skill must preserve unavailable and unknown states and
must never print credentials, tokens, account identifiers, headers, or raw
payloads.

Quota checks do not change providers, silently throttle unrelated jobs, or send
alerts. They return a local diagnostic for a private policy layer to interpret.
