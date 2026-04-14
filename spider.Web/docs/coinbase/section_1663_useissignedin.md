# useIsSignedIn
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useIsSignedIn



```ts theme={null}
function useIsSignedIn(): {
  isSignedIn: boolean;
};
```

Hook to check if a user is currently signed in.
Use this to gate authenticated-only features in your application.

## Returns

```ts theme={null}
{
  isSignedIn: boolean;
}
```

| Name         | Type      |
| ------------ | --------- |
| `isSignedIn` | `boolean` |

## Example

```tsx lines theme={null}
function AuthGuard({ children }) {
  const { isSignedIn } = useIsSignedIn();

  if (!isSignedIn) {
    return <Navigate to="/sign-in" />;
  }

  return children;
}
```

