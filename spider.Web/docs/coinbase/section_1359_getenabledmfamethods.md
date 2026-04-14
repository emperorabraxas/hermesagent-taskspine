# getEnabledMfaMethods
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/getEnabledMfaMethods



```ts theme={null}
function getEnabledMfaMethods(): MfaMethod[];
```

Gets the list of MFA methods enabled in the project configuration.

## Returns

[`MfaMethod`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/MfaMethod)\[]

An array of enabled MFA methods.

## Example

```typescript theme={null}
const config = getMfaConfigState();
if (config) {
  const methods = getEnabledMfaMethods(config);
  // methods = ['totp', 'sms']
}
```

