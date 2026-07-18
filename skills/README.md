# Public skill contracts

These skills describe reusable loop boundaries, not a household personality or
private prompt set. A private mirror may add its own preferences, sources, and
approval language while keeping these mutation and evidence rules.

Every skill should receive bounded context, preserve missing-source metadata,
and return a small structured result. Skills do not receive credentials or
write to external systems directly.

## Coverage map

The public contracts cover the reusable parts of the private runtime's relevant
skills:

- `household-chief-of-staff/` composes sources, loops, audience boundaries, and
  quiet behavior.
- `email-triage/` preserves the staged metadata-first classifier pipeline.
- `source-projection/` covers registered adapters and generated projections.
- `state-reconciliation/` covers reply closure and completion audits.
- `wellness-evidence/`, `sensor-history/`, and `quota-watch/` cover optional
  evidence streams without exposing their integrations.
- `document-routing/` covers private manifest-first document retrieval.
- `reference-grounding/` covers local references plus current authoritative
  sources for consequential claims.
- `live-dashboard/`, `milestone-dashboard/`, and `playbook-intelligence/` cover
  the dashboard, open-loop, and reusable playbook layers.
- `plan/` and `qa-dogfood/` cover minimal planning and systematic workflow QA.
- `private-reminders/` covers parameterized date and once-only jobs.
- `runtime-architecture/` covers the upstream/private/public layer boundary.
- `action-adapter/` preserves the approval gate for external effects.

Private domain skills such as legal templates, named care plans, provider CLI
recipes, personal training baselines, and reference corpora are intentionally
not copied. A private mirror can implement them behind these contracts.
