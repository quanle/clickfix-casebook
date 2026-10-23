# ClickFix Casebook

An open, research-style collection of **real-world ClickFix / fake-CAPTCHA intrusion case studies**, written to warn people and to serve as a structured, machine-readable dataset for a future security-learning agent.

> **Status:** community project. Detections are **untested samples** unless stated otherwise.

## What is ClickFix?
A web page shows a fake "verify you are human" / "fix this error" box and tells you to press `Win+R` (or open PowerShell/Terminal), paste a command it silently copied to your clipboard, and press Enter. That command downloads and runs malware **as you**, bypassing most browser protections.

## How to stay safe
1. **Never paste a command from a web page into Run, cmd, PowerShell or Terminal.** No real CAPTCHA asks for this.
2. Be suspicious of "free tools" (video downloaders, cracks, "hack in 5 minutes" videos) – they are common lures.
3. Review your browser extensions (`chrome://extensions`); remove anything you did not install from the official store, especially in *Developer mode*.
4. Always re-check a crypto address after pasting it.
5. If you ran such a command: disconnect from the network, then follow the remediation section of a matching case.

## Cases
| ID | Title | Date |
|---|---|---|
| [CFC-2026-0001](cases/2026-10-clickfix-msi-clipper-extension/report.md) | ClickFix → silent MSI → crypto clipper + fake "Save to Google Drive" extension | 2026-10 |

## Repository layout
```
cases/<yyyy-mm-slug>/report.md      human-readable research report
cases/<yyyy-mm-slug>/case.json      machine-readable record (schema/case.schema.json)
cases/<yyyy-mm-slug>/iocs.csv       indicators (defanged)
cases/<yyyy-mm-slug>/detections/    Sigma / YARA (labelled tested/untested)
schema/                             JSON Schema for case.json
templates/                          case template
tools/                              validation + privacy lint (MIT)
docs/agent-dataset.md               how cases feed a security agent
```

## Contribute a case
Read [CONTRIBUTING.md](CONTRIBUTING.md). Open a **New case** issue or a pull request. CI validates `case.json` and runs a privacy/secret lint. **No live malware, no personal data.**

## License
Content (reports, case data): **CC BY 4.0**. Tooling (`tools/`, workflows): **MIT**. See `LICENSES/`.

---

## Tóm tắt tiếng Việt
Đây là kho tổng hợp các **case study thật về kiểu tấn công ClickFix** (hộp "xác minh bạn không phải robot" giả, bảo bạn dán lệnh vào Win+R/PowerShell). Mục tiêu: cảnh báo cộng đồng, và xây bộ dữ liệu có cấu trúc để huấn luyện/cung cấp tri thức cho một **agent bảo mật** sau này.

**Cách tự bảo vệ:**
1. **Không bao giờ dán lệnh từ trang web vào Win+R, cmd hay PowerShell.** CAPTCHA thật không bao giờ yêu cầu điều đó.
2. Cảnh giác với "tool miễn phí" (tải video, crack, video "hack trong 5 phút").
3. Kiểm tra `chrome://extensions`, gỡ extension lạ không cài từ Chrome Web Store.
4. Luôn soát lại địa chỉ ví crypto sau khi dán.
5. Nếu đã lỡ chạy lệnh: ngắt mạng, làm theo phần khắc phục trong case tương ứng.

**Đóng góp:** xem `CONTRIBUTING.md`, mở issue "New case" hoặc pull request. Tuyệt đối không đưa mẫu mã độc hay thông tin cá nhân.
