# CreateDelegationOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/CreateDelegationOptions



```ts theme={null}
type CreateDelegationOptions = {
  expiresAt: string;
  idempotencyKey?: string;
};
```

Options for creating a delegation that allows a developer to sign on behalf of an end user.

## Properties

| Property                | Type     | Description                                                     |
| ----------------------- | -------- | --------------------------------------------------------------- |
| <a /> `expiresAt`       | `string` | The date until which the delegation is valid (ISO 8601 string). |
| <a /> `idempotencyKey?` | `string` | Optional idempotency key for safe retries.                      |

