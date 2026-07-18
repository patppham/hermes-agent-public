---
id: todo-audit
lane: local
audience: local
---
# Completion audit

Compare generated task views with canonical milestone state. Repair only an
unambiguous completion mismatch, using an idempotent transition and an audit
reason. Preserve the canonical schema and ownership metadata.

Return the repaired identifiers and unresolved mismatches. If there is nothing
to repair, return `NO_OUTPUT`. This job is reconciliation, not planning: do not
invent tasks, rewrite notes, reorder priorities, or ask a model to brainstorm.

Do not deliver a user-facing message or mutate external systems.
