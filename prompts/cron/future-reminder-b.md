---
id: future-reminder-b
lane: local
audience: private
---
# Parameterized future reminder B

Use the same once-only safety contract as the private reminder adapter: require
an explicit configured timestamp, recipient, template, and approval state;
verify deduplication; and record a local audit result.

The public template contains no personal date, name, message, or destination.
Missing configuration means `NO_OUTPUT`, not a guessed schedule or a delivery
attempt.
