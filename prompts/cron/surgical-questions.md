---
id: surgical-questions
lane: judgment
audience: routed-private
---
# Surgical questions

Use the deterministic candidate scan supplied by the private adapter. If there
are no unresolved, useful unknowns, return `wakeAgent: false` and `NO_OUTPUT`.

When a question is justified, ask at most one. Prioritize a deadline or blocked
decision, then a high-impact ambiguity, then a low-cost preference. Make the
question answerable in one short reply and route it only to the configured
owner. Include enough context that the owner does not need to reconstruct the
scan, but do not disclose unrelated private data.

Do not ask for information already present, turn curiosity into a task, repeat
a handled question, or send a shared message without explicit routing.
