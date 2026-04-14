# FetchWithX402Options
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/FetchWithX402Options



```ts theme={null}
type FetchWithX402Options = {
  address?:   | EvmAddress
     | string;
  fetch?: typeof globalThis.fetch;
  maxValue?: bigint;
  paymentRequirementsSelector?: PaymentRequirementsSelector;
  config?: X402Config;
};
```

Options for the fetchWithX402 function.

## Properties

| Property                             | Type                                                                                                 | Description                                                             |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| <a /> `address?`                     | \| [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmAddress) \| `string` | The address of the account to use for the fetch function.               |
| <a /> `fetch?`                       | *typeof* `globalThis.fetch`                                                                          | The fetch function to use for the fetch function.                       |
| <a /> `maxValue?`                    | `bigint`                                                                                             | The maximum allowed payment amount in base units (defaults to 0.1 USDC) |
| <a /> `paymentRequirementsSelector?` | `PaymentRequirementsSelector`                                                                        | A function that selects the payment requirements from the response      |
| <a /> `config?`                      | `X402Config`                                                                                         | Optional configuration for X402 operations (e.g., custom RPC URLs)      |

