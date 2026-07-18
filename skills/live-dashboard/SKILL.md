# Live dashboard projection

Use this contract for a dashboard that serves both a human-facing view and
machine-readable projections.

Keep canonical milestones separate from generated views. Build the view from
validated source data, preserve stable identifiers and completion semantics,
and write files atomically so an interrupted refresh cannot leave a partial
projection. Treat source freshness and missing integrations as visible state.

The dashboard may link to a private action or document, but it does not expose
private payloads by default, control devices, or become a second state store.
Authenticated hosting, tunnels, paths, and delivery remain private adapters.
