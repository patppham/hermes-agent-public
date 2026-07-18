# Mirroring the runtime privately

The public repository is designed to let an agent reconstruct the runtime
shape without receiving the household runtime itself. Treat it as a blueprint
and contract library, not as a data export.

## What maps to what

| Private runtime responsibility | Public contract | Private implementation remains responsible for |
| --- | --- | --- |
| Shared source projection | `runtime/context.py` | Gmail, calendar, health, sleep, and local sensor adapters |
| Canonical milestones and completion state | `runtime/state.py` | Household records, databases, and vault paths |
| Daily brief, coaching, scout, and proposal loops | `runtime/loop.py` plus `prompts/cron/*` | Private prompt values, model calls, evidence policy, and domain-specific judgment |
| Local-versus-judgment model routing | `runtime/routing.py` | Provider names, credentials, cost limits, and fallback behavior |
| Reply and approval handling | `runtime/delivery.py` plus `runtime/loop.py` | Messaging connectors, identity routing, and natural-language parsing |
| Background work lanes | `runtime/parallel.py` | Actual subagents, connector calls, retries, and cancellation policy |
| Dashboard and job health | `scripts/validate_public_surface.py` | Live probes, watchdogs, delivery telemetry, and private alert routes |
| Persona and orchestration guidance | `SOUL.md` and `.hermes.md` | Household identity, preferences, memory, paths, accounts, and local policy |
| Household skills | `skills/*/SKILL.md` | Private prompts, preferences, source references, personal policy, and credentials |

The private `dashboard/`, `scripts/`, `bridge/`, and retrieval trees contain
many integration-specific files. Their public counterpart is represented in
[`examples/runtime-surface.json`](../examples/runtime-surface.json), not by
copying their source or data. The `lsp/node_modules/` tree is dependency noise
and is never part of the mirror.

## Replication sequence

An agent building a private mirror should work in this order:

1. Copy the public `runtime/` package and its tests.
2. Create private source adapters that emit the bounded record shape accepted
   by `build_context`.
3. Create canonical state files or a private state store, then use
   deterministic reconciliation before model-driven work.
4. Implement one decision callback per high-judgment loop. Give it only the
   verified snapshot returned by `run_cycle`.
5. Copy the prompt files and persona/runtime guidance as templates. Replace
   placeholders in private files only; keep the public copies generic.
6. Map the generic lanes in `cron/jobs.json` to private scripts and providers.
7. Add private skills and prompts using the public skill contracts as their
   safety and mutation boundaries.
8. Add action adapters last. They may consume an authorized proposal, but the
   public contract never supplies credentials or production destinations.

## What must stay private

Keep these outside any public mirror:

- `.env`, auth files, OAuth tokens, databases, logs, sessions, caches, and
  generated projections;
- real email, calendar, health, sleep, financial, insurance, or household
  records;
- personal names, dates, phone numbers, chat IDs, local filesystem paths, and
  production delivery targets;
- private prompt values, household policy, persona preferences, source-specific
  reference corpora, and browser/action scripts for authenticated portals;
- archived or parked experiments whose fixtures contain household evidence.

The closest safe public equivalent is a synthetic fixture plus an explicit
adapter seam. Redaction is not a substitute for removing the original data
from repository history.
