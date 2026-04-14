# useCancelMfaVerification
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useCancelMfaVerification



```ts theme={null}
function useCancelMfaVerification(): {
  cancelMfaVerification: () => void;
};
```

A hook for cancelling an in-progress MFA verification flow.

Call `cancelMfaVerification` when the user dismisses the MFA UI without
completing verification. This will reject the original operation that
triggered MFA with a "cancelled" error.

## Returns

An object containing the cancelMfaVerification function.

| Name                      | Type         |
| ------------------------- | ------------ |
| `cancelMfaVerification()` | () => `void` |

## Example

```tsx theme={null}
function MfaModal({ onClose }: { onClose: () => void }) {
  const { cancelMfaVerification } = useCancelMfaVerification();

  const handleCancel = () => {
    cancelMfaVerification();
    onClose();
  };

  return (
    <div>
      <h2>Enter your MFA code</h2>
      <button onClick={handleCancel}>Cancel</button>
    </div>
  );
}
```

