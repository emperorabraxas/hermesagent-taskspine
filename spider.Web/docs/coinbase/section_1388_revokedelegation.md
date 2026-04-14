# revokeDelegation
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/revokeDelegation



```ts theme={null}
function revokeDelegation(options?: RevokeDelegationOptions): Promise<void>;
```

Revokes all active delegations for the current end user.
This operation can be performed by the end user themselves or by a developer using their API key.

## Parameters

| Parameter  | Type                                                                                                            | Description                                   |
| ---------- | --------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| `options?` | [`RevokeDelegationOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/RevokeDelegationOptions) | Optional options for revoking the delegation. |

## Returns

`Promise`\<`void`>

A promise that resolves when all active delegations have been revoked.

## Throws

Error if the user is not signed in.

