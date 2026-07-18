---
id: future-reminder-a
lane: local
audience: private
---
# Parameterized future reminder A

This is a once-only reminder contract. Run only when the private configuration
provides an explicit timestamp, authorized recipient, and approved reminder
template. Verify that the reminder is not already handled and keep the action
idempotent.

The public template intentionally contains no date, name, message, or channel.
If a placeholder remains unresolved, return `NO_OUTPUT`. Do not guess missing
values or send external communication without approval.
