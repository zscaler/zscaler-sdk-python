"""
ZCC-only model introspection.

This module derives the wire-level field mapping for any ZCC ZscalerObject
subclass directly from its existing ``request_format`` and ``__init__``
implementations. It does not modify or require any change to the model
classes themselves.

The serializer in ``_serialize.py`` uses the maps produced here to convert
user-supplied snake_case bodies into the exact key casing the ZCC API
expects, without relying on the heuristic snake-to-camel converter or its
hand-maintained ``FIELD_EXCEPTIONS`` table.

This module applies to ZCC only and does not affect other services.
"""

from __future__ import annotations

import ast
import inspect
import sys
import textwrap
from functools import lru_cache
from typing import Any, Dict, Set, Type

from zscaler.oneapi_object import ZscalerObject


class _AttrTracer:
    """Sentinel that records the snake_case attribute name accessed on the tracer."""

    __slots__ = ("name",)

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:  # pragma: no cover - debugging aid only
        return f"_AttrTracer({self.name!r})"


def _make_tracer(cls: Type[ZscalerObject]):
    """
    Return an instance that masquerades as ``cls`` and records every attribute
    access. Used to introspect ``cls.request_format`` without running the
    real ``__init__`` logic.

    A dynamic subclass is required because ``request_format`` calls
    ``super()`` (zero-arg form) which validates that ``self`` is an instance
    of the enclosing class.
    """

    accessed: Dict[str, _AttrTracer] = {}

    class _Tracer(cls):  # type: ignore[misc, valid-type]
        # ``__getattr__`` only fires on missing attribute lookup, so it does
        # not interfere with method dispatch or ``super()`` resolution.
        def __getattr__(self, name: str):
            if name not in accessed:
                accessed[name] = _AttrTracer(name)
            return accessed[name]

    inst = _Tracer.__new__(_Tracer)
    return inst, accessed


@lru_cache(maxsize=None)
def field_map(cls: Type[ZscalerObject]) -> Dict[str, str]:
    """
    Return ``{snake_case_attr -> wire_key}`` for ``cls`` by tracing its
    ``request_format`` method.

    Only entries whose value is a direct ``self.<attr>`` reference are
    captured. Literal/computed values (rare in current ZCC models) are
    intentionally skipped because they are not user-controllable and have
    no snake_case form.
    """

    tracer, _ = _make_tracer(cls)
    raw = cls.request_format(tracer)  # type: ignore[arg-type]
    return {value.name: key for key, value in raw.items() if isinstance(value, _AttrTracer)}


@lru_cache(maxsize=None)
def wire_keys(cls: Type[ZscalerObject]) -> Set[str]:
    """Return the set of wire-level keys declared by ``cls.request_format``."""
    return set(field_map(cls).values())


def _extract_nested_class_name(value_node: ast.AST) -> str | None:
    """
    Extract the name of a likely nested model class from the RHS of an
    ``Assign`` node in a model's ``__init__``.

    Recognized patterns (matching the conventions used throughout
    ``zscaler/zcc/models``):

    * ``self.x = NestedClass(config[...])``
    * ``self.x = ZscalerCollection.form_list(..., NestedClass)``
    * Either of the above wrapped in a conditional expression
      (``A if cond else B``).
    """

    if isinstance(value_node, ast.Call):
        func = value_node.func
        if isinstance(func, ast.Name):
            return func.id
        if (
            isinstance(func, ast.Attribute)
            and isinstance(func.value, ast.Name)
            and func.value.id == "ZscalerCollection"
            and func.attr == "form_list"
            and value_node.args
        ):
            last = value_node.args[-1]
            if isinstance(last, ast.Name):
                return last.id
        return None

    if isinstance(value_node, ast.IfExp):
        for branch in (value_node.body, value_node.orelse):
            name = _extract_nested_class_name(branch)
            if name is not None:
                return name

    return None


@lru_cache(maxsize=None)
def nested_types(cls: Type[ZscalerObject]) -> Dict[str, Type[ZscalerObject]]:
    """
    Inspect ``cls.__init__`` and return ``{snake_case_attr -> NestedClass}``
    for every attribute whose value is constructed from another
    ``ZscalerObject`` subclass.

    This drives recursive serialization: when a nested attribute is present
    in the user's body, the serializer uses the corresponding nested class
    as the schema for that sub-tree.
    """

    try:
        source = textwrap.dedent(inspect.getsource(cls.__init__))
    except (OSError, TypeError):
        return {}

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return {}

    module = sys.modules.get(cls.__module__)
    if module is None:
        return {}

    if not tree.body or not isinstance(tree.body[0], ast.FunctionDef):
        return {}

    result: Dict[str, Type[ZscalerObject]] = {}
    for node in ast.walk(tree.body[0]):
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not (isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == "self"):
            continue
        attr_name = target.attr
        if attr_name in result:
            continue
        class_name = _extract_nested_class_name(node.value)
        if class_name is None:
            continue
        candidate = getattr(module, class_name, None)
        if isinstance(candidate, type) and issubclass(candidate, ZscalerObject) and candidate is not ZscalerObject:
            result[attr_name] = candidate

    return result


def reset_caches() -> None:
    """Clear all introspection caches. Intended for tests only."""
    field_map.cache_clear()
    wire_keys.cache_clear()
    nested_types.cache_clear()
