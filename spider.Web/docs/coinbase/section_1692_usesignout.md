# useSignOut
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useSignOut



```ts theme={null}
function useSignOut(): {
  signOut: () => Promise<void>;
};
```

Hook that provides a wrapped sign-out function with authentication checks.
This hook uses useEnforceAuthenticated to ensure the user is signed in before attempting to sign out.

## Returns

```ts theme={null}
{
  signOut: () => Promise<void>;
}
```

| Name        | Type                     |
| ----------- | ------------------------ |
| `signOut()` | () => `Promise`\<`void`> |

## Example

```tsx lines theme={null}
function SignOutButton() {
  const { signOut } = useSignOut();
  const navigate = useNavigate();

  const handleSignOut = async () => {
    try {
      await signOut();
      navigate("/sign-in");
    } catch (error) {
      console.error("Failed to sign out:", error);
    }
  };

  return (
    <button onClick={handleSignOut}>
      Sign Out
    </button>
  );
}
```

