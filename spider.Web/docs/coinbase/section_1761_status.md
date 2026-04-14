# Status
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/Status



```ts theme={null}
type Status = "idle" | "pending" | "success" | "error";
```

Represents the status of a request.

* "idle": No request in progress.
* "pending": Request sent, waiting for confirmation.
* "success": Request confirmed, includes result.
* "error": Request failed, includes error details.

