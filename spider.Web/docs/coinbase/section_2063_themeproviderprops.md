# ThemeProviderProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/ThemeProviderProps



```ts theme={null}
type ThemeProviderProps = {
  theme?: Partial<Theme>;
  data-cdp-provider?: string;
} & HTMLAttributes<HTMLDivElement>;
```

Props for the ThemeProvider component.

## Type declaration

| Name                 | Type                                                                                     | Description                                                                                                                                                                                   |
| -------------------- | ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `theme?`             | `Partial`\<[`Theme`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/Theme)> | Theme overrides                                                                                                                                                                               |
| `data-cdp-provider?` | `string`                                                                                 | Provider name for multi-provider coordination. Used internally by CDPReactProvider to identify which provider owns focused elements. If not provided, a unique ID is generated automatically. |

## See

[ThemeProvider](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/ThemeProvider)

