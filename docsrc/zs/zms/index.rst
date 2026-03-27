ZMS (Microsegmentation)
=======================

This package covers the ZMS (Zscaler Microsegmentation) API interface for managing microsegmentation resources via GraphQL.

ZMS provides comprehensive microsegmentation capabilities including:

- **Agents** - Agent management, connection status, and version statistics
- **Agent Groups** - Agent group management with TOTP support
- **Nonces** - Provisioning key management
- **Resources** - Resource visibility and protection status
- **Resource Groups** - Managed and unmanaged resource group management
- **Policy Rules** - Microsegmentation policy rule management
- **App Zones** - Application zone management
- **App Catalog** - Application catalog entries
- **Tags** - Tag namespace, key, and value management

.. note::
    ZMS requires OneAPI authentication (OAuth2.0 via Zidentity). Legacy authentication is not supported.

.. toctree::
    :maxdepth: 1
    :hidden:

    agents
    agent_groups
    nonces
    resources
    resource_groups
    policy_rules
    app_zones
    app_catalog
    tags

.. automodule:: zscaler.zms
    :members:
    :undoc-members:
    :show-inheritance:
