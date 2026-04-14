# useProviderName
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Hooks/useProviderName



```ts theme={null}
function useProviderName(): string;
```

Hook to access the provider name from a component.

## Returns

`string`

The provider name.

## Example

```tsx lines theme={null}
const MyComponent = () => {
  const providerName = useProviderName();
  return <div>{providerName}</div>;
}

function App() {
  return (
    <CDPReactProvider name="provider-instance" config={config}>
      <MyComponent />
    </CDPReactProvider>
  );
}
```

