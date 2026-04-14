# useAppConfig
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Hooks/useAppConfig



```ts theme={null}
function useAppConfig(): Required<AppConfig>;
```

Hook to access the app config from a component.

## Returns

`Required`\<[`AppConfig`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/AppConfig)>

The app config.

## Example

```tsx lines theme={null}
const MyComponent = () => {
  // Access the app config from a child component
  const appConfig = useAppConfig();
  return <div>{appConfig.appName}</div>;
}

function App() {
  return (
    <CDPReactProvider config={config}>
      <MyComponent />
    </CDPReactProvider>
  );
}
```

