# useCurrentUser
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useCurrentUser



```ts theme={null}
function useCurrentUser(): {
  currentUser:   | null
     | User;
};
```

Hook to access the currently authenticated user's information.

## Returns

```ts theme={null}
{
  currentUser:   | null
     | User;
}
```

| Name          | Type                                                                                    |
| ------------- | --------------------------------------------------------------------------------------- |
| `currentUser` | \| `null` \| [`User`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/User) |

## Example

```tsx lines theme={null}
function UserProfile() {
  const { currentUser } = useCurrentUser();

  if (!currentUser) {
    return null;
  }

  return (
    <div>
      <h2>User Profile</h2>
      <p>User ID: {currentUser.userId}</p>
      <p>EVM Accounts: {currentUser.evmAccountObjects.map(acc => acc.address).join(", ")}</p>
    </div>
  );
}
```

