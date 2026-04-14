# useSignInWithSms
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useSignInWithSms



```ts theme={null}
function useSignInWithSms(): {
  signInWithSms: (options: SignInWithSmsOptions) => Promise<SignInWithSmsResult>;
};
```

Hook that provides access to the SMS-based sign-in functionality.
This is the first step in the SMS authentication flow.

## Returns

```ts theme={null}
{
  signInWithSms: (options: SignInWithSmsOptions) => Promise<SignInWithSmsResult>;
}
```

| Name              | Type                                                                     |
| ----------------- | ------------------------------------------------------------------------ |
| `signInWithSms()` | (`options`: `SignInWithSmsOptions`) => `Promise`\<`SignInWithSmsResult`> |

## Example

```tsx lines theme={null}
function SignInForm() {
  const [phoneNumber, setPhoneNumber] = useState("");
  const [flowId, setFlowId] = useState("");
  const { signInWithSms } = useSignInWithSms();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const result = await signInWithSms({ phoneNumber });
      setFlowId(result.flowId);
    } catch (error) {
      console.error("Failed to sign in:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="tel"
        value={phoneNumber}
        onChange={(e) => setPhoneNumber(e.target.value)}
        placeholder="Enter your phone number"
        aria-label="Enter your phone number"
      />
      <button type="submit">Sign In</button>
    </form>
  );
}
```

