---
name: reply-reconciliation
description: Reconcile unambiguous approvals and keep ambiguous replies safe.
---

# Reply reconciliation

## Contract

- Match a reply to a previously presented proposal using stable identifiers.
- Apply only unambiguous approval or rejection decisions.
- Deduplicate already handled replies.
- Route ambiguity back for clarification; never guess a mutation.
- Update canonical state deterministically and record an audit reason.

The adapter that reads messages and the adapter that writes state remain
private deployment components.
