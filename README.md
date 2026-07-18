# Hermes Runtime Patterns

A sanitized, shareable reference for building a local [Hermes Agent](https://github.com/NousResearch/hermes-agent) runtime.

This is an independent companion project, not an official Hermes distribution. It documents a small set of reusable runtime patterns without publishing a live assistant configuration.

## Hermes plus a product layer

[Hermes Agent](https://github.com/NousResearch/hermes-agent) is an open-source,
model-flexible agent runtime from Nous Research. It provides the conversation
loop, model/provider routing, tool use, terminal interface, gateway, and
messaging surfaces.

This project is the layer built on top of that runtime to turn a capable agent
into a persistent local-first chief of staff. It adds the operating model,
prompts, persona, source projections, state contracts, scheduled loops, and
approval boundaries that make the system behave like a product rather than a
collection of ad-hoc chats.

| Regular Hermes provides | This runtime layer adds |
| --- | --- |
| Model and tool orchestration | Observe → Verify → Decide → Act → Learn loops |
| Interactive and gateway conversations | 16 scheduled, inspectable cron contracts and prompts |
| Flexible provider integrations | Deterministic projections, freshness metadata, and private adapters |
| The ability to take actions | Approval-gated, auditable delivery and action boundaries |
| Conversation context | Canonical milestones, reconciliation, and quiet/no-op behavior |
| A general agent identity | `SOUL.md`, `.hermes.md`, and reusable product skills |

## Why this is useful

The product value is a reduction in coordination tax. Instead of asking an
agent to rediscover context every time, the runtime continuously prepares the
right evidence, notices meaningful changes, proposes bounded next steps, and
closes the loop when an approved action is complete. It stays quiet when there
is nothing useful to say, keeps private-owner information out of shared output,
and leaves provider credentials and side effects behind replaceable adapters.

That pattern is useful for a household chief of staff, a personal operating
system, or a small team's recurring operations. The public repository gives an
agent enough structure to reproduce the behavior without publishing the data,
identity, or integrations that make one deployment personal.

## Integrated systems

The private runtime is an orchestration layer over real sources and delivery
surfaces. The public repository documents the seams; it does not include the
accounts, credentials, or private adapter implementations.

| Integration | What it contributes |
| --- | --- |
| Google Workspace via `gog` | Gmail triage, shared Google Calendar, Drive, Docs, Sheets, and Contacts workflows |
| Google Health / Fitbit | Readiness, sleep/activity, nutrition, hydration, and other optional wellness evidence |
| Oura Ring | Private wearable sleep, readiness, recovery, and health projections |
| KeyLifts | Training history and strength/readiness context |
| Huckleberry | Private infant sleep, feeding, diaper, and growth context |
| BroadLink | Read-only local room temperature and humidity history |
| Hermes gateway channels | Chat delivery through configured Photon, Telegram, Discord, Slack, WhatsApp, Signal, or other Hermes connectors |
| Local dashboard and optional ngrok | Human-facing projections, completion views, and remote access to a deliberately exposed dashboard |
| Local vault projection | Optional Obsidian-style, local-first views of canonical household domains |
| Web search and browser/action adapters | Current authoritative research and explicitly approved authenticated workflows |
| Hermes memory and sidecars | Built-in memory by default; Honcho is optional, while the LightRAG experiment remains parked and disabled |

Some of these are active in the reference personal runtime and some are
optional adapters. A deployment should enable only the sources it can authorize,
validate, and keep within its privacy policy.

## What is included

- `runtime/` — a dependency-free reference implementation of bounded context building, a five-stage closed loop, deterministic state reconciliation, routing boundaries, bounded background fan-out, outcome summaries, and explicit delivery authorization.
- `cron/jobs.json` — the full sanitized schedule shape: 16 generic job contracts, disabled by default, with no production destinations. Every job points to an inspectable prompt and skill contract.
- `SOUL.md` and `.hermes.md` — deployment-neutral persona and orchestration guidance that preserve the privacy, routing, state, and quiet-output boundaries.
- `prompts/cron/` — one sanitized prompt contract per cron, including the bounded judgment and deterministic no-op rules.
- `scripts/` — safe public entrypoints for projection, cycle execution, state-audit preview, and surface validation.
- `skills/` — generic contracts for briefing, proposal, question, reconciliation, evidence, health, source projection, staged triage, document routing, reminders, architecture, and action gates.
- `tests/` — standard-library tests for the public runtime layer.
- `docs/architecture.md` and `docs/runtime-mirror.md` — the runtime boundary and private-mirror workflow.
- `examples/runtime-surface.json` — an inventory of private Python surfaces and their safe public equivalents.
- `examples/` — provider, job, source, skill, and runtime-input placeholders.

## Privacy boundary

This repository contains only generic runtime code, documentation, and synthetic examples. It does not contain:

- credentials, tokens, auth state, databases, logs, or session history;
- real messages, email/calendar identifiers, health records, financial records, or household data;
- names, addresses, phone numbers, production destinations, or local machine paths;
- a copy of a live runtime or upstream source checkout.

Every identifier in `examples/` is synthetic. Keep real runtime configuration in a private repository and inject secrets through the environment or a local secret manager.

## Install the runtime layer

This repository is an overlay and reference implementation, not a fork of
Hermes and not a separately packaged replacement. Install the upstream runtime
first, then keep this layer in a separate private runtime repository.

### 1. Install upstream Hermes

Use the official installer for your platform, then run its setup and health
checks:

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
source ~/.zshrc  # or source ~/.bashrc
hermes doctor
hermes setup
```

See the [upstream installation documentation](https://github.com/NousResearch/hermes-agent#quick-install)
for Windows, Termux, source-checkout, and provider-specific paths. Keep the
upstream checkout independently versioned. Do not copy this repository into
the upstream `hermes-agent/` source directory.

### 2. Install this public layer

Clone it beside the Hermes home and run the reference checks:

```bash
git clone https://github.com/patppham/hermes-agent-public.git "$HOME/.hermes-runtime-template"
cd "$HOME/.hermes-runtime-template"
python3 -m unittest discover -s tests -v
python3 scripts/validate_public_surface.py
```

### 3. Create a private runtime overlay

Copy the templates into a separate private repository, replace placeholders
with your own adapters and policy, then sync the reviewed persona and runtime
guidance into the Hermes home that your deployment loads:

```bash
PRIVATE_RUNTIME="$HOME/.hermes-runtime-private"
mkdir -p "$PRIVATE_RUNTIME"
cp -R SOUL.md .hermes.md cron prompts skills "$PRIVATE_RUNTIME"/

# After reviewing the private copies, use the paths expected by your Hermes home.
cp "$PRIVATE_RUNTIME/SOUL.md" "$HOME/.hermes/SOUL.md"
cp "$PRIVATE_RUNTIME/.hermes.md" "$HOME/.hermes.md"
```

Then implement the private source, state, delivery, and action adapters. Keep
real schedules, recipients, credentials, generated projections, logs, and
records in the private overlay. The public cron manifest is disabled by
default and uses synthetic destinations until those adapters are deliberately
configured.

### 4. Authenticate your own integrations

Every operator must create and authorize their own accounts. There is no shared
demo account, bundled OAuth token, API key, cookie, or provider session in this
repository. Before enabling a job, configure the credentials and scopes for the
systems that job uses:

- authenticate the Hermes model/provider and gateway channel you choose;
- complete `gog`'s own Google OAuth setup for the Workspace accounts and
  calendars you intend to expose;
- configure separate Oura, Huckleberry, Fitbit/Google Health, and KeyLifts
  access where applicable;
- grant only local-network read access to BroadLink sensors unless an explicit
  approved control adapter is intentionally added; and
- configure optional ngrok, browser, memory-sidecar, or other service tokens
  privately, if you use those adapters.

Keep OAuth files, client secrets, API keys, session cookies, local databases,
and provider exports outside Git. The public templates cannot work with live
data until your private adapter layer supplies authenticated, bounded records.

## How to use the patterns

1. Install and configure the upstream Hermes Agent project.
2. Copy the example shapes into a private runtime repository.
3. Replace placeholders with local values without committing them.
4. Keep generated projections, logs, sessions, and account routing private.

Run the sanitized reference runtime locally:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_public_surface.py
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

## Mirror the full runtime shape

The private runtime has more integration-specific Python than belongs in a
public repository. The public mirror keeps the same responsibilities, prompt
shape, persona boundaries, skill contracts, and schedule shape while replacing
household implementations with adapter seams. The audited surface inventory
covers 76 private Python paths, 16 cron jobs, and 55 skill/reference files
without copying their private contents.
Start with [`docs/runtime-mirror.md`](docs/runtime-mirror.md), then use
[`SOUL.md`](SOUL.md), [`.hermes.md`](.hermes.md), [`prompts/README.md`](prompts/README.md),
[`cron/jobs.json`](cron/jobs.json), the surface inventory, and the skill
contracts to build the private pieces locally.

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
