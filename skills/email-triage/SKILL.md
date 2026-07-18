# Staged email triage

Use this contract when a private adapter classifies inbox metadata before an
agent sees selected content.

## Pipeline

1. Fetch only registered accounts and preserve account scope.
2. Classify bounded chunks using subject, sender, and stable identifiers.
3. Fetch a short body excerpt only for messages promoted by the classifier.
4. Enrich promoted messages with a summary, thread status, and reply state.
5. Pass only the fields required by the consuming loop.

## Rules

- Never send full bodies through bulk classification.
- Preserve `missing`, `stale`, `promoted`, and `thread_status` metadata.
- Treat an empty account result as a diagnostic condition until verified.
- Deduplicate by stable thread/message identity.
- Keep account ownership and audience scope attached to every record.
- Do not mutate mail, send a reply, or mark a thread complete from triage.

The public runtime supplies synthetic records only. Credentials, account names,
raw messages, and provider-specific adapters belong in the private mirror.
