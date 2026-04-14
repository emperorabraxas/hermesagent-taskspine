# useEvmAccounts
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useEvmAccounts



```ts theme={null}
function useEvmAccounts(): {
  evmAccounts:   | null
     | EndUserEvmAccount[];
};
```

Hook to access all EVM account objects for the current user.
Returns an array of account objects with address and creation timestamp.
Users can have up to 10 EVM accounts.

## Returns

```ts theme={null}
{
  evmAccounts:   | null
     | EndUserEvmAccount[];
}
```

| Name          | Type                                                                                                              |
| ------------- | ----------------------------------------------------------------------------------------------------------------- |
| `evmAccounts` | \| `null` \| [`EndUserEvmAccount`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/EndUserEvmAccount)\[] |

## Example

```tsx lines theme={null}
function EVMAccountsList() {
  const { evmAccounts } = useEvmAccounts();

  if (!evmAccounts || evmAccounts.length === 0) {
    return <p>No EVM accounts found</p>;
  }

  return (
    <div>
      <h3>Your EVM Accounts</h3>
      <ul>
        {evmAccounts.map((account, index) => (
          <li key={account.address}>
            Account {index + 1}: {account.address}
            <br />
            Created: {new Date(account.createdAt).toLocaleDateString()}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

