# Exchange REST API Pagination
Source: https://docs.cdp.coinbase.com/exchange/rest-api/pagination



Coinbase Exchange uses cursor pagination for all REST requests which return arrays.

Cursor pagination allows for fetching results before and after the current page of results and is well suited for realtime data. Endpoints like `/trades`, `/fills`, `/orders`, return the latest items by default. To retrieve more results subsequent requests should specify which direction to paginate based on the data previously returned.

`before` and `after` cursors are available via response headers `CB-BEFORE` and `CB-AFTER`. Your requests should use these cursor values when making requests for pages after the initial request.

### Parameters

| Parameter | Default | Description                                                |
| :-------- | :------ | :--------------------------------------------------------- |
| `before`  |         | Request page before (newer) this pagination id             |
| `after`   |         | Request page after (older) this pagination id              |
| `limit`   | 1000    | Number of results per request. Maximum 1000 (default 1000) |

### Example

`GET /orders?before=2&limit=30`

### Before and After cursors

The `before` cursor references the first item in a results page and the `after` cursor references the last item in a set of results.

#### Before Cursor

To request a page of records before the current one, use the `before` query parameter. Your initial request can omit this parameter to get the default first page.

The response contains a `CB-BEFORE` header which returns the cursor id to use in your next request for the page before the current one. **The page before is a newer page and not one that happened before in chronological time.**

#### After Cursor

The response also contains a `CB-AFTER` header which returns the cursor id to use in your next request for the page after this one. **The page after is an older page and not one that happened after this one in chronological time.**

<aside>
  Cursor pagination can be unintuitive at first. <code>before</code> and <code>after</code> cursor arguments should not be confused with before and after in chronological time. Most paginated requests return the latest information (newest) as the first page sorted by newest (in chronological time) first. To get older information you would request pages <code>after</code> the initial page. To get information newer, you would request pages <code>before</code> the first page.
</aside>

