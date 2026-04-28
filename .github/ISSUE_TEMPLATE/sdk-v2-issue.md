---
name: SDK v2.x (Preview / Beta) Issue
about: Report an issue specific to the data-driven Zscaler Python SDK v2.x (currently in public preview / beta).
title: "[v2-ISSUE] "
labels: 'v2-beta'
assignees: ''

---

> ⚠️ **This template is for the Zscaler Python SDK v2.x preview/beta only.**
> If you are using the stable **v1.x** line (`pip install zscaler-sdk-python`),
> please use the [SDK Issue](./sdk-issue.md) template instead.
>
> v2.x is **OneAPI-only** — legacy authentication is **not** supported, and
> not every product is covered yet. Please confirm you are using OneAPI
> credentials (clientId / clientSecret + vanityDomain, or a bound API key)
> before opening this issue.
>
> 📦 PyPI (pre-release):
> https://pypi.org/project/zscaler-sdk-python/#history
>
> ```bash
> pip install --pre --upgrade "zscaler-sdk-python>=2.0.0b1"
> ```
>
> 📚 Getting started / docs (Zscaler Automation Hub):
> https://automate.zscaler.com/docs/tools/sdk-documentation/sdk-getting-started
>
> 🔁 v1.x → v2.x migration guide:
> https://github.com/zscaler/zscaler-sdk-python/blob/master/UPGRADE_GUIDE.md

**SDK Version**
Output of `pip show zscaler-sdk-python` (must be a `2.0.0bN` pre-release):

```
```

**Affected Product / Service**
Which Zscaler product and resource is affected? (e.g. ZIA / `pac_files`, ZPA / `application_segments`, ZDX / `devices`, ZIdentity / `users`, etc.)

**Description**
A clear and concise description of what the bug is.

**Reproduction**
A minimal, self-contained code sample demonstrating the bug. Please redact any
real client IDs, secrets, vanity domains, or customer IDs.

```python
from zscaler import ZscalerClient

config = {
    "clientId": "<redacted>",
    "clientSecret": "<redacted>",
    "vanityDomain": "<redacted>",
    # "customerId": "<redacted>",  # ZPA only
    "cloud": "PRODUCTION",
}

with ZscalerClient(config) as client:
    # ...
    pass
```

**Expected behavior**
A clear and concise description of what you expected to happen.

**Actual behavior**
What actually happened. Include the full exception/traceback or API response,
not just the message.

**Is it a regression from v1.x?**
Did the equivalent call work on the v1.x SDK? If so, which v1.x version?

**Debug Logs**
SDK debug logs are essential for triage. Enable them with one of:

- Environment variables:
  * `ZSCALER_SDK_LOG=true`
  * `ZSCALER_SDK_VERBOSE=true`
- Or in code:
  ```python
  import logging
  logging.basicConfig(level=logging.DEBUG)
  ```

Paste the relevant request/response lines here (redact tokens and PII):

```
```

**Environment**
 - OS: [e.g. macOS 14.5, Ubuntu 22.04, Windows 11]
 - Python version: [e.g. 3.11.8]
 - SDK version: [e.g. 2.0.0b3]
 - Auth mode: OneAPI (client credentials / API key)
 - Cloud: [e.g. PRODUCTION, zscalertwo, zscalerthree, gov]

**Additional context**
Anything else that helps reproduce or scope the issue (related Automation Hub
docs link, OpenAPI spec section, screenshots, etc.).
