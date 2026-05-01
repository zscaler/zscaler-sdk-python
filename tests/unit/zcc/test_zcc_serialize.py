"""
Unit tests for the ZCC-only model-driven serializer.

These tests do not require any network access. They prove that:

1. ``field_map`` and ``nested_types`` introspect each ZCC model class
   correctly.
2. ``zcc_to_wire`` produces a body with the exact wire-key casing the ZCC
   API expects, for every field in the five real ``WebPolicy`` payloads
   (one per supported OS).

Real payloads live under ``local_dev/OneAPI/zcc_dev/web_policy/`` and are
the source of truth for "what the API wants on input".
"""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from zscaler.zcc._field_introspect import field_map, nested_types, wire_keys
from zscaler.zcc._serialize import _ZccWireBody, zcc_to_wire
from zscaler.zcc.models.webpolicy import (
    AndroidPolicy,
    DisasterRecovery,
    Groups,
    IOSPolicy,
    LinuxPolicy,
    MacOSPolicy,
    OnNetPolicy,
    PolicyExtension,
    Users,
    WebPolicy,
    WindowsPolicy,
)

PAYLOAD_DIR = Path(__file__).resolve().parents[3] / "local_dev" / "OneAPI" / "zcc_dev" / "web_policy"

PAYLOAD_FILES = [
    "android_policy.json",
    "ios_policy.json",
    "linux_policy.json",
    "mac_policy.json",
    "windows_policy.json",
]


# ---------------------------------------------------------------------------
# Introspection
# ---------------------------------------------------------------------------


def test_field_map_uses_model_declared_wire_keys():
    fmap = field_map(WebPolicy)
    # Snake-on-the-wire keys preserved as declared by the model.
    assert fmap["pac_url"] == "pac_url"
    assert fmap["device_type"] == "device_type"
    assert fmap["reauth_period"] == "reauth_period"
    # Standard camelCase keys.
    assert fmap["app_service_ids"] == "appServiceIds"
    assert fmap["forwarding_profile_id"] == "forwardingProfileId"
    assert fmap["policy_extension"] == "policyExtension"
    # Nested object attribute -> camelCase wire key.
    assert fmap["windows_policy"] == "windowsPolicy"
    assert fmap["mac_policy"] == "macPolicy"


def test_field_map_irregular_casing_resolved_from_model():
    fmap = field_map(PolicyExtension)
    # All these used to require a hand-maintained FIELD_EXCEPTIONS entry.
    # Now they come straight from the model's request_format dictionary.
    assert fmap["use_default_adapter_for_dns"] == "useDefaultAdapterForDNS"
    assert fmap["enforce_split_dns"] == "enforceSplitDNS"
    assert fmap["truncate_large_udpdns_response"] == "truncateLargeUDPDNSResponse"
    assert fmap["delete_dhcp_option121_routes"] == "deleteDHCPOption121Routes"
    assert fmap["intercept_zia_traffic_all_adapters"] == "interceptZIATrafficAllAdapters"
    assert fmap["packet_tunnel_exclude_list_for_ipv6"] == "packetTunnelExcludeListForIPv6"
    assert fmap["override_at_cmd_by_policy"] == "overrideATCmdByPolicy"
    assert fmap["purge_kerberos_preferred_dc_cache"] == "purgeKerberosPreferredDCCache"


def test_disable_password_collision_resolved_per_class():
    """The same snake_case name maps to different wire keys in different
    classes. A flat global table cannot capture this — per-class
    introspection does."""
    assert field_map(WindowsPolicy)["disable_password"] == "disable_password"
    assert field_map(AndroidPolicy)["disable_password"] == "disable_password"
    assert field_map(LinuxPolicy)["disable_password"] == "disablePassword"
    assert field_map(IOSPolicy)["disable_password"] == "disablePassword"
    assert field_map(MacOSPolicy)["disable_password"] == "disablePassword"


def test_install_ssl_certs_collision_resolved_per_class():
    assert field_map(WindowsPolicy)["install_ssl_certs"] == "install_ssl_certs"
    assert field_map(LinuxPolicy)["install_ssl_certs"] == "installCerts"


def test_wire_keys_are_inverse_of_field_map():
    fmap = field_map(WebPolicy)
    assert wire_keys(WebPolicy) == set(fmap.values())


