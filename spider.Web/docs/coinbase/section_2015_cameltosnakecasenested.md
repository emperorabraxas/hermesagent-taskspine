# CamelToSnakeCaseNested
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/CamelToSnakeCaseNested



```ts theme={null}
type CamelToSnakeCaseNested<T> = T extends readonly any[] ? T : T extends object ? { [K in keyof T as K extends string ? CamelToSnakeCase<K> : K]: CamelToSnakeCaseNested<T[K]> } : T;
```

Convert a camel case object to a snake case object

## Type Parameters

| Type Parameter |
| -------------- |
| `T`            |

