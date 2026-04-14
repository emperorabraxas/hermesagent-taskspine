# useRegisterMfaListener
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useRegisterMfaListener



```ts theme={null}
function useRegisterMfaListener(onMfaRequired: MfaRequiredCallback, options?: UseRegisterMfaListenerOptions): void;
```

Hook to register a listener for MFA verification requirements.

When a sensitive operation (like signing a transaction) requires MFA verification,
the `onMfaRequired` callback will be invoked. The consumer should show their custom
MFA UI and use `useInitiateMfaVerification` and `useSubmitMfaVerification` to
complete the verification flow.

After successful MFA verification, the original operation will automatically continue.

## Parameters

| Parameter       | Type                                                                                                                       | Description                                         |
| --------------- | -------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| `onMfaRequired` | [`MfaRequiredCallback`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/MfaRequiredCallback)                   | Callback invoked when MFA verification is required. |
| `options?`      | [`UseRegisterMfaListenerOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Interfaces/UseRegisterMfaListenerOptions) | Optional configuration including scope element.     |

## Returns

`void`

## Example

```tsx theme={null}
// In this example, MfaModal would implement the MFA verification flow using
// useInitiateMfaVerification and useSubmitMfaVerification hooks
function App() {
  const [showMfaModal, setShowMfaModal] = useState(false);
  const [mfaMethods, setMfaMethods] = useState<MfaMethod[]>([]);
  const { cancelMfaVerification } = useCancelMfaVerification();

  useRegisterMfaListener(({ methods }) => {
    setMfaMethods(methods);
    setShowMfaModal(true);
  });

  const handleClose = () => {
    cancelMfaVerification();
    setShowMfaModal(false);
  };

  return (
    <>
      <YourApp />
      <MfaModal
        methods={mfaMethods}
        isOpen={showMfaModal}
        onClose={handleClose}
      />
    </>
  );
}
```

