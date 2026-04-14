# signEvmTransaction
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/signEvmTransaction



```ts theme={null}
function signEvmTransaction(options: SignEvmTransactionOptions): Promise<SignEvmTransactionResult>;
```

Signs a hash with an EVM account.

## Parameters

| Parameter | Type                                                                                                                | Description                  |
| --------- | ------------------------------------------------------------------------------------------------------------------- | ---------------------------- |
| `options` | [`SignEvmTransactionOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SignEvmTransactionOptions) | The options for the signing. |

## Returns

`Promise`\<[`SignEvmTransactionResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SignEvmTransactionResult)>

The result of the signing.

## Example

```typescript lines theme={null}
const user = await getCurrentUser();
const evmAccount = user?.evmAccountObjects[0]?.address;

const result = await signEvmTransaction({
  evmAccount,
  transaction: {
    to: "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    value: 100000000000000n, // 0.0001 ETH in wei
    nonce: 0,
    gas: 21000n,
    maxFeePerGas: 30000000000n,
    maxPriorityFeePerGas: 1000000000n,
    chainId: 84532, // Base Sepolia
    type: "eip1559",
  }
});
```

