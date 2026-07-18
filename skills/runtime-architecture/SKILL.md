# Runtime architecture

Use this skill when mirroring a personal Hermes runtime around an upstream
source checkout.

## Layers

- Upstream source remains independently versioned and replaceable.
- Private runtime owns persona, prompts, adapters, credentials, state, and
  deployment configuration.
- Public contracts expose reusable behavior without copying private data.

Keep generated projections, logs, sessions, caches, auth files, databases,
vendored dependencies, and local indexes out of the public repository. Inject
provider names, paths, destinations, schedules, and secrets through private
configuration. Do not merge unrelated upstream history into a runtime mirror.

When a contract changes, update its prompt, skill, context builder, state
adapter, and targeted verification together.
