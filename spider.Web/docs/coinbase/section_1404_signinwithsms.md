# signInWithSms
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/signInWithSms



```ts theme={null}
function signInWithSms(options: SignInWithSmsOptions): Promise<SignInWithSmsResult>;
```

Initiates the sign in flow with a phone number via SMS.

## Parameters

| Parameter | Type                                                                                                      | Description                  |
| --------- | --------------------------------------------------------------------------------------------------------- | ---------------------------- |
| `options` | [`SignInWithSmsOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SignInWithSmsOptions) | The options for the sign in. |

## Returns

`Promise`\<[`SignInWithSmsResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SignInWithSmsResult)>

The result of the sign in.

## Example

```typescript lines theme={null}
const result = await signInWithSms({
  phoneNumber: "+14155552671"
});
```

