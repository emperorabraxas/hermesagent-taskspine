# useIsInitialized
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useIsInitialized



```ts theme={null}
function useIsInitialized(): {
  isInitialized: boolean;
};
```

Hook to check if the CDP client has been properly initialized.
This should be used before attempting any CDP operations to ensure the client is ready.

## Returns

```ts theme={null}
{
  isInitialized: boolean;
}
```

| Name            | Type      |
| --------------- | --------- |
| `isInitialized` | `boolean` |

## Example

```tsx lines theme={null}
function LoadingGuard({ children }) {
  const { isInitialized } = useIsInitialized();

  if (!isInitialized) {
    return <div>Loading...</div>;
  }

  return children;
}
```

