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
