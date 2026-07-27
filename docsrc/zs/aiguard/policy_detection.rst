policy_detection
================

The following methods allow for interaction with the Zscaler AI Guard Policy Detection API endpoints.
Includes executing a detection policy and resolving-and-executing a detection policy against content.

.. warning::

    **These endpoints are only available through the legacy AI Guard client.**

    The policy detection endpoints (``/v1/detection/execute-policy`` and
    ``/v1/detection/resolve-and-execute-policy``) are **not** exposed through OneAPI.
    They must be called with :class:`~zscaler.oneapi_client.LegacyAIGuardClient`, which
    authenticates with an AI Guard API key against ``https://api.<cloud>.zseclipse.net``.

    Every other AI Guard resource -- detection policies, policy match rules, LLM
    providers, LLM applications and their credentials -- is **OneAPI only** and is
    reached with ``ZscalerClient``.

Methods are accessible via ``aiguard.policy_detection`` on a ``LegacyAIGuardClient``:

.. code-block:: python

    from zscaler.oneapi_client import LegacyAIGuardClient

    with LegacyAIGuardClient({"api_key": "<api key>", "cloud": "us1"}) as client:
        result, _, err = client.aiguard.policy_detection.resolve_and_execute_policy(
            content="User prompt or AI response to scan",
            direction="IN",
        )

The API key may also be supplied through the ``AIGUARD_API_KEY`` environment variable
(``AIGUARD_CLOUD`` for the cloud, ``AIGUARD_OVERRIDE_URL`` to override the base URL).

.. _aiguard-policy_detection:

.. automodule:: zscaler.aiguard.policy_detection
    :members:
    :undoc-members:
    :show-inheritance:
