#!/usr/bin/env python3
"""Validate every cases/*/case.json against schema/case.schema.json. MIT licensed."""
import json, sys, pathlib
from jsonschema import Draft202012Validator
root = pathlib.Path(__file__).resolve().parent.parent
v = Draft202012Validator(json.loads((root / "schema/case.schema.json").read_text()))
bad, ids = 0, set()
for f in sorted(root.glob("cases/*/case.json")):
    d = json.loads(f.read_text())
    errs = list(v.iter_errors(d))
    for e in errs: print(f"{f}: {e.message}"); bad += 1
    if d.get("id") in ids: print(f"{f}: duplicate id"); bad += 1
    ids.add(d.get("id"))
    for p in d.get("detections", []):
        if not (f.parent / p).exists(): print(f"{f}: missing {p}"); bad += 1
    if not (f.parent / "report.md").exists(): print(f"{f}: missing report.md"); bad += 1
print(f"{len(ids)} case(s), {bad} error(s)"); sys.exit(1 if bad else 0)
