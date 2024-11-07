## ZPA Pagination

This SDK offers several pagination controls that help manage data retrieval efficiently from the API. Understanding and using these controls properly ensures effective data handling and optimal usage of network resources.

### Available Pagination Controls

1. **`page`**
   - **Purpose:** Specifies the starting page number for the API request.
   - **Use Case:** Ideal for resuming data fetching from a specific point, especially useful if the operations were previously interrupted.

2. **`pagesize`**
   - **Purpose:** Defines the number of items to be returned per page.
   - **Use Case:** Designed to control the volume of data per API call, which is crucial for managing memory overhead and coping with current rate-limits.

3. **`max_pages`**
   - **Purpose:** Sets a limit on the number of pages that can be retrieved.
   - **Use Case:** Great for to cap the extent of data fetched, especially when only a sample or a finite number of API calls is desired.

4. **`max_items`**
   - **Purpose:** Caps the total number of items retrieved across all pages.
   - **Use Case:** Ensures that the fetching process stops once a specific number of items is reached, perfect when a precise dataset size is needed.

### Guidelines and Best Practices

- **Combining Controls:**
  - Combining `page` and `pagesize` provides a straightforward control over the start point and volume of data for each fetch.
  - Using `max_pages` and `max_items` provides limits on the fetching operations but from different perspectives: `max_pages` limits the number of fetch operations, whereas `max_items` limits the total number of items fetched.

- **Preventing Parameter Conflicts:**
  - Mixing `page` or `pagesize` with `max_pages` or `max_items` can lead to conflicts in the data fetching logic. To prevent these issues and ensure clarity:
    - A `ValueError` exception is thrown if both sets of parameters are used simultaneously. This alert helps avoid misconfigurations that can lead to inefficient data fetching and potential performance issues.

- **Error Handling:**
  - **`ValueError`:** This is raised to alert about the improper use of incompatible pagination controls. It ensures developers are aware to not mix direct pagination controls (`page`, `pagesize`) with overarching limits (`max_pages`, `max_items`).

- **Recommendations:**
  - Use `page` and `pagesize` for straightforward pagination without intrinsic limits on the number or volume of data.
  - Choose either `max_pages` or `max_items` based on the specific requirements of the operation to avoid unnecessary complexity and potential conflicts.
  - Always set sensible defaults for `pagesize` to prevent excessive data fetches.

