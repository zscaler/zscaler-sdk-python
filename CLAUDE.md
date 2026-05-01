# Zscaler Python SDK — AI Agent Guidance

This document provides context for AI agents working on the Zscaler Python SDK (`zscaler-sdk-python`).

## Rules & Skills

### Cursor Rules (`.cursor/rules/`)

- **zscaler-sdk-python.mdc** — Core standards: models from JSON, naming conventions, docstrings, documentation updates. Applies when editing `zscaler/**/*.py`.
- **troubleshoot-sdk.mdc** — Troubleshooting guide for model/API/client issues.
- **release-versioning.mdc** — How to update CHANGELOG, release_notes.rst, pyproject.toml, zscaler/__init__.py, docsrc/conf.py, and Makefile (for new packages).

### Claude Skills (`.claude/skills/`)

- **plan-sdk-service** — Plan and implement new services. Use when:
  - Creating models from a JSON payload
  - Adding new API clients or resources
  - Extending existing ZIA, ZPA, ZTW, ZTB, etc. resources

- **troubleshoot-sdk** — Diagnose and fix SDK issues. Use when:
  - Debugging AttributeError, KeyError, or API errors
  - Investigating wrong/missing data in responses
  - Syncing documentation (CHANGELOG, docsrc)

## Linter

After every code change, run `make format` then `make lint`. Fix all errors (extra spaces, trailing whitespace, import order). The linter must pass.

## Testing

- **Unit tests**: `tests/unit/` — mock HTTP with `unittest.mock`; no live API
- **Integration tests**: `tests/integration/<product>/` — VCR + `Mock*Client`; deterministic names; cleanup in `finally`
- See Phase 5 in `.claude/skills/plan-sdk-service/SKILL.md` for full templates

## API Client Patterns

- **Try/except**: Every function that parses response → model must wrap in try/except (see `segment_groups.py`)
- **ZPA POST search**: Some endpoints use POST `/resource/search` with filterBy/pageBy/sortBy; use `_post_search_all_pages` or `CommonFilterSearch`
- **JMESPath client-side filtering**: All list endpoints return a `ZscalerAPIResponse` that supports `resp.search(expression)` for client-side filtering/projection via [JMESPath](https://jmespath.org/). This is additive — `query_params` remain the primary mechanism for server-side filtering. See the Pagination section in `README.md` for examples.

## ZCC-Specific Architecture

The ZCC API is unusually inconsistent in its attribute casing — payloads mix `camelCase` (`disasterRecovery`), `lowerCamelCaseWithAcronyms` (`enforceSplitDNS`, `oneIdMTDeviceAuthEnabled`), and the occasional `snake_case` field. To insulate users (and the rest of the SDK) from those quirks, the **ZCC service has its own model-driven serializer**. This applies *only* to ZCC; do not change other products' serialization paths.

### Serializer flow

1. **`zscaler/zcc/_field_introspect.py`** — model introspection layer.
   - `field_map(cls)` traces a `ZscalerObject` subclass's `request_format()` with an `_AttrTracer` to derive a deterministic `snake_case_attr → wire_key` map (per-class, since two different classes can collide on the same snake_case key but use different wire casings).
   - `nested_types(cls)` AST-parses the class's `__init__` to discover which attributes are themselves `ZscalerObject` subclasses (or lists of them), so nested dictionaries are recursed into with the correct schema.
   - Both are LRU-cached; `reset_caches()` is exposed for tests.
2. **`zscaler/zcc/_serialize.py`** — `zcc_to_wire(body, schema_cls)`.
   - Recursively walks `body` (a `dict[str, Any]` keyed in `snake_case`) and, for every key, resolves the wire name by consulting (in order): the model-declared `field_map`, `WebPolicy.SNAKE_CASE_KEYS` for legacy preservation cases, then `to_lower_camel_case` (which honours `FIELD_EXCEPTIONS` from `zscaler/helpers.py`).
   - Returns a `_ZccWireBody(dict)` — a marker subclass of `dict` that carries the same payload but signals "already converted to wire format".
3. **`zscaler/request_executor.py`** — the ZCC branch of `_prepare_body()` checks `isinstance(body, _ZccWireBody)` and, if so, passes the dict through unchanged. This prevents the executor's legacy `convert_keys_to_camel_case_selective` pass from clobbering keys like `enforceSplitDNS` back into `enforceSplitDns`.
4. **`zscaler/zcc/web_policy.py`** — `web_policy_edit` calls `body = zcc_to_wire(body, WebPolicy)` immediately before sending. New ZCC mutating endpoints should follow the same pattern.

### Asymmetric ZCC contracts

- **`web_policy_edit` / `list_by_company` (groups & users)** — the *request* expects flat `groupIds: list[int]` and `userIds: list[str]`; the *response* returns nested `groups: [{id, name}]` and `users: [{id, name}]`. **Do not** call `transform_common_id_fields(reformat_params, ...)` on ZCC web-policy bodies (it would mangle the request shape). The asymmetry is documented in `web_policy_edit`'s docstring.
- **`/web/policy/edit` create response** — the API returns only `{"success": "true", "id": <new_id>}`; it does not echo the policy. Integration tests must (a) parse the raw `response.get_body()` to capture `id` *before* any further assertions so the `finally` cleanup is always reachable, and (b) self-heal on entry by deleting any leftover policy with the same name (the API silently rejects duplicate names with `success=false, id=0`).

### Dynamic cloud-to-subdomain mapping (`LegacyZCCClient`)

`zscaler/zcc/legacy.py` exposes a `_ZCC_CLOUD_SUBDOMAIN_OVERRIDES` map and a `_build_zcc_base_url(cloud)` helper. The default subdomain is `api-mobile`; `zscalerten` is mapped to `mobile6`. Both the base URL and the OAuth login URL are derived from the same helper, so users on non-default clouds do not need to pass an `override_url`. Add new tenant clouds to `_ZCC_CLOUD_SUBDOMAIN_OVERRIDES` rather than introducing more parameters.

### `device_type` parameter normalisation

`zscaler/utils.py` `zcc_param_mapper` accepts `device_type` as either a string label (`"ios"`, `"windows"`) or an int code (`3`). The scalar-to-list wrapper handles both `str` and `int`; do not pass `device_type` as a one-element list unless you really mean to fan-out across multiple device types.

## Key Conventions

| Aspect | Convention |
|--------|------------|
| Models from JSON | Always require JSON payload; map camelCase API keys → snake_case Python attributes |
| Product design | Follow existing resource in same product (ZIA, ZPA, ZTW, ZTB) |
| Docstrings | Args, Returns, Examples (with `>>>` code blocks) for every function; `list_` functions must mention `resp.search()` |
| Documentation | CHANGELOG, release_notes.rst, and `docsrc/zs/<product>/<module>.rst` (exact format in plan-sdk-service Phase 6) |
| Naming | Model: PascalCase; API client: PascalCase + `API`; functions: snake_case |

## Reference Examples

See `.claude/skills/plan-sdk-service/examples/`:

- `zia-service-example.md` — ZIA (int IDs, CommonBlocks)
- `zpa-service-example.md` — ZPA (str IDs, form_list)
- `ztw-service-example.md` — ZTW (int IDs)
- `ztb-service-example.md` — ZTB (str IDs, form_response_body)
