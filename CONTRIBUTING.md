# Contributing a case

1. Copy `templates/case-template.md` to `cases/<yyyy-mm-short-slug>/report.md`; add `case.json` (must validate against `schema/case.schema.json`), `iocs.csv`, optional `detections/`.
2. Pick the next free id `CFC-YYYY-NNNN`.
3. Run `pip install jsonschema && python tools/validate.py` locally.
4. Open a PR using the template.

## Privacy / redaction checklist (mandatory)
- [ ] No real names, emails, phone numbers, usernames, hostnames, SIDs, serials.
- [ ] No internal IPs (10/8, 172.16/12, 192.168/16, 100.64/10) or internal domains.
- [ ] Paths generalised (`%LOCALAPPDATA%`, `C:\Users\<user>`).
- [ ] No list of the victim's accounts, employers, products, or infrastructure.
- [ ] No passwords, tokens, cookies, API keys, seed phrases.
- [ ] Screenshots cropped/blurred.

## Safety rules
- **No live malware**, archives of samples, or full deobfuscated malicious code. Hashes and short snippets only.
- Defang: `hxxp://`, `example[.]com`, `1.2.3[.]4`. Wallet addresses and hashes may be listed as-is.
- Label every claim: `PRESENT_IN_SAMPLE` (seen in code), `OBSERVED_ON_HOST` (seen in logs/forensics), `HYPOTHESIS`.
- Detection rules must say `TESTED` or `UNTESTED`.
