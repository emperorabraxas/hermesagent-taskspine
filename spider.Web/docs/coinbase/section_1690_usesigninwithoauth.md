# useSignInWithOAuth
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useSignInWithOAuth



```ts theme={null}
function useSignInWithOAuth(): {
  signInWithOAuth: (providerType: OAuth2ProviderType, options?: {
     idempotencyKey?: string;
  }) => Promise<void>;
  oauthState:   | null
     | OAuthFlowState;
};
```

Hook that provides access to the OAuth sign-in functionality (Google, Apple, and X are currently supported).
This is the first step in the OAuth authentication flow.
In a web application, this will redirect the user to the OAuth provider sign in page.
This sign in method is not yet supported on mobile.

## Returns

```ts theme={null}
{
  signInWithOAuth: (providerType: OAuth2ProviderType, options?: {
     idempotencyKey?: string;
  }) => Promise<void>;
  oauthState:   | null
     | OAuthFlowState;
}
```

| Name                | Type                                                                                                                                                                                          |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `signInWithOAuth()` | (`providerType`: [`OAuth2ProviderType`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/OAuth2ProviderType), `options?`: \{ `idempotencyKey?`: `string`; }) => `Promise`\<`void`> |
| `oauthState`        | \| `null` \| [`OAuthFlowState`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Interfaces/OAuthFlowState)                                                                                     |

## Examples

```tsx lines theme={null}
// Google
function SignInForm() {
  const { signInWithOAuth } = useSignInWithOAuth();

  const handleSignInWithGoogle = () => {
    void signInWithOAuth("google");
  };

  return (
    <button onClick={handleSignInWithGoogle}>
      Sign in with Google
    </button>
  );
}
```

```tsx lines theme={null}
// Apple
function SignInForm() {
  const { signInWithOAuth } = useSignInWithOAuth();

  const handleSignInWithApple = () => {
    void signInWithOAuth("apple");
  };

  return (
    <button onClick={handleSignInWithApple}>
      Sign in with Apple
    </button>
  );
}
```

```tsx lines theme={null}
// X
function SignInForm() {
  const { signInWithOAuth } = useSignInWithOAuth();

  const handleSignInWithX = () => {
    void signInWithOAuth("x");
  };

  return (
    <button onClick={handleSignInWithX}>
      Sign in with X
    </button>
  );
}
```

