# useEvmSmartAccounts
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useEvmSmartAccounts



```ts theme={null}
function useEvmSmartAccounts(): {
  evmSmartAccounts:   | null
     | EndUserEvmSmartAccount[];
};
```

Hook to access all EVM smart account objects for the current user.
Returns an array of smart account objects with address, owner addresses, and creation timestamp.
Each EVM EOA can own one smart account.

## Returns

```ts theme={null}
{
  evmSmartAccounts:   | null
     | EndUserEvmSmartAccount[];
}
```

| Name               | Type                                                                                                                        |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| `evmSmartAccounts` | \| `null` \| [`EndUserEvmSmartAccount`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/EndUserEvmSmartAccount)\[] |

## Example

```tsx lines theme={null}
function SmartAccountsList() {
  const { evmSmartAccounts } = useEvmSmartAccounts();

  if (!evmSmartAccounts || evmSmartAccounts.length === 0) {
    return <p>No smart accounts found</p>;
  }

  return (
    <div>
      <h3>Your Smart Accounts</h3>
      <ul>
        {evmSmartAccounts.map((account, index) => (
          <li key={account.address}>
            Smart Account {index + 1}: {account.address}
            <br />
            Owners: {account.ownerAddresses.join(', ')}
            <br />
            Created: {new Date(account.createdAt).toLocaleDateString()}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

