# cancelMfaVerification
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Functions/cancelMfaVerification



```ts theme={null}
function cancelMfaVerification(): void;
```

Cancels the current MFA verification flow.

Call this when the user dismisses the MFA UI without completing verification.
The original operation that triggered MFA will reject with an error.

## Returns

`void`

## Example

```typescript theme={null}
// In your MFA modal's cancel button handler
function MfaModal() {
  const handleCancel = () => {
    cancelMfaVerification();
    closeModal();
  };

  return <button onClick={handleCancel}>Cancel</button>;
}
```

