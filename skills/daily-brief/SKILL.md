---
name: daily-brief
description: Produce a concise briefing from verified, fresh context.
---

# Daily brief

## Contract

- Read only the bounded context supplied by the caller.
- Separate facts, conflicts, and proposed next actions.
- Preserve missing or stale-source warnings; never fill gaps from memory.
- Return at most three important bullets and one optional approval request.
- Do not create tasks, send messages, or broaden recipients.

The caller owns source fetching, model routing, delivery, and state updates.
