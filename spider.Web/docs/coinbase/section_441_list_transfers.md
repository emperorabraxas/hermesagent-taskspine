# List transfers
Source: https://docs.cdp.coinbase.com/api-reference/payment-apis/rest-api/transfers-under-development/list-transfers

get /v2/transfers
List transfers for your organization. Use this to view and monitor your transfer activity.

**Status Filtering**: Filter by specific status to efficiently manage transfers:
* `?status=processing` - Monitor active transfers.
* `?status=quoted` - Find transfers awaiting execution.
* `?status=failed` - Review failed transfers for troubleshooting.
* `?status=completed` - Find completed transfers.

**Account Filtering**: Filter by account ID to find transfers involving a specific account:
* `?accountId=<ID>` - All transfers where the account is either source or target (OR semantics).
* `?sourceAccountId=<ID>` - Only transfers where the account is the source (outbound).
* `?targetAccountId=<ID>` - Only transfers where the account is the target (inbound).
Providing `accountId` together with `sourceAccountId` or `targetAccountId` is a validation error and returns HTTP 400.

**Date Range Filtering**: Filter by creation or last-updated time for reconciliation:
* `?createdAfter=2026-01-01T00:00:00Z&createdBefore=2026-01-31T23:59:59Z` - Transfers created within a date range.
* `?updatedAfter=2026-01-01T00:00:00Z` - Transfers updated since a given time. Useful for incremental sync.

**Asset Filtering**: Filter by source or target asset symbol:
* `?sourceAsset=usd` - Transfers funded from a USD account.
* `?targetAsset=usdc` - Transfers delivering USDC to the target.

**Other Filters**:
* `?sourceAddress=0x...` - Transfers from a specific on-chain source address.
* `?targetAddress=0x...` - Transfers to a specific on-chain destination address.
* `?targetEmail=user@example.com` - Transfers to a specific email recipient.
* `?transferId=transfer_...` - Look up a single transfer by ID; bypasses pagination.


