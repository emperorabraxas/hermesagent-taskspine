# getMfaConfig
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/getMfaConfig



```ts theme={null}
function getMfaConfig(): Promise<MfaConfig>;
```

Gets the MFA configuration for the current project.
This endpoint returns information about whether MFA is enabled for the project
and the configuration for TOTP authentication.

## Returns

`Promise`\<`MfaConfig`>

The MFA configuration for the project.

## Example

```typescript lines theme={null}
const result = await getMfaConfig();
if (result?.totpConfig?.enabled) {
  console.log("TOTP MFA is enabled for this project");
}
```

