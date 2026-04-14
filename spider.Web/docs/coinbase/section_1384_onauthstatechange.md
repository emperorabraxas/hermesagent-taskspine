# onAuthStateChange
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/onAuthStateChange



```ts theme={null}
function onAuthStateChange(callback: OnAuthStateChangeFn): void;
```

Sets a callback function to be called when the authentication state changes,
i.e. when a user signs in or out.

## Parameters

| Parameter  | Type                                                                                                    | Description                                                               |
| ---------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `callback` | [`OnAuthStateChangeFn`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/OnAuthStateChangeFn) | The callback function to be called when the authentication state changes. |

## Returns

`void`

## Example

```typescript lines theme={null}
onAuthStateChange(async (user) => {
  if (user) {
    console.log("User signed in:", user.userId);
  } else {
    console.log("User signed out");
  }
});
```

