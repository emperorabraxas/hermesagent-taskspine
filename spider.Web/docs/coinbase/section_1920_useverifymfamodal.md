# useVerifyMfaModal
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Hooks/useVerifyMfaModal



```ts theme={null}
function useVerifyMfaModal(options: UseVerifyMfaModalOptions): UseVerifyMfaModalReturn;
```

Hook to imperatively control the MFA verification modal.

This hook allows you to open and close the MFA verification modal programmatically,
which is useful for integrating MFA verification into complex flows without using
the `<VerifyMfaModal />` component pattern.

## Parameters

| Parameter | Type                                                                                                             | Description                                   |
| --------- | ---------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| `options` | [`UseVerifyMfaModalOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/UseVerifyMfaModalOptions) | The options for the hook including callbacks. |

## Returns

[`UseVerifyMfaModalReturn`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/UseVerifyMfaModalReturn)

An object containing `open` and `close` functions.

## Example

```tsx lines theme={null}
function ProtectedAction() {
  const { open } = useVerifyMfaModal({
    onSuccess: () => performSensitiveAction(),
    onError: (error) => console.error("MFA verification failed:", error),
    onCancel: () => console.log("MFA verification cancelled"),
  });

  const handleClick = () => {
    const opened = open(); // Returns false if modal is already open
    if (!opened) {
      console.log("MFA modal is already open");
    }
  };

  return (
    <button onClick={handleClick}>
      Perform sensitive action
    </button>
  );
}
```

