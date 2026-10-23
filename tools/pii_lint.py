#!/usr/bin/env python3
"""Flag likely personal data, internal IPs, secrets and undefanged URLs. MIT licensed."""
import re, sys, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
RULES = {
  "email": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}",
  "private_ip": r"\b(10\.\d{1,3}|192\.168|172\.(1[6-9]|2\d|3[01])|100\.(6[4-9]|[7-9]\d|1[01]\d|12[0-7]))\.\d{1,3}\.\d{1,3}\b",
  "windows_sid": r"S-1-5-21-\d+",
  "hostname": r"\bDESKTOP-[A-Z0-9]{5,}\b",
  "user_path": r"C:\\Users\\(?!<user>|Public)[A-Za-z0-9._-]+",
  "github_token": r"\bgh[pousr]_[A-Za-z0-9]{30,}",
  "aws_key": r"\bAKIA[0-9A-Z]{16}\b",
  "private_key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
  "live_url": r"\bhttps?://(?!(github\.com|www\.contributor-covenant\.org|json-schema\.org|attack\.mitre\.org)\b)[^\s)\"']+",
}
ALLOW_EMAIL = re.compile(r"@(example\.(com|org)|users\.noreply\.github\.com)$")
SKIP = {".git"}
hits = 0
for f in root.rglob("*"):
    if not f.is_file() or SKIP & set(f.parts) or f.suffix in {".png",".jpg"} or f.name == "pii_lint.py": continue
    for n, line in enumerate(f.read_text(errors="ignore").splitlines(), 1):
        for name, rx in RULES.items():
            for m in re.finditer(rx, line):
                if name == "email" and ALLOW_EMAIL.search(m.group()): continue
                print(f"{f.relative_to(root)}:{n}: {name}: {m.group()}"); hits += 1
print(f"{hits} finding(s)"); sys.exit(1 if hits else 0)
