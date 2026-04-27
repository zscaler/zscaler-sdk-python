# Upgrade Guide: Zscaler Python SDK v1.x → v2.x (Beta)

> **Status:** v2.x is currently in **public preview / beta**. APIs, models, and import paths may change before the General Availability (GA) release. **Do not use v2.x for production workloads yet.**

The Zscaler Python SDK v2.x is a complete redesign of the SDK toolchain. It is **data-driven** — every model, request, and response is generated from the official Zscaler OpenAPI specifications — which means the SDK now stays in lock-step with the public API contract and ships new endpoints as soon as they are published.

For full hands-on documentation, code samples, and the v2.x API reference, visit the **[Zscaler Automation Hub – Python SDK](https://automate.zscaler.com/docs/tools/sdk-documentation/sdk-getting-started)**.

---

## Table of Contents

- [Before You Begin](#before-you-begin)
- [What's New in v2.x](#whats-new-in-v2x)
- [Authentication: OneAPI Only](#authentication-oneapi-only)
- [Product Coverage in the v2.x Beta](#product-coverage-in-the-v2x-beta)
- [Breaking Changes Overview](#breaking-changes-overview)
- [Migration Path](#migration-path)
  - [Step 1 — Decide if You Should Migrate Now](#step-1--decide-if-you-should-migrate-now)
  - [Step 2 — Install the v2.x Beta](#step-2--install-the-v2x-beta)
  - [Step 3 — Switch to OneAPI Authentication](#step-3--switch-to-oneapi-authentication)
  - [Step 4 — Update Imports and Client Construction](#step-4--update-imports-and-client-construction)
  - [Step 5 — Update Method Calls and Models](#step-5--update-method-calls-and-models)
  - [Step 6 — Update Error Handling](#step-6--update-error-handling)
  - [Step 7 — Test Thoroughly](#step-7--test-thoroughly)
- [Running v1.x and v2.x Side by Side](#running-v1x-and-v2x-side-by-side)
- [Where to Get Help](#where-to-get-help)

---

## Before You Begin

Read this section in full before changing your `requirements.txt` or `pyproject.toml`.

| Topic                    | v1.x (current GA)                                          | v2.x (beta)                                                       |
|--------------------------|-------------------------------------------------------------|--------------------------------------------------------------------|
| Status                   | Generally Available, fully supported                       | **Public Preview / Beta**                                         |
| Authentication           | OneAPI **and** legacy per-product API keys                 | **OneAPI only** — legacy authentication is **not supported**      |
| Codebase                 | Hand-written models and resource clients                   | **Data-driven** — generated from official OpenAPI specs           |
| Product coverage         | All Zscaler products (ZIA, ZPA, ZDX, ZCC, ZIdentity, ZTW, ZTB, ZWA, …) | **Limited subset** — see [Product Coverage](#product-coverage-in-the-v2x-beta) |
| Breaking changes         | Stable                                                     | **Yes** — import paths, method signatures, and models all change |
| Recommended for production | ✅ Yes                                                     | ❌ Not yet                                                        |

> ⚠️ **Important:** Migrating existing v1.x code to v2.x will introduce breaking changes. Plan to migrate in a non-production branch, run the full integration test suite, and stay on v1.x in production until v2.x reaches GA.

---

## What's New in v2.x

- **Data-driven SDK.** All API operations, request bodies, and response models are generated from the official Zscaler OpenAPI 3.0 specifications. New endpoints reach the SDK as soon as they are published, with no hand-edits required.
- **Strongly-typed models.** Request and response objects are Python classes with explicit fields and types, giving you better IDE autocompletion, in-editor type checking, and runtime validation.
- **Always-current docs.** Every API class, method, and model is documented from the same spec the SDK is generated from, so the reference and the code can never drift apart.
- **Smaller, faster install.** v2.x drops legacy authentication adapters and the older hand-written client tree, reducing dependencies.
- **OneAPI-native.** A single OAuth2 client serves every supported product. No more per-product credentials.

---

## Authentication: OneAPI Only

> 🔒 **v2.x supports OneAPI authentication exclusively.** Legacy per-product authentication (ZPA `client_id`/`client_secret` keypairs, ZIA `username`/`password`/`api_key`, ZCC `api_key`/`secret_key`, ZDX `key_id`/`key_secret`, etc.) **is not available** in v2.x and will not be added.

If your tenant has not yet been migrated to the **[Zscaler Identity (Zidentity) platform](https://help.zscaler.com/zidentity/what-zidentity)**, you must:

1. Stay on the v1.x SDK, **or**
2. Migrate your tenant to Zidentity and provision OneAPI clients **before** adopting v2.x.

For Zidentity onboarding, OAuth2 client creation, and scope assignment, see the [OneAPI Getting Started guide](https://automate.zscaler.com/docs/getting-started/getting-started).

---

## Product Coverage in the v2.x Beta

The v2.x beta currently supports a **subset** of Zscaler products. Coverage will grow with each beta release until parity with v1.x is reached at GA.

| Product                                 | v1.x (GA) | v2.x (Beta) |
|-----------------------------------------|-----------|-------------|
| **ZIA — Zscaler Internet Access**       | ✅        | ✅          |
| **ZDX — Zscaler Digital Experience**    | ✅        | ✅          |
| **ZIdentity (zid)**                     | ✅        | ✅          |
| ZPA — Zscaler Private Access            | ✅        | 🚧 Planned  |
| ZCC — Zscaler Client Connector          | ✅        | 🚧 Planned  |
| ZTW — Zscaler Cloud / Branch Connector  | ✅        | 🚧 Planned  |
| ZTB — Zero Trust Branch                 | ✅        | 🚧 Planned  |
| ZWA — Workflow Automation               | ✅        | 🚧 Planned  |

If you depend on a product that is not yet in the v2.x beta, **continue to use v1.x** — the two release lines will run in parallel until v2.x reaches feature parity.

---

## Breaking Changes Overview

The high-level shape of the breaking changes is the same in every product. Always consult the **[Automation Hub – Python SDK reference](https://automate.zscaler.com/docs/tools/sdk-documentation/sdk-getting-started)** for the exact, per-product call signatures.

1. **Authentication surface.** Legacy auth helpers (`LegacyZIAClient`, `LegacyZPAClient`, `LegacyZCCClient`, `LegacyZDXClient`, `LegacyZIdentityClient`, `LegacyZTWClient`, etc.) **do not exist** in v2.x. Construct a single `ZscalerClient` with OneAPI credentials.
2. **Import paths.** Resource and model imports have moved into a generated module layout (`zscaler.api.<product>.<resource>` for clients and `zscaler.models.<product>.<resource>` for models). v1.x paths such as `zscaler.zia.user_management` will not resolve in v2.x.
3. **Models.** Hand-written model classes (those inheriting from `ZscalerObject` with `request_format()` / `as_dict()`) are replaced by generated, strongly-typed classes. Field names follow the official spec; deserializers are stricter about types.
4. **Method signatures.** Method names are derived from the OpenAPI `operationId` (snake-cased). Request bodies are passed as typed model instances rather than `**kwargs` dicts.
5. **Return types.** The `(result, response, error)` tuple shape is preserved, but `result` is now a typed model (or list of typed models), not a `dict` or a `ZscalerObject`.
6. **Error handling.** A wider, more granular set of exception classes is exposed. Validation failures surface as dedicated exceptions before the request is even dispatched.
7. **Pagination.** Built-in pagination remains available, but the helper methods on response objects use the v2.x typed-response API surface.

---

## Migration Path

### Step 1 — Decide if You Should Migrate Now

Migrate to v2.x **only** if **all** of the following are true:

- Your Zscaler tenant is on **Zidentity** (Zidentity migration completed by your TAM / Customer Success team).
- The product(s) your code depends on are listed under [Product Coverage in the v2.x Beta](#product-coverage-in-the-v2x-beta).
- You are evaluating, prototyping, or building a new project — **not** running production workloads on this code.

If any of those is not true, **stay on v1.x**. v1.x will continue to receive bug fixes and security patches until v2.x reaches GA.

### Step 2 — Install the v2.x Beta

The v2.x line ships from the same PyPI project (`zscaler-sdk-python`) as a **pre-release** version (`2.0.0bN`). Pre-releases are not picked up by `pip` unless you opt in explicitly.

```bash
# Install the latest v2.x beta
pip install --pre --upgrade "zscaler-sdk-python>=2.0.0b1"
```

Or pin a specific beta in your `requirements.txt`:

```text
zscaler-sdk-python==2.0.0b1
```

Or in `pyproject.toml` (Poetry, with pre-release opt-in):

```toml
[tool.poetry.dependencies]
zscaler-sdk-python = { version = "^2.0.0b1", allow-prereleases = true }
```

> **Note:** The default `pip install zscaler-sdk-python` continues to install the latest v1.x GA release. Pre-releases must be requested explicitly with `--pre` or a pinned `2.0.0bN` version.

### Step 3 — Switch to OneAPI Authentication

If you are still authenticating with legacy per-product credentials in v1.x, you must replace those with a OneAPI client **before** running v2.x.

**v1.x — legacy ZIA example (no longer works in v2.x):**

```python
from zscaler.oneapi_client import LegacyZIAClient

config = {
    "username": "...",
    "password": "...",
    "api_key": "...",
    "cloud": "zscalertwo",
}
with LegacyZIAClient(config) as client:
    users, _, _ = client.user_management.list_users()
```

**v2.x — OneAPI (works for every supported product):**

```python
from zscaler import ZscalerClient

config = {
    "clientId": "...",
    "clientSecret": "...",        # or "privateKey": "..." for JWT auth
    "vanityDomain": "...",
    "cloud": "production",         # optional; defaults to production
}
client = ZscalerClient(config)
```

### Step 4 — Update Imports and Client Construction

The v1.x dotted-accessor pattern (`client.zia.<resource>`) is replaced in v2.x by **API classes** that are imported directly. Construct each API class with the shared `ZscalerClient` instance.

For the exact import path, class name, and constructor signature for the resource you use, refer to the **[Automation Hub Python SDK reference](https://automate.zscaler.com/docs/tools/sdk-documentation/sdk-getting-started)**.

### Step 5 — Update Method Calls and Models

- Rename callsites from v1.x snake_case kwargs to the generated **typed model** for each request body.
- Replace dict access on responses (e.g. `response["name"]`) with attribute access on the typed model (e.g. `response.name`).
- Replace `dict`-shaped list filters with the v2.x query-parameter model classes.

The Automation Hub reference includes a runnable example for every operation.

### Step 6 — Update Error Handling

v2.x raises a richer, more specific exception hierarchy. Replace broad `except Exception` blocks with the typed exceptions you actually want to handle (validation errors, authentication errors, API errors, transport errors). The exact class names are documented in the Automation Hub reference.

### Step 7 — Test Thoroughly

- Run your full integration suite against a non-production tenant.
- Watch for new validation errors — v2.x is stricter than v1.x about required fields and value types because the models come straight from the OpenAPI spec.
- Verify pagination, rate-limit handling, and retry behavior in long-running workflows.
- Re-run any cassettes or mocks; v2.x uses the OneAPI base URL exclusively, so legacy hostnames in fixtures will not match.

---

## Running v1.x and v2.x Side by Side

You **cannot** install both v1.x and v2.x of `zscaler-sdk-python` into the same Python environment — they share the `zscaler` top-level package name.

If you maintain projects that depend on both lines (e.g. a v1.x production codebase and a v2.x exploration), use one of:

- **Separate virtual environments** (`venv`, `virtualenv`, or `uv venv`) — one per project.
- **Separate Poetry / Hatch projects**, each pinning its own SDK version.
- **Containerised runs** (Docker, devcontainers) where each container installs only one SDK version.

---

## Where to Get Help

- **v2.x usage, code samples, and full API reference:** [Zscaler Automation Hub – Python SDK](https://automate.zscaler.com/docs/tools/sdk-documentation/sdk-getting-started)
- **OneAPI onboarding:** [Getting Started with Zscaler APIs](https://automate.zscaler.com/docs/getting-started/getting-started)
- **Zidentity onboarding:** [About Zidentity](https://help.zscaler.com/zidentity/what-zidentity)
- **Bug reports / feature requests:** [GitHub Issues](https://github.com/zscaler/zscaler-sdk-python/issues) — please prefix v2.x reports with `[v2-beta]`.
- **Community discussion:** [Zenith Community](https://community.zscaler.com/)
- **Customer support:** open a ticket via the [Zscaler Support Portal](https://help.zscaler.com/login-tickets).

If a v2.x bug blocks your evaluation, file an issue against this repository — the v2.x line is developed in the open alongside v1.x.
