# SwapError
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Classes/SwapError



Error thrown when a swap operation fails with a known, actionable reason.

## Extends

* `Error`

## Constructors

### Constructor

```ts theme={null}
new SwapError(code: SwapErrorCode, message: string): SwapError;
```

Creates a new SwapError.

#### Parameters

| Parameter | Type                                                                                        | Description                                          |
| --------- | ------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| `code`    | [`SwapErrorCode`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SwapErrorCode) | The error code identifying the type of swap failure. |
| `message` | `string`                                                                                    | The error message.                                   |

#### Returns

`SwapError`

#### Overrides

```ts theme={null}
Error.constructor
```

## Properties

| Property     | Modifier | Type                                                                                        | Description                                          |
| ------------ | -------- | ------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| <a /> `code` | `public` | [`SwapErrorCode`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SwapErrorCode) | The error code identifying the type of swap failure. |

