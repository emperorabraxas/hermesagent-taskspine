# Flattened
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/Flattened



```ts theme={null}
type Flattened<T> = { [K in KebabCasePaths<T>]: string };
```

A flattened representation of the Tokens type, where keys are
kebab-cased paths and all values are strings.

## Type Parameters

| Type Parameter                               |
| -------------------------------------------- |
| `T` *extends* `Record`\<`string`, `unknown`> |

## Example

```ts theme={null}
const themeOverrides: Partial<Flattened<typeof tokens>> = {
  'colors-brand-primary': string;
  'fontFamily-sans': string;
}
```

