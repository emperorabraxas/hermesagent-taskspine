# getUserOperation
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/getUserOperation



```ts theme={null}
function getUserOperation(options: GetUserOperationOptions): Promise<EvmUserOperation>;
```

Gets a user operation by its hash.

## Parameters

| Parameter | Type                                                                                                            | Description                                 |
| --------- | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| `options` | [`GetUserOperationOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/GetUserOperationOptions) | The options for getting the user operation. |

## Returns

`Promise`\<[`EvmUserOperation`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/EvmUserOperation)>

The user operation details.

## Example

```typescript lines theme={null}
const result = await getUserOperation({
  userOperationHash: "0x123...",
  evmSmartAccount: "0xabc...",
  network: "base-sepolia"
});
console.log("User Operation Status:", result.transactionHash);
```

