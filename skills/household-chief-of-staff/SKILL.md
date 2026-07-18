# Chief-of-staff composition

Use this skill when composing a local-first assistant from projections, skills,
and scheduled loops. It is a public contract, not a household persona.

## Operating model

1. Read the source registry and the smallest relevant prepared projections.
2. Verify freshness, ownership, cancellation, and missing-source metadata.
3. Choose deterministic code for exact reconciliation or a judgment lane for
   bounded interpretation.
4. Produce a useful result or an explicit no-op.
5. Put every mutation behind canonical state and an approval-gated adapter.

## Communication

Separate shared coordination from private-owner work before writing. A shared
result must not contain a private record merely because the source was
available. Prefer one practical implication and one next action over a complete
dump of every input.

## Source and state boundaries

The context builder owns fetching and normalization. The skill consumes bounded
records and must preserve source timestamps and confidence. Canonical state owns
commitments; generated dashboards and summaries are projections. Do not silently
repair, create, or close a commitment from a narrative response.

## Quiet behavior

Return `NO_OUTPUT` when no material change, useful question, authorized action,
or meaningful warning exists. A scheduled invocation is not a reason to send a
message.
