# Example bounded skill

## Purpose

Turn a prepared context object into one concise update without making external changes.

## Inputs

- `context`: already-filtered evidence with timestamps and provenance;
- `audience`: an explicit non-production or approved recipient class;
- `max_items`: the maximum number of observations to return.

## Contract

1. Use only the supplied context.
2. Preserve missing or stale-source markers.
3. Do not infer private identifiers or fill gaps with guesses.
4. Do not create tasks, send messages, or mutate state.
5. Return at most `max_items` observations and one uncertainty note when needed.

## Output

Return a short Markdown update with:

- the observations;
- the evidence window;
- the next safe follow-up, if one is explicitly requested.
