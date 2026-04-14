# CDPReactProvider
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/CDPReactProvider



```ts theme={null}
function CDPReactProvider(props: CDPReactProviderProps): Element;
```

CDPReactProvider component.

## Parameters

| Parameter | Type                                                                                                       | Description                              |
| --------- | ---------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| `props`   | [`CDPReactProviderProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/CDPReactProviderProps) | Props for the CDPReactProvider component |

## Returns

`Element`

The CDPReactProvider component

## Example

```tsx lines theme={null}
function App() {
  return (
    <CDPReactProvider config={config} theme={themeOverrides}>
      <YourApp />
    </CDPReactProvider>
  );
}
```

