# linkEmail
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/linkEmail



```ts theme={null}
function linkEmail(email: string, options?: {
  idempotencyKey?: string;
}): Promise<{
  flowId: string;
  message: string;
}>;
```

Links an email account to the current user.

## Parameters

| Parameter                 | Type                              | Description                                |
| ------------------------- | --------------------------------- | ------------------------------------------ |
| `email`                   | `string`                          | The email address to link.                 |
| `options?`                | \{ `idempotencyKey?`: `string`; } | Optional options for the link operation.   |
| `options.idempotencyKey?` | `string`                          | Optional idempotency key for safe retries. |

## Returns

`Promise`\<\{
`flowId`: `string`;
`message`: `string`;
}>

The result of the link email initiation.

