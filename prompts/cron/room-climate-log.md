---
id: room-climate-log
lane: local
audience: local
---
# Local sensor history

Read the approved local sensor adapter and append a normalized timestamped
reading to private history. Preserve gaps, units, sensor identity, and source
quality. Keep this job read-only so the history can support later analysis.

Do not issue device commands, infer comfort or safety from one reading, expose
the location outside the private runtime, or send a message. Return a local
status only.
