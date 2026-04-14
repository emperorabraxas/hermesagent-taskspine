# getEvmEip7702DelegationOperation
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/getEvmEip7702DelegationOperation



```ts theme={null}
function getEvmEip7702DelegationOperation(options: GetEvmEip7702DelegationOperationOptions): Promise<EvmEip7702DelegationOperation>;
```

Returns the current status of an EIP-7702 delegation operation for an end user's EVM account.
Use the delegationOperationId returned by createEvmEip7702Delegation to poll for operation completion.

## Parameters

| Parameter | Type                                                                                                                                            | Description                                     |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| `options` | [`GetEvmEip7702DelegationOperationOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/GetEvmEip7702DelegationOperationOptions) | Options containing the delegation operation ID. |

## Returns

`Promise`\<[`EvmEip7702DelegationOperation`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/EvmEip7702DelegationOperation)>

The delegation operation status (PENDING, SUBMITTED, COMPLETED, or FAILED).

## Throws

Error if the user is not signed in.

