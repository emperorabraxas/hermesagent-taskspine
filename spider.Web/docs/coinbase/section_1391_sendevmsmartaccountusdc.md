# sendEvmSmartAccountUsdc
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/sendEvmSmartAccountUsdc



```ts theme={null}
function sendEvmSmartAccountUsdc(options: SendEvmSmartAccountUsdcOptions): Promise<SendEvmSmartAccountUsdcResult>;
```

Sends USDC on an EVM network from a Smart Account.

## Parameters

| Parameter | Type                                                                                                                          | Description                   |
| --------- | ----------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| `options` | [`SendEvmSmartAccountUsdcOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendEvmSmartAccountUsdcOptions) | The options for sending USDC. |

## Returns

`Promise`\<[`SendEvmSmartAccountUsdcResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendEvmSmartAccountUsdcResult)>

The result of sending USDC.

## Example

```typescript theme={null}
const user = await getCurrentUser();
const evmSmartAccount = user?.evmSmartAccountObjects[0]?.address;

const result = await sendEvmSmartAccountUsdc({
  evmSmartAccount,
  to: "0x1234567890123456789012345678901234567890",
  amount: "10.00",
  network: "base-sepolia",
  useCdpPaymaster: true, // Optional: sponsor gas fees
});

console.log("User Operation Hash:", result.userOpHash);
```

