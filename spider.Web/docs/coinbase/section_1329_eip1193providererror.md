# EIP1193ProviderError
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Classes/EIP1193ProviderError



EIP-1193 provider error.

## Extends

* `Error`

## Constructors

### Constructor

```ts theme={null}
new EIP1193ProviderError(code: EIP1193ErrorCode, message: string): EIP1193ProviderError;
```

Creates a new EIP-1193 Provider error.

#### Parameters

| Parameter | Type                                                                                              | Description                                |
| --------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| `code`    | [`EIP1193ErrorCode`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EIP1193ErrorCode) | The error code from EIP1193ErrorCode enum. |
| `message` | `string`                                                                                          | The error message.                         |

#### Returns

`EIP1193ProviderError`

#### Overrides

```ts theme={null}
Error.constructor
```

## Properties

| Property     | Modifier | Type                                                                                              | Description                                |
| ------------ | -------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| <a /> `code` | `public` | [`EIP1193ErrorCode`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EIP1193ErrorCode) | The error code from EIP1193ErrorCode enum. |

