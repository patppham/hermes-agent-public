---
id: projection-refresh
lane: local
audience: local
---
# Projection refresh

This is a deterministic job. Do not invoke a judgment model.

Read the private source registry, query only enabled adapters, normalize the
returned records, and write the generated projection atomically. Preserve
source timestamps, freshness, missing-source reasons, cancellation markers,
ownership, and confidence metadata. Exclude records that the registry marks
out of scope. A failed or empty adapter must not become a fabricated zero or a
false healthy result.

Return a local audit containing source counts, stale/missing sources, and write
status. Do not send a message, mutate canonical milestones, or include raw
payloads in the result.
