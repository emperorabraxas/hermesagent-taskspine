# isEmailInvalid
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Utilities/isEmailInvalid



```ts theme={null}
function isEmailInvalid(value: string): boolean;
```

Check if an email address is invalid.

## Parameters

| Parameter | Type     | Description                    |
| --------- | -------- | ------------------------------ |
| `value`   | `string` | The email address to validate. |

## Returns

`boolean`

`true` if the email address is invalid, `false` otherwise.

## Example

```tsx lines theme={null}
if (isEmailInvalid("test@example")) {
  console.log("Invalid email address");
}
```

