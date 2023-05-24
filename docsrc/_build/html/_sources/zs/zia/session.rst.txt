session
========

The following methods allow for interaction with the ZIA Authentication Session API endpoints.

Methods are accessible via ``zia.session``

There is no need to manually create or delete a Zscaler SDK Python session, especially if you are using a
context handler such as ``with``. The example below shows correct usage of Zscaler SDK Python to print
the GRE tunnels configured in ZIA. The authenticated session will be automatically torn down by
Zscaler SDK Python after all the tunnels have been printed.


.. code-block:: python

    from zscaler.zia import ZIA

    with ZIA() as zia:
        for tunnel in zia.traffic.list_gre_tunnels():
            print(tunnel)

.. _zia-session:

.. automodule:: zscaler.zia.session
    :members: