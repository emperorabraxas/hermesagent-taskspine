# useCreateEvmSmartAccount
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useCreateEvmSmartAccount



```ts theme={null}
function useCreateEvmSmartAccount(): {
  createEvmSmartAccount: (options?: CreateEvmSmartAccountOptions) => Promise<`0x${string}`>;
};
```

A hook for creating a EVM Smart Account for the current user.
If no owner is provided, a new EOA will be created as the owner.
If an owner is provided, it must not already control another smart account for this user.

## Returns

An object containing the createSmartAccount function.

| Name                      | Type                                                                                                                                                                        |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `createEvmSmartAccount()` | (`options?`: [`CreateEvmSmartAccountOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/CreateEvmSmartAccountOptions)) => `Promise`\<`` `0x${string}` ``> |

## Example

```tsx theme={null}
import { useCreateEvmSmartAccount } from '@coinbase/cdp-hooks';

function MyComponent() {
  const { createEvmSmartAccount } = useCreateEvmSmartAccount();

  const handleCreateAccount = async () => {
    try {
      // Create with a new EOA owner
      const account = await createEvmSmartAccount({
        enableSpendPermissions: true
      });
      console.log('EVM Smart Account created:', account);

      // Or create with a specific owner
      const accountWithOwner = await createEvmSmartAccount({
        owner: '0x1234...',
        enableSpendPermissions: false
      });
    } catch (error) {
      console.error('Failed to create EVM Smart Account:', error);
    }
  };

  return <button onClick={handleCreateAccount}>Create EVM Smart Account</button>;
}
```

