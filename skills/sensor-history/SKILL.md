# Read-only sensor history

Use this skill for local sensor logging that may later support analysis.

Normalize readings into a private, append-only history with timestamp, unit,
sensor identifier, source quality, and gap metadata. Keep collection separate
from interpretation. Do not turn one reading into a trend or a safety claim.

This skill is read-only. It never issues actuator commands, changes device
configuration, exposes physical location, or sends a message. Device control,
if a private deployment needs it, belongs to a separate adapter with an
explicit approval gate and an allowlist.
