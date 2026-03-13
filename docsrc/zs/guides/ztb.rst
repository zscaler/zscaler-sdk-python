ZTB (Zero Trust Branch) Authentication and Usage
================================================

ZTB authenticates via **API key**. The SDK calls
``POST /api/v3/api-key-auth/login`` with ``{"api_key": "..."}`` and receives a
``delegate_token`` used as ``Authorization: Bearer <token>`` for all subsequent requests.

Environment Variables
---------------------

+----------------------+--------+------------------------------------------------------------------+
| Variable             | Req.   | Description                                                      |
+======================+========+==================================================================+
| ``ZTB_API_KEY``      | Yes*   | ZTB API key created in the ZTB UI                                 |
+----------------------+--------+------------------------------------------------------------------+
| ``ZTB_CLOUD``        | Yes**  | Cloud subdomain (e.g. ``zscalerbd-api``). Base URL:               |
|                      |        | ``https://{cloud}.goairgap.com``                                  |
+----------------------+--------+------------------------------------------------------------------+
| ``ZTB_OVERRIDE_URL`` | No     | Full base URL override. If set, ``cloud`` is not required.        |
+----------------------+--------+------------------------------------------------------------------+
| ``ZSCALER_PARTNER_ID`` | No   | Partner ID for ``x-partner-id`` header                            |
+----------------------+--------+------------------------------------------------------------------+

\* Or pass ``api_key`` in config.
\** Or ``ZTB_OVERRIDE_URL``; at least one of ``cloud`` or ``override_url`` is required.

Configuration Options
---------------------

+------------------+-----------+------------------------------------------------------------------------+
| Option           | Default   | Description                                                             |
+==================+===========+========================================================================+
| ``api_key``      | required  | ZTB API key from the ZTB console                                        |
+------------------+-----------+------------------------------------------------------------------------+
| ``cloud``        | required* | Cloud subdomain (e.g. ``zscalerbd-api``)                                 |
+------------------+-----------+------------------------------------------------------------------------+
| ``override_url`` | ``None``  | Full base URL override. Include protocol (``https://``).                |
+------------------+-----------+------------------------------------------------------------------------+
| ``partner_id``   | ``None``  | Partner ID for ``x-partner-id`` header                                  |
+------------------+-----------+------------------------------------------------------------------------+
| ``timeout``      | ``240``   | Request timeout in seconds                                              |
+------------------+-----------+------------------------------------------------------------------------+
| ``max_retries``  | ``5``     | Max retry attempts for 429/5xx/network errors                           |
+------------------+-----------+------------------------------------------------------------------------+

\* Required if ``override_url`` is not set.

Important Notes
---------------

- ZTB is available only via the **Legacy** client (``LegacyZTBClient``). OneAPI/OAuth2 is not supported for ZTB.
- On **401 Unauthorized**, the client automatically re-authenticates and retries once.
- On **429** (rate limit) or **5xx** (502/503/504), the SDK retries with exponential backoff.
- Request bodies remain in **snake_case**; query parameters are converted to camelCase by the SDK.

Available Resources
-------------------

Resources are accessed via ``client.ztb.<resource>``:

- **alarms** — Alarms API
- **api_keys** — API key auth
- **app_connector_config** — App connector configuration
- **devices** — Active devices, device tags, OS list, device details, DHCP history, filter values
- **groups_router** — Groups router
- **logs** — Logs and visibility charts
- **policy_comments** — Policy comments
- **ransomware_kill** — Ransomware kill
- **site** — Site management
- **site2site_vpn** — Site-to-site VPN (Cloud Gateway)
- **template_router** — Template router

Example
-------

.. code-block:: py

   from zscaler.oneapi_client import LegacyZTBClient

   config = {
       "api_key": "{yourZTBAPIKey}",
       "cloud": "zscalerbd-api",
       "logging": {"enabled": False, "verbose": False},
   }

   def main():
       with LegacyZTBClient(config) as client:
           alarms, response, error = client.ztb.alarms.list_alarms()
           if error:
               print(f"Error: {error}")
               return

           devices, _, err = client.ztb.devices.list_active_devices(
               query_params={"page": 1, "limit": 25}
           )
           if not err:
               for d in devices:
                   print(d.hostname)

   if __name__ == "__main__":
       main()
