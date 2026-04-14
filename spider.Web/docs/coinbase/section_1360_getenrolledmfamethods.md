# getEnrolledMfaMethods
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/getEnrolledMfaMethods



```ts theme={null}
function getEnrolledMfaMethods(user: User): MfaMethod[];
```

Gets the list of MFA methods that the user has enrolled in.

## Parameters

| Parameter | Type                                                                      | Description      |
| --------- | ------------------------------------------------------------------------- | ---------------- |
| `user`    | [`User`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/User) | The user object. |

## Returns

[`MfaMethod`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/MfaMethod)\[]

An array of enrolled MFA methods ('totp', 'sms', or both).

## Example

```typescript theme={null}
const user = await getCurrentUser();
const methods = getEnrolledMfaMethods(user);
// methods = ['totp', 'sms']

if (methods.length > 1) {
  // Prompt user to choose which method to use
  const selectedMethod = await promptUser(methods);
  await initiateMfaVerification({ mfaMethod: selectedMethod });
}
```

