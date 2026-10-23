# Using the casebook as a security-agent dataset
Each `case.json` is a structured, schema-validated record designed for retrieval and training:
- **Retrieval (RAG):** index `report.md` sections + `case.json`; an agent matches a user's symptoms (pasted command, odd extension, Run key) to known cases and returns the remediation list.
- **Classification / triage:** `kill_chain[].action` + `ttps` give labelled sequences (observation → ATT&CK technique).
- **Evidence grading:** every claim carries `PRESENT_IN_SAMPLE`, `OBSERVED_ON_HOST` or `HYPOTHESIS`, so an agent can learn to separate fact from inference and state uncertainty.
- **Detection synthesis:** `detections/` pairs case facts with rules (labelled TESTED/UNTESTED) for rule-generation tasks.
- **Remediation planning:** ordered `remediation` steps teach safe-first ordering (contain → preserve evidence → remove → rotate credentials).
Export idea: `jq -c . cases/*/case.json > dataset.jsonl`. Schema changes must stay backward compatible (add fields, don't rename).
