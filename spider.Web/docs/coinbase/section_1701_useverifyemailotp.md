# useVerifyEmailOTP
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useVerifyEmailOTP



```ts theme={null}
function useVerifyEmailOTP(): {
  verifyEmailOTP: (options: VerifyEmailOTPOptions) => Promise<VerifyEmailOTPResult>;
};
```

Hook that provides access to the email OTP verification functionality.
This is the second step in the email authentication flow, used after signInWithEmail.

## Returns

```ts theme={null}
{
  verifyEmailOTP: (options: VerifyEmailOTPOptions) => Promise<VerifyEmailOTPResult>;
}
```

| Name               | Type                                                                                                                                                                                                                                                |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `verifyEmailOTP()` | (`options`: [`VerifyEmailOTPOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/VerifyEmailOTPOptions)) => `Promise`\<[`VerifyEmailOTPResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/VerifyEmailOTPResult)> |

## Example

```tsx lines theme={null}
function OTPVerification(flowId: string) {
  const [otp, setOTP] = useState("");
  const { verifyEmailOTP } = useVerifyEmailOTP();

  const otpIsValid = useMemo(() => {
    // Check if the OTP is a 6 digit number
    return /^[0-9]{6}$/.test(otp);
  }, [otp]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const { user } = await verifyEmailOTP({
        flowId,
        otp
      });

      // Handle the result
      console.log(user);
    } catch (error) {
      console.error("Failed to verify OTP:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={otp}
        onChange={(e) => setOTP(e.target.value)}
        placeholder="Enter OTP from email"
        aria-label="Enter OTP from email"
      />
      <button type="submit" disabled={!otpIsValid}>Verify OTP</button>
    </form>
  );
}
```

