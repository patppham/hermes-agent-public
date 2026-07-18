# Canonical state reconciliation

Use this skill for completion audits, reply handling, and other deterministic
state transitions.

## Rules

1. Load canonical state and generated views separately.
2. Match records using stable identifiers, never display text alone.
3. Apply only an unambiguous, allowed transition.
4. Make the transition idempotent and record its reason.
5. Preserve owner, audience, timestamps, and source evidence.
6. Leave ambiguity unresolved or request one private clarification.

Reconciliation is not planning. It must not invent tasks, infer consent from
silence, rewrite a user's notes, or ask a model to decide an exact comparison.
External mutations and delivery are separate approval-gated adapters.
