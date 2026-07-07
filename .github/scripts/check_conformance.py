#!/usr/bin/env python3
"""Conformance checks for the shared-workflows repository.

Ensures the README workflow table and the workflow files stay in sync,
and that every reusable workflow is workflow_call-only with documented
inputs.
"""
import pathlib
import re
import sys

import yaml

root = pathlib.Path(__file__).resolve().parents[2]
workflows = root / ".github" / "workflows"
readme = (root / "README.md").read_text(encoding="utf-8")

errors = []
reusables = sorted(p.name for p in workflows.glob("reusable-*.yml"))

# 1) Every reusable workflow is listed in the README table, and vice versa.
documented = set(re.findall(r"\|\s*`(reusable-[a-z0-9-]+\.yml)`\s*\|", readme))
for name in reusables:
    if name not in documented:
        errors.append(f"{name}: missing from the README workflow table")
for name in sorted(documented):
    if not (workflows / name).exists():
        errors.append(f"README table lists non-existent workflow {name}")

# 2) Reusables are workflow_call-only and every input has a description.
for name in reusables:
    data = yaml.safe_load((workflows / name).read_text(encoding="utf-8"))
    # YAML 1.1 parses the bare `on` key as boolean True
    triggers = data.get("on", data.get(True))
    # Normalize the scalar and list forms (on: workflow_call / on: [...])
    if isinstance(triggers, str):
        triggers = {triggers: None}
    elif isinstance(triggers, list):
        triggers = {t: None for t in triggers}
    if not isinstance(triggers, dict) or set(triggers) != {"workflow_call"}:
        errors.append(f"{name}: must be triggered exclusively via workflow_call")
        continue
    call = triggers["workflow_call"] or {}
    for input_name, spec in (call.get("inputs") or {}).items():
        if not (spec or {}).get("description"):
            errors.append(f"{name}: input '{input_name}' has no description")

if errors:
    print("Conformance check failed:")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)

print(f"Conformance OK: {len(reusables)} reusable workflows checked")
