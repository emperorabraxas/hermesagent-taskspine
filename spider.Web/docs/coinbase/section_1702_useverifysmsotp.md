# useVerifySmsOTP
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useVerifySmsOTP



```ts theme={null}
function useVerifySmsOTP(): {
  verifySmsOTP: (options: VerifySmsOTPOptions) => Promise<VerifySmsOTPResult>;
};
```

Hook that provides access to the SMS OTP verification functionality.
This is the second step in the SMS authentication flow, used after signInWithSms.

## Returns

```ts theme={null}
{
  verifySmsOTP: (options: VerifySmsOTPOptions) => Promise<VerifySmsOTPResult>;
}
```

| Name             | Type                                                                   |
| ---------------- | ---------------------------------------------------------------------- |
| `verifySmsOTP()` | (`options`: `VerifySmsOTPOptions`) => `Promise`\<`VerifySmsOTPResult`> |

## Example

```tsx lines theme={null}
function OTPVerification(flowId: string) {
  const [otp, setOTP] = useState("");
  const { verifySmsOTP } = useVerifySmsOTP();

  const otpIsValid = useMemo(() => {
    // Check if the OTP is a 6 digit number
    return /^[0-9]{6}$/.test(otp);
  }, [otp]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const { user } = await verifySmsOTP({
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
        placeholder="Enter OTP from SMS"
        aria-label="Enter OTP from SMS"
      />
      <button type="submit" disabled={!otpIsValid}>Verify OTP</button>
    </form>
  );
}
```

