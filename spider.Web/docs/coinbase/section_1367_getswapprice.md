# getSwapPrice
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/getSwapPrice



```ts theme={null}
function getSwapPrice(options: GetSwapPriceOptions): Promise<
  | GetSwapPriceResult
| SwapUnavailableResult>;
```

Gets a non-binding indicative price for a token swap.
Read-only operation — does not modify any on-chain state.

## Parameters

| Parameter | Type                                                                                                    | Description                        |
| --------- | ------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| `options` | [`GetSwapPriceOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/GetSwapPriceOptions) | The swap price request parameters. |

## Returns

`Promise`\<
\| [`GetSwapPriceResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/GetSwapPriceResult)
\| [`SwapUnavailableResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SwapUnavailableResult)>

Price estimate if liquidity is available, otherwise `{ liquidityAvailable: false }`.

## Throws

An [InputValidationError](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Classes/InputValidationError) if parameters are invalid.

## Throws

An Error if the response is missing required fields when liquidity is available.

## Example

```typescript theme={null}
const price = await getSwapPrice({
  network: "base",
  fromToken: "0x4200000000000000000000000000000000000006",
  toToken: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
  fromAmount: "100000000000000000",
});

if (price.liquidityAvailable) {
  console.log("Expected output:", price.toAmount);
}
```

