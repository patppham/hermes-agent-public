---
id: household-health-update
lane: judgment
audience: private
---
# Private household health update

Prepare a private, evidence-aware update from the supplied health and care
context. Use only current records within the configured scope. Preserve the
owner and audience of each datum, identify missing or stale sources, and avoid
turning an observed value into a clinical conclusion.

Summarize only what changed, what may need attention, and one practical next
step when justified. Cite or name the authoritative source for any age-specific,
clinical, legal, or safety-sensitive claim. If nothing is actionable, return
`NO_OUTPUT`.

Write a warm, replyable note rather than a scorecard or checklist. Use no forced
headings, include at most two supporting care metrics, and ask at most one
question only when its answer changes the next support decision. Surface only
the highest-severity verified warning using the adapter's safe wording.

Never expose private details to a shared channel, invent a measurement, alter a
care plan, or send external communication without an approval-gated adapter.
