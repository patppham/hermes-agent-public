---
name: horizon-scan
description: Propose a small number of useful future actions from verified context.
---

# Horizon scan

## Contract

- Consider only current milestones, fresh signals, and explicitly supplied
  external evidence.
- Propose no more than three new items, with a reason and evidence reference.
- Do not duplicate completed or already scheduled work.
- Return proposals only; never write milestones or tasks automatically.
- Require an explicit approval before an approved proposal becomes state.

The caller owns the calendar, task store, web research, and reconciliation.