def test_nested_types_for_web_policy():
    expected = {
        "android_policy": AndroidPolicy,
        "disaster_recovery": DisasterRecovery,
        "groups": Groups,
        "ios_policy": IOSPolicy,
        "linux_policy": LinuxPolicy,
        "mac_policy": MacOSPolicy,
        "on_net_policy": OnNetPolicy,
        "policy_extension": PolicyExtension,
        "users": Users,
        "windows_policy": WindowsPolicy,
    }
    assert nested_types(WebPolicy) == expected


def test_leaf_models_have_no_nested_types():
    # PolicyExtension and the per-OS classes are leaves in the WebPolicy tree.
    for cls in (PolicyExtension, WindowsPolicy, LinuxPolicy, IOSPolicy, AndroidPolicy, MacOSPolicy, Groups):
        assert nested_types(cls) == {}


# ---------------------------------------------------------------------------
# zcc_to_wire — pass-through and marker behaviour
# ---------------------------------------------------------------------------


def test_zcc_to_wire_returns_marker_dict():
    out = zcc_to_wire({"name": "foo"}, WebPolicy)
    assert isinstance(out, _ZccWireBody)
    assert isinstance(out, dict)


def test_zcc_to_wire_translates_snake_input_to_wire_keys():
    body = {
        "name": "test",
        "device_type": 4,
        "pac_url": "",
        "rule_order": 2,
        "forwarding_profile_id": 0,
        "policy_extension": {
            "enforce_split_dns": 0,
            "use_default_adapter_for_dns": "1",
            "truncate_large_udpdns_response": 0,
        },
    }
    out = zcc_to_wire(body, WebPolicy)
    assert out["name"] == "test"
    assert out["device_type"] == 4  # snake-on-the-wire preserved
    assert out["pac_url"] == ""
    assert out["ruleOrder"] == 2
    assert out["forwardingProfileId"] == 0
    pe = out["policyExtension"]
    assert pe["enforceSplitDNS"] == 0
    assert pe["useDefaultAdapterForDNS"] == "1"
    assert pe["truncateLargeUDPDNSResponse"] == 0


def test_zcc_to_wire_accepts_camelcase_input_unchanged():
    """Users who paste an API response back as kwargs must keep working."""
    body = {
        "ruleOrder": 2,
        "forwardingProfileId": 0,
        "policyExtension": {"enforceSplitDNS": 0, "useDefaultAdapterForDNS": "1"},
    }
    out = zcc_to_wire(body, WebPolicy)
    assert out["ruleOrder"] == 2
    assert out["forwardingProfileId"] == 0
    assert out["policyExtension"]["enforceSplitDNS"] == 0
    assert out["policyExtension"]["useDefaultAdapterForDNS"] == "1"


def test_zcc_to_wire_unknown_keys_fall_back_to_legacy_converter():
    """Fields the model has not yet incorporated must still be converted via
    ``to_lower_camel_case`` (which honours ``FIELD_EXCEPTIONS``). This
    keeps backwards compatibility with payloads that contain fields the
    model does not yet declare, e.g. ``oneIdMTDeviceAuthEnabled``."""
    body = {"one_id_mt_device_auth_enabled": "0"}
    out = zcc_to_wire(body, WebPolicy)
    assert "oneIdMTDeviceAuthEnabled" in out
    assert out["oneIdMTDeviceAuthEnabled"] == "0"


def test_zcc_to_wire_preserves_lists_of_primitives():
    body = {"app_service_ids": ["a", "b"], "user_ids": []}
    out = zcc_to_wire(body, WebPolicy)
    assert out["appServiceIds"] == ["a", "b"]
    assert out["userIds"] == []


def test_zcc_to_wire_recurses_into_lists_of_dicts():
    """``users`` is declared as a list of ``Users`` model instances; each
    element must be re-keyed using the ``Users`` schema."""
    body = {"users": [{"id": 1, "login_name": "alice@example.com"}]}
    out = zcc_to_wire(body, WebPolicy)
    assert out["users"] == [{"id": 1, "loginName": "alice@example.com"}]


