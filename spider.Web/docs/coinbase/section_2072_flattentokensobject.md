# flattenTokensObject
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Utilities/flattenTokensObject



```ts theme={null}
function flattenTokensObject<T>(tokensObject: T, cssVarPrefix?: string): Flattened<T>;
```

Flattens a nested theme object into a single-level object with CSS variable representations.

## Type Parameters

| Type Parameter                                                                                                     |
| ------------------------------------------------------------------------------------------------------------------ |
| `T` *extends* [`NestedTokenObject`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/NestedTokenObject) |

## Parameters

| Parameter       | Type     | Default value | Description                                         |
| --------------- | -------- | ------------- | --------------------------------------------------- |
| `tokensObject`  | `T`      | `undefined`   | The nested tokens object to flatten.                |
| `cssVarPrefix?` | `string` | `"cdp-web"`   | An optional prefix for the generated CSS variables. |

## Returns

[`Flattened`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/Flattened)\<`T`>

A flattened theme object.

