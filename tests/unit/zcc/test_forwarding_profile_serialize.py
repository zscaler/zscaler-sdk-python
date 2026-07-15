"""
Unit tests that prove the ZCC ForwardingProfile model is the single
source of truth for wire-key casing.

The committed ``payload.json`` fixture is the exact body the ZCC API
accepts (verified by Postman). These tests:

1. Convert that wire payload into a snake_case body (the shape callers
   actually pass to ``update_forwarding_profile``).
2. Run it back through ``zcc_to_wire(..., ForwardingProfile)``.
3. Assert the result is byte-for-byte identical to the original wire
   payload. Any future drift in the model immediately fails this test.

No ``FIELD_EXCEPTIONS`` are required for any forwarding-profile field;
all wire keys (including ``UDPTimeout``, ``pacURL``, ``actionTypeZIA``
etc.) are declared by ``request_format`` on the relevant sub-models.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from zscaler.zcc._field_introspect import field_map, nested_types, wire_keys
from zscaler.zcc._serialize import _ZccWireBody, zcc_to_wire
from zscaler.zcc.models.forwardingprofile import (
    ForwardingProfile,
    ForwardingProfileActions,
    ForwardingProfileZpaActions,
    PartnerInfo,
    SystemProxyData,
    UnifiedTunnel,
)

PAYLOAD = Path(__file__).resolve().parent / "fixtures" / "forwarding_profile" / "payload.json"


# Per-class reverse maps (wire_key -> snake_attr) derived from each model's
# request_format. We use these to mechanically re-key the truth payload so
# the test never embeds hand-maintained casing assumptions of its own.
_REVERSE_MAPS: Dict[type, Dict[str, str]] = {
    cls: {wire: snake for snake, wire in field_map(cls).items()}
    for cls in (
        ForwardingProfile,
        ForwardingProfileActions,
        ForwardingProfileZpaActions,
        UnifiedTunnel,
        SystemProxyData,
        PartnerInfo,
    )
}


def _wire_to_snake(value: Any, schema_cls: type) -> Any:
    """Recursively transform a wire-form payload into the snake_case form
    a caller would pass into the SDK, using each schema's reverse map."""
    if isinstance(value, list):
        nested = nested_types(schema_cls)
        return [_wire_to_snake(item, schema_cls) for item in value]
    if not isinstance(value, dict):
        return value
    reverse = _REVERSE_MAPS[schema_cls]
    nested = nested_types(schema_cls)
    out: Dict[str, Any] = {}
    for wire_key, sub_value in value.items():
        snake_key = reverse.get(wire_key, wire_key)
        # Recurse if the parent class declares this sub-tree as a
        # nested model.
        nested_cls = nested.get(snake_key)
        if nested_cls is not None and isinstance(sub_value, (dict, list)):
            sub_value = _wire_to_snake(sub_value, nested_cls)
        out[snake_key] = sub_value
    return out


def _normalize(obj: Any) -> Any:
    """Strip _ZccWireBody / ZscalerObject wrappers so json.dumps can compare."""
    if hasattr(obj, "request_format") and not isinstance(obj, dict):
        return _normalize(obj.request_format())
    if isinstance(obj, dict):
        return {k: _normalize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_normalize(x) for x in obj]
    return obj


def test_payload_round_trip_is_byte_for_byte_identical():
    truth = json.loads(PAYLOAD.read_text())
    snake_input = _wire_to_snake(truth, ForwardingProfile)
    projected = _normalize(zcc_to_wire(snake_input, ForwardingProfile))
    assert json.dumps(projected, sort_keys=True) == json.dumps(truth, sort_keys=True)


def test_zcc_to_wire_returns_marker_dict():
    out = zcc_to_wire({"name": "x"}, ForwardingProfile)
    assert isinstance(out, _ZccWireBody)


def test_irregular_acronym_keys_come_from_the_model_not_field_exceptions():
    """Verify the model declares every irregular wire key. If any of these
    came from heuristic camel-casing or FIELD_EXCEPTIONS we'd be back to
    the old workaround pattern.
    """
    fp_action_keys = wire_keys(ForwardingProfileActions)
    assert "UDPTimeout" in fp_action_keys
    assert "DTLSTimeout" in fp_action_keys
    assert "TLSTimeout" in fp_action_keys
    assert "allowTLSFallback" in fp_action_keys
    assert "latencyBasedServerMTEnablement" in fp_action_keys

    spd_keys = wire_keys(SystemProxyData)
    assert "pacURL" in spd_keys
    assert "enablePAC" in spd_keys
    assert "performGPUpdate" in spd_keys
    assert "bypassProxyForPrivateIP" in spd_keys

    ut_keys = wire_keys(UnifiedTunnel)
    assert "actionTypeZIA" in ut_keys
    assert "actionTypeZPA" in ut_keys

    fp_keys = wire_keys(ForwardingProfile)
    assert "enableLWFDriver" in fp_keys
    assert "enableSplitVpnTN" in fp_keys
    assert "enableAllDefaultAdaptersTN" in fp_keys


def test_nested_types_are_introspected_correctly():
    """The serializer recurses based on ``nested_types``. If any nested
    declaration is missing, sub-tree keys would fall back to the heuristic
    converter — exactly what we are trying to avoid.
    """
    assert nested_types(ForwardingProfile)["forwarding_profile_actions"] is ForwardingProfileActions
    assert nested_types(ForwardingProfile)["forwarding_profile_zpa_actions"] is ForwardingProfileZpaActions
    assert nested_types(ForwardingProfile)["unified_tunnel"] is UnifiedTunnel
    assert nested_types(ForwardingProfileActions)["system_proxy_data"] is SystemProxyData
    assert nested_types(UnifiedTunnel)["system_proxy_data"] is SystemProxyData
    assert nested_types(ForwardingProfileZpaActions)["partner_info"] is PartnerInfo
