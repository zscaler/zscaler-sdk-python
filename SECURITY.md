# Security Policy

Zscaler takes the security of its software, services, and customers' data seriously. This document explains how to report a security vulnerability that affects the **Zscaler Python SDK** (`zscaler-sdk-python`) or any other Zscaler product or service.

## Supported Versions

Security fixes are applied to the actively supported release lines listed below. If you are running an unsupported version, please upgrade before reporting an issue — the fix may already be available.

| Version | Status                                       | Receives security fixes |
|---------|----------------------------------------------|--------------------------|
| 2.x     | Public Preview / Beta (OneAPI only)          | ✅ Yes                  |
| 1.x     | General Availability                         | ✅ Yes                  |
| 0.x     | Retired                                      | ❌ No — please upgrade  |

## Reporting a Vulnerability

> **Please do _not_ open a public GitHub issue, pull request, or discussion to report a security vulnerability.** Public reports give attackers a head start and put other Zscaler customers at risk before a fix can be released.

To report a vulnerability in this SDK or in any Zscaler product or service, use Zscaler's official **Vulnerability Disclosure Program**, which is run in partnership with [Bugcrowd](https://bugcrowd.com):

🔗 **<https://www.zscaler.com/security/vulnerability-disclosure-program#overview>**

The disclosure page describes:

- The full program scope (in-scope and out-of-scope vulnerability categories).
- Confidentiality requirements that apply to all submissions.
- The Bugcrowd submission form used to triage and track reports.
- How rewards are determined.

### What to Include in Your Report

To help our team triage and reproduce the issue quickly, please include as much of the following as you can:

- A clear description of the vulnerability and its potential impact.
- The affected SDK version(s) (`pip show zscaler-sdk-python`).
- The Python version and operating system you used to reproduce the issue.
- A minimal, self-contained proof of concept (script, request/response capture, or stack trace).
- Any relevant configuration (with secrets redacted) — e.g. `cloud`, `vanityDomain`, OneAPI scopes, or legacy auth mode.
- Suggested mitigation or patch, if you have one.

### Handling Sensitive Data

When sharing logs, traces, or HAR files, **redact secrets** before sending them — including (but not limited to) `clientSecret`, `privateKey`, `api_key`, OAuth bearer tokens, customer IDs, microtenant IDs, and any personally identifiable information.

If a credential has been exposed publicly (for example, in a commit, container image, or paste site), please also rotate the credential through the Zscaler Identity (Zidentity) Admin UI — or the appropriate legacy admin console — as soon as possible.

### What to Expect

After you submit a report through the [Zscaler Vulnerability Disclosure Program](https://www.zscaler.com/security/vulnerability-disclosure-program#overview):

1. Bugcrowd will acknowledge receipt and assign a researcher to triage your submission.
2. The Zscaler security team will validate the issue and assess its severity (typically using CVSS).
3. We will work with you on remediation timelines and, where applicable, coordinate disclosure.
4. Once a fix has shipped to all supported release lines, the issue may be referenced in the SDK [release notes](docsrc/zs/guides/release_notes.rst) and [CHANGELOG.md](CHANGELOG.md).

We ask that you keep all details of any reported vulnerability confidential until Zscaler has had a reasonable opportunity to investigate, remediate, and release a fix, in line with the [confidentiality terms](https://www.zscaler.com/security/vulnerability-disclosure-program#overview) of the disclosure program.

## Non-Security Issues

Bugs, feature requests, and general questions about the SDK that **do not** involve a security vulnerability should be filed through the standard channels:

- 🐛 [GitHub Issues](https://github.com/zscaler/zscaler-sdk-python/issues) — for code defects and enhancement requests.
- 💬 [Zenith Community](https://community.zscaler.com/) — for usage questions and discussion.
- 🛟 [Zscaler Support Portal](https://help.zscaler.com/login-tickets) — for tenant-specific or production support.

Thank you for helping keep Zscaler customers and the broader community safe.
