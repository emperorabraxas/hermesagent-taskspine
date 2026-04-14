# executeSwap
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/executeSwap



```ts theme={null}
function executeSwap(options: ExecuteSwapOptions): Promise<ExecuteSwapResult>;
```

Executes a token swap on behalf of the signed-in user.
The backend atomically quotes, signs Permit2 (if needed), simulates, and submits the transaction.
Returns immediately with a transaction hash (EOA) or user operation hash (smart account).

## Parameters

| Parameter | Type                                                                                                  | Description                    |
| --------- | ----------------------------------------------------------------------------------------------------- | ------------------------------ |
| `options` | [`ExecuteSwapOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/ExecuteSwapOptions) | The swap execution parameters. |

## Returns

`Promise`\<[`ExecuteSwapResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/ExecuteSwapResult)>

A discriminated union result with the transaction/operation hash and swap details.

## Throws

An [InputValidationError](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Classes/InputValidationError) if parameters are invalid.

## Throws

A [SwapError](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Classes/SwapError) for known failures (insufficient liquidity/balance/allowance, simulation failure).

## Throws

An [APIError](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Classes/APIError) for auth, network, or server errors.

## Example

```typescript theme={null}
const result = await executeSwap({
  network: "base",
  fromToken: "0x4200000000000000000000000000000000000006",
  toToken: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
  fromAmount: "100000000000000000",
  slippageBps: 100,
});

if (result.type === "evm-eoa") {
  console.log("Transaction hash:", result.transactionHash);
} else {
  console.log("User operation hash:", result.userOpHash);
}
```

