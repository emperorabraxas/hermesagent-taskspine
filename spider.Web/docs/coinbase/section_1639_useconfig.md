# useConfig
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useConfig



```ts theme={null}
function useConfig(): {
  config: Config;
};
```

Hook to get the CDP being used by the SDK.

## Returns

```ts theme={null}
{
  config: Config;
}
```

| Name     | Type     |
| -------- | -------- |
| `config` | `Config` |

## Example

```tsx lines theme={null}
function App() {
  const { config } = useConfig();

  return (
    <div>
      <p>Project ID: {config.projectId}</p>
    </div>
  );
}
```

