# createEvmEip7702Delegation
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/createEvmEip7702Delegation



```ts theme={null}
function createEvmEip7702Delegation(options: CreateEvmEip7702DelegationOptions): Promise<CreateEvmEip7702DelegationResult>;
```

Creates an EIP-7702 delegation for an end user's EVM EOA account, upgrading it with smart account capabilities.

This endpoint retrieves delegation artifacts from onchain, signs the EIP-7702 authorization,
submits a Type 4 transaction, and creates an associated smart account object. After success,
the local auth state is refreshed so the new smart account appears in the user's account list.

## Parameters

| Parameter | Type                                                                                                                                | Description                                   |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| `options` | [`CreateEvmEip7702DelegationOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/CreateEvmEip7702DelegationOptions) | Options for creating the EIP-7702 delegation. |

## Returns

`Promise`\<[`CreateEvmEip7702DelegationResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/CreateEvmEip7702DelegationResult)>

The delegation operation ID for polling the operation status.

## Throws

Error if the user is not signed in.

## Throws

Error if the address does not belong to the current user.

