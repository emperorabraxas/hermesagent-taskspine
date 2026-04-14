# sendSolanaTransaction
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/sendSolanaTransaction



```ts theme={null}
function sendSolanaTransaction(options: SendSolanaTransactionOptions): Promise<SendSolanaTransactionResult>;
```

Send a Solana transaction.

## Parameters

| Parameter | Type                                                                                                                      | Description                                     |
| --------- | ------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| `options` | [`SendSolanaTransactionOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendSolanaTransactionOptions) | The options for sending the Solana transaction. |

## Returns

`Promise`\<[`SendSolanaTransactionResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendSolanaTransactionResult)>

The transaction signature.

