#!/usr/bin/env python3
"""Validate the public cron and runtime surface without reading private data."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SAFE_DESTINATIONS = {"local-only", "example:non-production"}


def _load(path: Path) -> dict:
    with path.open(encoding="utf-8") as source:
        value = json.load(source)
    if not isinstance(value, dict):
        raise ValueError(f"expected an object: {path}")
    return value


def main() -> int:
    cron = _load(ROOT / "cron/jobs.json")
    surface = _load(ROOT / "examples/runtime-surface.json")
    jobs = cron.get("jobs", [])
    if not isinstance(jobs, list) or not jobs:
        raise ValueError("cron/jobs.json must contain jobs")
    if cron.get("enabled_by_default") is not False:
        raise ValueError("public jobs must be disabled by default")
    if not surface.get("public_contracts"):
        raise ValueError("runtime surface must document public contracts")

    for key in ("persona", "runtime_guidance", "prompt_root"):
        value = cron.get(key)
        if not isinstance(value, str):
            raise ValueError(f"cron manifest is missing {key}")
        if key != "prompt_root" and not (ROOT / value).is_file():
            raise ValueError(f"missing manifest reference: {value}")

    for job in jobs:
        if job.get("enabled", False):
            raise ValueError(f"public job is enabled: {job.get('id', '<unknown>')}")
        script = job.get("script")
        if not isinstance(script, str) or not script.startswith("scripts/"):
            raise ValueError(f"job has no public script: {job.get('id', '<unknown>')}")
        if not (ROOT / script).is_file():
            raise ValueError(f"missing script reference: {script}")
        prompt = job.get("prompt")
        if not isinstance(prompt, str) or not prompt.startswith("prompts/cron/"):
            raise ValueError(f"job has no public prompt: {job.get('id', '<unknown>')}")
        if not (ROOT / prompt).is_file():
            raise ValueError(f"missing prompt reference: {prompt}")
        skills = job.get("skills")
        if not isinstance(skills, list) or not skills:
            raise ValueError(f"job has no public skills: {job.get('id', '<unknown>')}")
        for skill in skills:
            if not isinstance(skill, str) or not skill.startswith("skills/"):
                raise ValueError(f"unsafe skill reference: {skill}")
            if not (ROOT / skill).is_file():
                raise ValueError(f"missing skill reference: {skill}")
        destination = (job.get("delivery") or {}).get("destination")
        if destination not in SAFE_DESTINATIONS:
            raise ValueError(f"unsafe public destination: {destination}")

    tracked = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    forbidden = (
        "/" + "Users/",
        "/" + "home/",
        "-----BEGIN",
        "ghp_",
        "github_pat_",
    )
    email_pattern = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE)
    numeric_pattern = re.compile(r"(?:\+\d[\d ()-]{7,}\d|\b\d{8,}\b)")
    violations = []
    scan_paths = {ROOT / relative for relative in tracked}
    scan_paths.update(
        path
        for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts
    )
    for path in scan_paths:
        if not path.is_file():
            continue
        if path == Path(__file__).resolve():
            continue
        private_filename = path.name in {
            ".env",
            "auth.json",
            "google_client_secret.json",
            "state.db",
            "sessions.json",
        }
        if private_filename:
            violations.append(str(path.relative_to(ROOT)))
            continue
        if path.suffix not in {".md", ".json", ".yaml", ".yml", ".py", ".sh"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        emails = email_pattern.findall(text)
        has_non_synthetic_email = any(
            not email.lower().endswith("@example.invalid") for email in emails
        )
        if (
            any(marker in text for marker in forbidden)
            or has_non_synthetic_email
            or numeric_pattern.search(text)
        ):
            violations.append(str(path.relative_to(ROOT)))
    if violations:
        raise ValueError(f"private path or credential marker found in: {', '.join(violations)}")

    print(f"public surface valid: {len(jobs)} disabled jobs, {len(tracked)} tracked files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
