# waitForEvmEip7702Delegation
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/waitForEvmEip7702Delegation



```ts theme={null}
function waitForEvmEip7702Delegation(options: WaitForEvmEip7702DelegationOptions): Promise<
  | false
| EvmEip7702DelegationOperation>;
```

Polls the EIP-7702 delegation operation status until it reaches COMPLETED, FAILED, or the timeout is reached.

## Parameters

| Parameter | Type                                                                                                                                  | Description                                                         |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `options` | [`WaitForEvmEip7702DelegationOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/WaitForEvmEip7702DelegationOptions) | Options for the delegation operation to check and polling behavior. |

## Returns

`Promise`\<
\| `false`
\| [`EvmEip7702DelegationOperation`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/EvmEip7702DelegationOperation)>

The delegation operation on COMPLETED; false on timeout.

## Throws

Error if the operation status is FAILED.

## Example

```ts theme={null}
const result = await waitForEvmEip7702Delegation({
  delegationOperationId: 'op-123',
  timeoutMs: 60_000,
});
if (result) {
  console.log('Delegation completed:', result.transactionHash);
} else {
  console.log('Timed out');
}
```

