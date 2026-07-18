# Approval-gated action adapter

Use this boundary for messaging, browser actions, claims, device control, or
other external side effects.

The decision layer may produce a structured proposal with target, payload,
reason, audience, and approval requirement. The adapter must validate scope,
deduplicate the action, require explicit approval, and record the result without
leaking secrets into logs or model context.

The public reference runtime stops at authorization. A private deployment owns
credentials, destination resolution, retries, idempotency keys, and any actual
side effect. No skill may bypass this boundary by calling a provider directly.
