# linkSms
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/linkSms



```ts theme={null}
function linkSms(phoneNumber: string, options?: {
  idempotencyKey?: string;
}): Promise<{
  flowId: string;
  message: string;
}>;
```

Links a SMS account to the current user.

## Parameters

| Parameter                 | Type                              | Description                                |
| ------------------------- | --------------------------------- | ------------------------------------------ |
| `phoneNumber`             | `string`                          | The phone number to link.                  |
| `options?`                | \{ `idempotencyKey?`: `string`; } | Optional options for the link operation.   |
| `options.idempotencyKey?` | `string`                          | Optional idempotency key for safe retries. |

## Returns

`Promise`\<\{
`flowId`: `string`;
`message`: `string`;
}>

The result of the link SMS initiation.

