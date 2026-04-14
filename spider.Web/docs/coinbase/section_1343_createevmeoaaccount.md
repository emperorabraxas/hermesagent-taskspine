# createEvmEoaAccount
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/createEvmEoaAccount



```ts theme={null}
function createEvmEoaAccount(options?: CreateEvmEoaAccountOptions): Promise<`0x${string}`>;
```

Creates an EVM EOA (Externally Owned Account) for the current user.
Multiple EVM EOA accounts can be created per user.

## Parameters

| Parameter  | Type                                                                                                                  | Description                                |
| ---------- | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| `options?` | [`CreateEvmEoaAccountOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/CreateEvmEoaAccountOptions) | Optional options for creating the account. |

## Returns

`Promise`\<`` `0x${string}` ``>

The address of the newly created EVM EOA account.

## Throws

Error if the user is not signed in.

