# createDelegation
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/createDelegation



```ts theme={null}
function createDelegation(options: CreateDelegationOptions): Promise<CreateDelegationResult>;
```

Creates a delegation that allows a developer to sign on behalf of an end user for the specified duration.
The end user must be authenticated to authorize this delegation.

## Parameters

| Parameter | Type                                                                                                            | Description                          |
| --------- | --------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| `options` | [`CreateDelegationOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/CreateDelegationOptions) | Options for creating the delegation. |

## Returns

`Promise`\<[`CreateDelegationResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/CreateDelegationResult)>

The delegation ID.

## Throws

If `expiresAt` is not a valid date or is not in the future.

## Throws

Error if the user is not signed in.

