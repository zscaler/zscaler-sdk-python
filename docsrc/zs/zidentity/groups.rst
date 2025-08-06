groups
-------

The following methods allow for interaction with the Zidentity
Groups API endpoints.

Methods are accessible via ``zidentity.groups``

Pagination
~~~~~~~~~~

The Zidentity Groups API supports pagination with a maximum page size of 100 records per request. The SDK automatically handles pagination for all groups endpoints.

**Key Features:**
- **Maximum Page Size**: 100 records per page (enforced by API)
- **Automatic Pagination**: SDK handles pagination transparently
- **Response Format**: Returns data in `records` field with pagination metadata

**Example Usage:**

.. code-block:: python

    from zscaler import ZscalerClient

    config = {
        "clientId": '{yourClientId}',
        "clientSecret": '{yourClientSecret}',
        "vanityDomain": '{yourvanityDomain}',
        "cloud": "beta",
    }

    def main():
        with ZscalerClient(config) as client:
            # Request 300 groups (will automatically fetch 3 pages)
            groups_response, response, error = client.zidentity.groups.list_groups(
                query_params={'page_size': 300}
            )
            
            if error:
                print(f"Error listing groups: {error}")
                return
            
            print(f"Total groups in response: {len(groups_response.records)}")
            print(f"Total available: {groups_response.results_total}")
            print(f"Page offset: {groups_response.page_offset}")
            print(f"Page size: {groups_response.page_size}")
            
            # Access individual groups
            for group in groups_response.records:
                print(f"Group: {group.name} (ID: {group.id})")
            
            # Manual pagination using response object
            while response.has_next():
                next_results, error = response.next()
                if error:
                    print(f"Error fetching next page: {error}")
                    break
                
                print(f"Next page: {len(next_results)} groups")
                for group in next_results:
                    print(f"Group: {group['name']} (ID: {group['id']})")

    if __name__ == "__main__":
        main()

**Pagination Metadata:**
The `Groups` model provides convenient access to pagination metadata:
- `groups_response.results_total`: Total number of records available
- `groups_response.page_offset`: Current page offset
- `groups_response.page_size`: Number of records per page (max 100)
- `groups_response.next_link`: URL for next page (if available)
- `groups_response.prev_link`: URL for previous page (if available)
- `groups_response.records`: Collection of `GroupRecord` objects

.. _zidentity-groups:

.. automodule:: zscaler.zidentity.groups
    :members:
    :undoc-members:
    :show-inheritance:
