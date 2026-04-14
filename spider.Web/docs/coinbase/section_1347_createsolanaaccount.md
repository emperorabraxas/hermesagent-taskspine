# createSolanaAccount
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/createSolanaAccount



```ts theme={null}
function createSolanaAccount(options?: CreateSolanaAccountOptions): Promise<string>;
```

Creates a Solana account for the current user.
Multiple Solana accounts can be created per user.

## Parameters

| Parameter  | Type                                                                                                                  | Description                                |
| ---------- | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| `options?` | [`CreateSolanaAccountOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/CreateSolanaAccountOptions) | Optional options for creating the account. |

## Returns

`Promise`\<`string`>

The address of the newly created Solana account.

## Throws

Error if the user is not signed in.

