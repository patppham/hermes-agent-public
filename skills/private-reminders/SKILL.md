# Private reminders

Use this skill for annual and once-only scheduled reminders whose values are
injected by private configuration.

Require an explicit timestamp, authorized recipient, message template, and
deduplication key. Verify that the reminder is current and has not already been
handled. Treat unresolved placeholders as configuration errors, not as a reason
to guess. Keep the result private and place delivery behind explicit approval.

The public repository contains only the contract. Names, dates, channels,
message text, and personal schedules belong in a private layer.
