# CamelToSnakeCase
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/CamelToSnakeCase



```ts theme={null}
type CamelToSnakeCase<T> = T extends `${infer A}${infer B}` ? B extends Uncapitalize<B> ? `${A}${CamelToSnakeCase<B>}` : `${Uncapitalize<A>}_${CamelToSnakeCase<Uncapitalize<B>>}` : T;
```

Convert a camel case string to a snake case string

## Type Parameters

| Type Parameter         |
| ---------------------- |
| `T` *extends* `string` |

