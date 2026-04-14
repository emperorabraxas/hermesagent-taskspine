# useSignInWithEmail
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useSignInWithEmail



```ts theme={null}
function useSignInWithEmail(): {
  signInWithEmail: (options: SignInWithEmailOptions) => Promise<SignInWithEmailResult>;
};
```

Hook that provides access to the email-based sign-in functionality.
This is the first step in the email authentication flow.

## Returns

```ts theme={null}
{
  signInWithEmail: (options: SignInWithEmailOptions) => Promise<SignInWithEmailResult>;
}
```

| Name                | Type                                                                                                                                                                                                                                                    |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `signInWithEmail()` | (`options`: [`SignInWithEmailOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/SignInWithEmailOptions)) => `Promise`\<[`SignInWithEmailResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/SignInWithEmailResult)> |

## Example

```tsx lines theme={null}
function SignInForm() {
  const [email, setEmail] = useState("");
  const [flowId, setFlowId] = useState("");
  const { signInWithEmail } = useSignInWithEmail();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const result = await signInWithEmail({ email });
      setFlowId(result.flowId);
    } catch (error) {
      console.error("Failed to sign in:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Enter your email"
        aria-label="Enter your email"
      />
      <button type="submit">Sign In</button>
    </form>
  );
}
```

