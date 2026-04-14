# useCreateSolanaAccount
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useCreateSolanaAccount



```ts theme={null}
function useCreateSolanaAccount(): {
  createSolanaAccount: (options?: CreateSolanaAccountOptions) => Promise<string>;
};
```

A hook for creating a Solana account for the current user.
This function will throw an error if the user already has a Solana account.

## Returns

An object containing the createSolanaAccount function.

| Name                    | Type                                                               |
| ----------------------- | ------------------------------------------------------------------ |
| `createSolanaAccount()` | (`options?`: `CreateSolanaAccountOptions`) => `Promise`\<`string`> |

## Example

```tsx theme={null}
import { useCreateSolanaAccount } from '@coinbase/cdp-hooks';

function MyComponent() {
  const { createSolanaAccount } = useCreateSolanaAccount();

  const handleCreateAccount = async () => {
    try {
      const account = await createSolanaAccount();
      console.log('Solana account created:', account);
    } catch (error) {
      console.error('Failed to create Solana account:', error);
    }
  };

  return <button onClick={handleCreateAccount}>Create Solana Account</button>;
}
```

