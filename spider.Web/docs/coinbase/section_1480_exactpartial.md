# ExactPartial
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/ExactPartial



```ts theme={null}
type ExactPartial<T> = { [P in keyof T]?: T[P] extends object ? ExactPartial<T[P]> : T[P] };
```

A type that makes all properties of an object optional.

## Type Parameters

| Type Parameter | Description               |
| -------------- | ------------------------- |
| `T`            | The type to make partial. |

## Returns

The partial type.

