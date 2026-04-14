# SwapIssues
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/SwapIssues



```ts theme={null}
type SwapIssues = {
  allowance: SwapIssuesAllowance | null;
  balance: SwapIssuesBalance | null;
};
```

Potential issues discovered during preflight checks that could prevent the swap from being executed successfully. Null if no issues were detected.

## Properties

| Property          | Type                            | Description                                                                                                                     |
| ----------------- | ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| <a /> `allowance` | `SwapIssuesAllowance` \| `null` | Details of the allowance that the `taker` must set in order to execute the swap successfully. Null if no allowance is required. |
| <a /> `balance`   | `SwapIssuesBalance` \| `null`   | Details of the `fromToken` balance that the `taker` must hold. Null if the `taker` has a sufficient balance.                    |

