Zscaler AI Guard
=================
This package covers the Zscaler AI Guard interface.

AI Guard is split across two authentication paths:

* **OneAPI** (``ZscalerClient``) -- detection policies, policy match rules, LLM providers,
  LLM applications and their credentials.
* **Legacy** (``LegacyAIGuardClient``) -- ``policy_detection`` only. The
  ``/v1/detection/*`` endpoints are not available through OneAPI.

.. toctree::
    :maxdepth: 1
    :glob:
    :hidden:

    *

.. automodule:: zscaler.aiguard
    :members:
    :undoc-members:
    :show-inheritance:
