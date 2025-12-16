Z-Insights
==========

This package covers the Z-Insights Analytics API interface for querying security analytics data via GraphQL.

Z-Insights provides unified real-time visibility into:

- **Web Traffic** - Traffic analytics by location, user, protocol, and threat categories
- **Cyber Security** - Security incidents and threat analysis across all security layers
- **Firewall** - Zero Trust Firewall traffic, actions, and network services
- **SaaS Security** - Cloud Access Security Broker (CASB) application reports
- **Shadow IT** - Discovered application analytics and risk assessment
- **IoT** - IoT device visibility and classification statistics

.. note::
    Z-Insights requires OneAPI authentication (OAuth2.0 via Zidentity). Legacy authentication is not supported.

.. toctree::
    :maxdepth: 1
    :hidden:

    web_traffic
    cyber_security
    firewall
    saas_security
    shadow_it
    iot

.. automodule:: zscaler.zinsights
    :members:
    :undoc-members:
    :show-inheritance:
