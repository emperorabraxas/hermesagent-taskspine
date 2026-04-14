# MfaError
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Classes/MfaError



Error thrown when an MFA operation fails.

## Extends

* `Error`

## Constructors

### Constructor

```ts theme={null}
new MfaError(code: MfaErrorCode, message: string): MfaError;
```

Creates a new MfaError.

#### Parameters

| Parameter | Type                                                                                      | Description                                       |
| --------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------- |
| `code`    | [`MfaErrorCode`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/MfaErrorCode) | The error code identifying the type of MFA error. |
| `message` | `string`                                                                                  | The error message.                                |

#### Returns

`MfaError`

#### Overrides

```ts theme={null}
Error.constructor
```

## Properties

| Property     | Modifier | Type                                                                                      | Description                                       |
| ------------ | -------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------- |
| <a /> `code` | `public` | [`MfaErrorCode`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/MfaErrorCode) | The error code identifying the type of MFA error. |

