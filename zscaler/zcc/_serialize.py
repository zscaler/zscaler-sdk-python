"""
ZCC-only request body serializer.

This module converts a user-supplied request body (typically containing
snake_case keys) into the exact wire-key casing declared by a ZCC model
class via its ``request_format`` method.

Design goals:

* The model class is the single source of truth for wire keys.
* No reliance on heuristic snake-to-camel conversion or hand-maintained
  ``FIELD_EXCEPTIONS`` tables.
* Per-class scoping: the same snake_case attribute can map to different
  wire keys depending on which model class it belongs to (e.g.
  ``WindowsPolicy.disable_password`` -> ``disable_password`` (snake on
  the wire) vs ``LinuxPolicy.disable_password`` -> ``disablePassword``).
* camelCase wire keys passed by the user are accepted as-is; unknown keys
  pass through unchanged so we never silently drop or mangle data.

This module applies to ZCC only and must not be used by other services.
"""

from __future__ import annotations

from typing import Any, Type

from zscaler.helpers import convert_keys_to_camel_case_selective, to_lower_camel_case
from zscaler.oneapi_object import ZscalerObject

from ._field_introspect import field_map, nested_types, wire_keys


def _legacy_snake_preserve_keys() -> "set[str]":
    """
    The set of snake_case keys the legacy ZCC converter has historically
    preserved on the wire (currently ``WebPolicy.SNAKE_CASE_KEYS``).

    Treated as a transitional fallback: any key listed here passes through
    the serializer unchanged when the per-class model does not declare it.
    Sourced lazily to avoid a circular import at module load time.
    """
    from zscaler.zcc.models.webpolicy import WebPolicy

    return WebPolicy.SNAKE_CASE_KEYS


class _ZccWireBody(dict):
    """
    Marker dict subclass indicating that the body has already been
    serialized into ZCC wire form by :func:`zcc_to_wire`.

    The request executor checks ``isinstance(body, _ZccWireBody)`` to skip
    its legacy ``convert_keys_to_camel_case_selective`` step for ZCC
    endpoints.

    Acts as a regular dict for ``json.dumps`` and downstream consumers.
    """


def _resolve_wire_key(provided_key: str, fmap: "dict[str, str]", wkeys: "set[str]") -> str:
    """Return the wire-form key for ``provided_key``.

    Resolution order (model first, legacy behaviour as a strict superset):

      1. Snake_case attribute name declared by the model -> use the wire
         key declared in ``request_format``.
      2. Wire-form key already declared by the model -> keep as-is.
      3. Snake_case key listed in the legacy ``WebPolicy.SNAKE_CASE_KEYS``
         set -> preserve as snake_case. This covers fields the API expects
         in snake_case but the SDK model has not yet incorporated (e.g.
         top-level ``allowed_apps``, ``bypass_mms_apps``).
      4. Otherwise -> fall back to ``to_lower_camel_case`` (which honours
         the existing ``FIELD_EXCEPTIONS`` table). Already-camelCase keys
         pass through unchanged because the converter is a no-op for
         strings without an underscore.
    """
    if provided_key in fmap:
        return fmap[provided_key]
    if provided_key in wkeys:
        return provided_key
    if provided_key in _legacy_snake_preserve_keys():
        return provided_key
    return to_lower_camel_case(provided_key)


def _resolve_nested_cls(
    provided_key: str,
    nested: "dict[str, Type[ZscalerObject]]",
    fmap: "dict[str, str]",
) -> "Type[ZscalerObject] | None":
    """
    Look up the nested model class for ``provided_key`` (which may be the
    snake_case attribute name or the wire-form key). Returns ``None`` when
    the key does not designate a nested structure.
    """
    if provided_key in nested:
        return nested[provided_key]
    for snake_name, wire_name in fmap.items():
        if wire_name == provided_key and snake_name in nested:
            return nested[snake_name]
    return None


def zcc_to_wire(body: Any, schema_cls: Type[ZscalerObject]) -> Any:
    """
    Convert ``body`` to the exact wire shape declared by ``schema_cls``.

    Args:
        body: The user's request body. May be a dict, a list of dicts, a
            ``ZscalerObject`` instance, or a primitive. Non-dict / non-list
            primitives are returned unchanged.
        schema_cls: The ZCC model class that defines the wire shape. Must
            be a subclass of :class:`ZscalerObject`.

    Returns:
        A :class:`_ZccWireBody` dict (for dict inputs), a list (for list
        inputs whose elements are dicts), or the original value otherwise.
    """
    if isinstance(body, ZscalerObject):
        body = body.request_format()

    if isinstance(body, list):
        return [zcc_to_wire(item, schema_cls) if isinstance(item, dict) else item for item in body]

    if not isinstance(body, dict):
        return body

    fmap = field_map(schema_cls)
    nested = nested_types(schema_cls)
    wkeys = wire_keys(schema_cls)

    snake_preserve = _legacy_snake_preserve_keys()

    out = _ZccWireBody()
    for raw_key, value in body.items():
        wire_key = _resolve_wire_key(raw_key, fmap, wkeys)
        nested_cls = _resolve_nested_cls(raw_key, nested, fmap)

        if nested_cls is not None:
            # Schema-aware recursion: the model declares a class for this
            # sub-tree, so use it as the schema for the recursive call.
            if isinstance(value, dict):
                value = zcc_to_wire(value, nested_cls)
            elif isinstance(value, list):
                value = [zcc_to_wire(item, nested_cls) if isinstance(item, dict) else item for item in value]
        elif isinstance(value, (dict, list)) and not isinstance(value, _ZccWireBody):
            # No sub-schema declared. Fall back to the legacy ZCC converter
            # for this subtree so containers like ``endToEndDiagnostics``,
            # ``generateCliPasswordContract`` and ``locationRulesetPolicies``
            # still get their child keys correctly cased (offTrusted,
            # vpnTrusted, allowZpaDisableWithoutPassword, etc.).
            value = convert_keys_to_camel_case_selective(value, snake_preserve)

        out[wire_key] = value

    return out
