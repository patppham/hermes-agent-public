# Public Hermes runtime template

This repository is a sanitized companion for building a private Hermes
runtime. It contains generic code, contracts, and synthetic fixtures. It is
not a copy of any household deployment.

## Build a private mirror

1. Keep `runtime/` as the deterministic core.
2. Use `cron/jobs.json` as the schedule and execution contract.
3. Use `examples/source-registry.json` and `examples/config.yaml` as shapes;
   replace their disabled placeholders only in a private checkout.
4. Start from the sanitized `SOUL.md`, `.hermes.md`, `prompts/`, and `skills/`
   contracts, then implement source adapters, private prompt values, action
   adapters, and state projections in a private mirror.
5. Run `python3 scripts/validate_public_surface.py` before publishing any
   derived repository.

## Public/private boundary

Public code may contain schemas, validation, bounded projections, routing
contracts, sanitized prompt/skill templates, and synthetic examples. It must not contain real messages, health
or financial records, household identifiers, production destinations,
credentials, auth state, local paths, generated state, or copied private
prompts.

The public runtime authorizes proposals but does not send messages, control
devices, browse authenticated portals, or mutate external systems. Those
adapters belong in the private mirror behind the same approval boundary.

## Verification

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_public_surface.py
python3 -m runtime --input examples/runtime-input.json --now 2026-07-16T12:00:00Z
```
