# Source projection

Use this skill for deterministic collection and normalization of external or
local evidence into a generated projection.

## Contract

- Read an explicit source registry rather than discovering accounts implicitly.
- Query only enabled, authorized adapters.
- Normalize timestamps, identity, ownership, status, and units.
- Preserve freshness, missing-source reasons, cancellation, and confidence.
- Exclude out-of-scope or fully cancelled records according to policy.
- Write projections atomically and make reruns idempotent.
- Keep raw payloads and credentials outside the projection and repository.

An adapter failure is not an empty success. Return a typed diagnostic so a
consumer can distinguish no data, stale data, unavailable data, and invalid
data. Projection jobs do not send messages or mutate canonical commitments.
