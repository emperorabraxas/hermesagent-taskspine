# onOAuthStateChange
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/onOAuthStateChange



```ts theme={null}
function onOAuthStateChange(callback: OnOAuthStateChangeFn): void;
```

Sets a callback function to be called when the OAuth flow state changes,
i.e. when a user signs in with OAuth.

## Parameters

| Parameter  | Type                                                                                                      | Description                                                           |
| ---------- | --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| `callback` | [`OnOAuthStateChangeFn`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/OnOAuthStateChangeFn) | The callback function to be called when the OAuth flow state changes. |

## Returns

`void`