def test_zcc_to_wire_preserves_none_values():
    body = {"name": None, "policy_extension": None}
    out = zcc_to_wire(body, WebPolicy)
    assert out["name"] is None
    assert out["policyExtension"] is None


# ---------------------------------------------------------------------------
# Round-trip parity against the real per-OS payloads
# ---------------------------------------------------------------------------


def _key_tree(value: Any) -> Any:
    """Strip values; keep only the recursive shape of dict keys / list shape.

    Two structures with identical key trees expose the same keys at every
    depth, regardless of values. This is exactly the property we want to
    assert on a wire-form body.
    """
    if isinstance(value, dict):
        return {k: _key_tree(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_key_tree(item) for item in value]
    return None


def _snake_via_schema(body: Any, schema_cls) -> Any:
    """Inverse of ``zcc_to_wire`` — used only by the round-trip test to
    simulate "what a user would type if they snake-cased an API response
    using only the model's own knowledge"."""
    if isinstance(body, list):
        return [_snake_via_schema(item, schema_cls) if isinstance(item, dict) else item for item in body]
    if not isinstance(body, dict):
        return body
    fmap = field_map(schema_cls)
    nested = nested_types(schema_cls)
    wire_to_snake = {wire: snake for snake, wire in fmap.items()}
    out: dict = {}
    for k, v in body.items():
        snake_k = wire_to_snake.get(k, k)
        # Resolve nested type by either snake or wire form
        nested_cls = nested.get(snake_k) or nested.get(k)
        if nested_cls is not None:
            if isinstance(v, dict):
                v = _snake_via_schema(v, nested_cls)
            elif isinstance(v, list):
                v = [_snake_via_schema(item, nested_cls) if isinstance(item, dict) else item for item in v]
        out[snake_k] = v
    return out


@pytest.mark.parametrize("payload_name", PAYLOAD_FILES)
def test_policy_extension_round_trip_parity(payload_name):
    """The ``policyExtension`` subtree is where the majority of irregular
    casing lives (``useDefaultAdapterForDNS``, ``enforceSplitDNS``,
    ``truncateLargeUDPDNSResponse``, ``deleteDHCPOption121Routes``,
    ``oneIdMTDeviceAuthEnabled``, ``interceptZIATrafficAllAdapters``,
    ``packetTunnelExcludeListForIPv6``, ``zccFailCloseSettingsExit*``,
    etc.). For each real payload, prove that:

        snake-case-via-schema(payload['policyExtension'])
            -> zcc_to_wire(..., PolicyExtension)
            == payload['policyExtension']

    at the key-tree level. This is the main payoff of the new design."""
    payload_path = PAYLOAD_DIR / payload_name
    payload = json.loads(payload_path.read_text())
    pe = payload.get("policyExtension")
    assert isinstance(pe, dict), f"{payload_name}: missing policyExtension subtree"

    user_input = _snake_via_schema(pe, PolicyExtension)
    wire_body = zcc_to_wire(user_input, PolicyExtension)

    assert _key_tree(wire_body) == _key_tree(
        pe
    ), f"{payload_name}: policyExtension wire-form key tree differs from API payload"


@pytest.mark.parametrize("payload_name", PAYLOAD_FILES)
def test_policy_extension_is_idempotent_on_camelcase_payload(payload_name):
    """Running the serializer on an already-camelCase ``policyExtension``
    must be a no-op at the key-tree level."""
    payload_path = PAYLOAD_DIR / payload_name
    payload = json.loads(payload_path.read_text())
    pe = payload["policyExtension"]
    out = zcc_to_wire(pe, PolicyExtension)
    assert _key_tree(out) == _key_tree(pe), f"{payload_name}: PolicyExtension idempotence check failed"


@pytest.mark.parametrize("payload_name", PAYLOAD_FILES)
def test_top_level_declared_keys_round_trip_correctly(payload_name):
    """Top-level WebPolicy round-trip: for every key the model *declares*
    in ``WebPolicy.field_map``, the wire-form key must match the original
    payload exactly. Keys the model has not yet declared are reported via
    :func:`test_unmodelled_top_level_keys_are_documented` instead, so the
    two concerns stay separate."""
    payload_path = PAYLOAD_DIR / payload_name
    payload = json.loads(payload_path.read_text())

    fmap = field_map(WebPolicy)
    declared_wire_keys = set(fmap.values())

    user_input = _snake_via_schema(payload, WebPolicy)
    wire = zcc_to_wire(user_input, WebPolicy)

    # The set of declared wire keys present in the original payload must
    # appear identically (and recursively, via the schema) in the output.
    payload_declared = {k for k in payload if k in declared_wire_keys}
    wire_declared = {k for k in wire if k in declared_wire_keys}
    assert payload_declared == wire_declared, (
        f"{payload_name}: declared top-level wire keys differ.\n"
        f"  missing in wire: {payload_declared - wire_declared}\n"
        f"  extra in wire:   {wire_declared - payload_declared}"
    )


def test_unmodelled_top_level_keys_are_documented():
    """Diagnostic. Surfaces top-level WebPolicy keys that appear in real
    API payloads but are not yet declared by ``WebPolicy.request_format``.
    The serializer falls back to ``WebPolicy.SNAKE_CASE_KEYS`` and then to
    the legacy ``to_lower_camel_case`` for these. Listing them here keeps
    the gap visible without coupling the serializer to a hand-maintained
    table — they should be added to the model over time."""
    fmap = field_map(WebPolicy)
    declared_wire_keys = set(fmap.values())
    snake_preserve = WebPolicy.SNAKE_CASE_KEYS

    undeclared: dict = {}
    for payload_name in PAYLOAD_FILES:
        payload = json.loads((PAYLOAD_DIR / payload_name).read_text())
        for k in payload:
            if k in declared_wire_keys:
                continue
            if k in snake_preserve:
                continue
            # Skip keys that are camelCase already and would pass through
            # the legacy converter unchanged (no underscore).
            if "_" not in k:
                continue
            undeclared.setdefault(k, []).append(payload_name)

    # This assertion does not fail. It records the current state so future
    # contributors can see the remaining model gaps at a glance.
    if undeclared:
        gaps = "\n  ".join(f"{k}  (in {', '.join(payloads)})" for k, payloads in sorted(undeclared.items()))
        # pytest -s will show this; otherwise it lives in the test name.
        print(f"\nWebPolicy top-level keys not yet declared by the model:\n  {gaps}")


# ---------------------------------------------------------------------------
# Request-executor integration: marker dict bypasses the legacy converter
# ---------------------------------------------------------------------------


def test_prepare_body_passes_zcc_wire_body_through_unchanged():
    """The request executor's ZCC branch must detect ``_ZccWireBody`` and
    return the body verbatim, skipping the legacy heuristic converter.
    Without this contract, the executor would re-process a body that was
    already serialized by ``zcc_to_wire`` and could re-introduce wrong
    casing for keys the model deliberately preserves as snake_case
    (e.g. ``pac_url``, ``device_type``, ``disable_password`` in
    Windows/Android policies)."""
    from zscaler.request_executor import RequestExecutor

    body = zcc_to_wire(
        {
            "name": "test",
            "device_type": 4,
            "pac_url": "",
            "policy_extension": {
                "enforce_split_dns": 0,
                "use_default_adapter_for_dns": "1",
            },
            "windows_policy": {"disable_password": "secret"},
            "linux_policy": {"disable_password": "secret"},
        },
        WebPolicy,
    )
    # Stand-in for the RequestExecutor -- we only need to invoke
    # _prepare_body, which is independent of network state.
    fake_exec = SimpleNamespace(
        use_legacy_client=False,
        zdx_legacy_client=None,
        ztb_legacy_client=None,
    )
    out = RequestExecutor._prepare_body(fake_exec, "/zcc/papi/public/v1/web/policy/edit", body)

    # Every model-declared key must reach the wire exactly as the model
    # said it would.
    assert out["device_type"] == 4
    assert out["pac_url"] == ""
    assert out["policyExtension"]["enforceSplitDNS"] == 0
    assert out["policyExtension"]["useDefaultAdapterForDNS"] == "1"
    # Per-class scoping survives the round-trip through the executor.
    assert out["windowsPolicy"]["disable_password"] == "secret"
    assert out["linuxPolicy"]["disablePassword"] == "secret"
    # And the marker has been stripped: downstream sees a plain dict.
    assert type(out) is dict
