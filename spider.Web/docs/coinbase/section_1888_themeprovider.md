# ThemeProvider
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/ThemeProvider



```ts theme={null}
function ThemeProvider(props: ThemeProviderProps): Element;
```

Provides the theme to its child components and injects CSS variables.

## Parameters

| Parameter | Type                                                                                                   | Description                  |
| --------- | ------------------------------------------------------------------------------------------------------ | ---------------------------- |
| `props`   | [`ThemeProviderProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/ThemeProviderProps) | The props for the component. |

## Returns

`Element`

The theme provider component.

## See

[useTheme](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Hooks/useTheme)

## Example

```tsx lines theme={null}
const AuthBasedTheme = ({ children }: { children: React.ReactNode }) => {
  const { isSignedIn: signedIn } = useIsSignedIn();
  const { evmAddress: cdpEvmAddress } = useEvmAddress();
  const isAuthenticated = signedIn && cdpEvmAddress;
  const theme = useMemo(() => (isAuthenticated ? darkTheme : {}), [isAuthenticated]);
  return (
    <ThemeProvider theme={theme}>
      {children}
    </ThemeProvider>
  );
};

function App() {
  // Change the theme based on the user's authentication status
  return (
    <CDPHooksProvider config={cdpConfig}>
      <AuthBasedTheme>
        <YourApp />
      </AuthBasedTheme>
    </CDPHooksProvider>
  );
}
```

