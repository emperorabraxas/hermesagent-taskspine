# linkApple
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/linkApple



```ts theme={null}
function linkApple(options?: {
  idempotencyKey?: string;
}): Promise<void>;
```

Links an Apple account to the current user.

## Parameters

| Parameter                 | Type                              | Description                                |
| ------------------------- | --------------------------------- | ------------------------------------------ |
| `options?`                | \{ `idempotencyKey?`: `string`; } | Optional options for the link operation.   |
| `options.idempotencyKey?` | `string`                          | Optional idempotency key for safe retries. |

## Returns

`Promise`\<`void`>

The result of the link Apple initiation.

