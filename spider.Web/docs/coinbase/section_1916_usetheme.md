# useTheme
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Hooks/useTheme



```ts theme={null}
function useTheme(): ThemeContextValue;
```

Hook to access the theme from a component.

## Returns

[`ThemeContextValue`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/ThemeContextValue)

The theme.

## See

[ThemeProvider](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/ThemeProvider)

## Example

```tsx lines theme={null}
function App() {
  // Style a paragraph with the secondary text color
  const { theme } = useTheme();
  return <p style={{ color: theme["colors-fg-muted"] }}>Secondary text</p>;
}
```

