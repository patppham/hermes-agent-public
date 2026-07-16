# Hermes Runtime Patterns

A sanitized, shareable reference for building a local [Hermes Agent](https://github.com/NousResearch/hermes-agent) runtime.

This is an independent companion project, not an official Hermes distribution. It documents a small set of reusable runtime patterns without publishing a live assistant configuration.

## What is included

- `runtime/` — a dependency-free reference implementation of bounded context building, deterministic state reconciliation, and explicit delivery authorization.
- `tests/` — standard-library tests for the public runtime layer.
- `docs/architecture.md` — the runtime boundary and data flow.
- `examples/` — provider, job, source, skill, and runtime-input placeholders.

## Privacy boundary

This repository is intentionally documentation- and example-only. It does not contain:

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
python3 -m runtime --input examples/runtime-input.json
```

The runtime package is intentionally an extraction of safe patterns, not a drop-in replacement for a complete household deployment.

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
