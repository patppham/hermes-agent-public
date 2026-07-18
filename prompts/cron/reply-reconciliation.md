---
id: reply-reconciliation
lane: local
audience: local
---
# Reply reconciliation

Reconcile new replies against pending proposals and canonical state. Apply only
unambiguous approvals or rejections, deduplicate already handled messages, and
record the reason for every state transition. Preserve the originating owner,
audience, and proposal identifier.

Ambiguous replies must not mutate state. Emit one private clarification request
through the configured adapter when clarification is allowed; otherwise record
the pending ambiguity locally. If there are no new replies, return `NO_OUTPUT`.

Do not generate new plans, infer consent from silence, replay a transition, or
send to a shared destination from this deterministic contract.
