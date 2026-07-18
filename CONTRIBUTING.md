# Contributing

Keep contributions generic and safe to publish.

- Use synthetic identifiers and example domains only.
- Never commit credentials, auth files, logs, sessions, databases, or copied messages.
- Do not add local machine paths, production destinations, or personal records.
- Prefer deterministic examples and small documentation changes.
- Keep `cron/jobs.json` as the canonical public schedule contract and run
  `python3 scripts/validate_public_surface.py` after changing it.
- Keep one inspectable prompt and relevant skill reference for every public
  cron. Add generic contracts or adapter seams for private runtime behavior;
  do not copy private Python scripts, prompt values, generated projections, or
  source records verbatim.
- Validate JSON examples with `python -m json.tool` before opening a pull request.

Please explain the privacy boundary of any new integration or fixture in the pull request description.
