# Public cron prompt contracts

The private runtime's prompts are part of its product surface. They are kept as
separate files here so every scheduled job has an inspectable contract instead
of hiding the behavior in a JSON blob.

These are sanitized templates, not a copy of a private prompt set. They retain
the reusable decisions that make the loops useful:

- verify prepared context before interpretation;
- preserve freshness and missing-source metadata;
- separate private and shared audiences;
- no-op when there is nothing material to say;
- bound proposals and questions;
- keep state mutation deterministic and idempotent;
- require approval before external action; and
- report observed facts separately from inference or hypothesis.

The cron manifest references one prompt for every job. A private mirror can
extend a template with local sources, names, schedules, and routing only in a
private file or generated configuration layer.
