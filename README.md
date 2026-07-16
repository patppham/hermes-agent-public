# Hermes Runtime Patterns

A sanitized, shareable reference for building a local [Hermes Agent](https://github.com/NousResearch/hermes-agent) runtime.

This is an independent companion project, not an official Hermes distribution. It documents a small set of reusable runtime patterns without publishing a live assistant configuration.

## What is included

- `runtime/` — a dependency-free reference implementation of bounded context building, a five-stage closed loop, deterministic state reconciliation, routing boundaries, bounded background fan-out, outcome summaries, and explicit delivery authorization.
- `tests/` — standard-library tests for the public runtime layer.
- `docs/architecture.md` — the runtime boundary and data flow.
- `examples/` — provider, job, source, skill, and runtime-input placeholders.

## Privacy boundary

This repository contains only generic runtime code, documentation, and synthetic examples. It does not contain:

- credentials, tokens, auth state, databases, logs, or session history;
- real messages, email/calendar identifiers, health records, financial records, or household data;
- names, addresses, phone numbers, production destinations, or local machine paths;
- a copy of a live runtime or upstream source checkout.

Every identifier in `examples/` is synthetic. Keep real runtime configuration in a private repository and inject secrets through the environment or a local secret manager.

## How to use the patterns

1. Install and configure the upstream Hermes Agent project.
2. Copy the example shapes into a private runtime repository.
3. Replace placeholders with local values without committing them.
4. Keep generated projections, logs, sessions, and account routing private.

Run the sanitized reference runtime locally:

```bash
python3 -m unittest discover -s tests -v
python3 -m runtime --input examples/runtime-input.json --now 2026-07-16T12:00:00Z
```

The demo prints the complete `Observe → Verify → Decide → Act → Learn` cycle. It proposes a synthetic brief, waits for approval, and reconciles canonical completion state without sending anything. Pass `--approved` to see the non-production destination authorization path.

## The useful part of the loop

The public layer captures the behavior that makes an assistant feel proactive while keeping integrations replaceable:

- Observe and verify: fresh, enabled, non-cancelled inputs are bounded before any decision callback sees them.
- Decide: inject a model or rules callback through `run_cycle(..., decide=...)`; the callback receives only the verified snapshot.
- Route: deterministic work stays on the `local` lane; synthesis and proposals are marked for the `judgment` lane. Provider names remain private deployment choices.
- Act: proposals are bounded and held behind explicit approval. The package authorizes a destination but never executes an external action.
- Learn: canonical milestones reconcile generated completion state, and `outcome` reports counts without copying source content.
- Fan out: `run_parallel` runs named background tasks with a small worker cap and records only safe success/error classes.

This is the shareable core behind daily briefs, proposal scouts, evidence-only coaching, safe browser/action adapters, and parallel background jobs. The connectors, prompts, model credentials, household policy, and real action adapters stay outside this repository.

## Design principles

- Prefer deterministic projections and reconciliation for state changes.
- Give model-driven jobs bounded, already-prepared context.
- Separate canonical state from generated views.
- Make delivery targets explicit and non-production by default.
- Treat privacy and secret scanning as release gates.

## Contributing

Only add generic documentation, code, or synthetic examples. Do not add real account identifiers, personal records, copied message content, credentials, local paths, or production routing. See [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`SECURITY.md`](SECURITY.md).

## License

Released under the [MIT License](LICENSE).
