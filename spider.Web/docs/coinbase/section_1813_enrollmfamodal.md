# EnrollMfaModal
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/EnrollMfaModal



```ts theme={null}
function EnrollMfaModal(props: EnrollMfaModalProps): Element;
```

A enroll MFA modal component that wraps the [EnrollMfa](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/EnrollMfa) component.

## Parameters

| Parameter | Type                                                                                                   | Description                                 |
| --------- | ------------------------------------------------------------------------------------------------------ | ------------------------------------------- |
| `props`   | [`EnrollMfaModalProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/EnrollMfaModalProps) | The props for the EnrollMfaModal component. |

## Returns

`Element`

The EnrollMfaModal component.

## See

* [EnrollMfaModalTrigger](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/EnrollMfaModalTrigger) for the trigger button.
* [EnrollMfaModalContent](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/EnrollMfaModalContent) for the modal content.

## Examples

```tsx lines theme={null}
// Render the EnrollMfaModal component with a custom success handler
function App() {
  const handleSuccess = (mfaCode: string) => {
    console.log(`Successfully verified`, mfaCode);
  };

  return (
    <CDPReactProvider config={config}>
      <EnrollMfaModal onSuccess={handleSuccess} />
    </CDPReactProvider>
  );
}
```

```tsx lines theme={null}
// Render the EnrollMfaModal component with a custom trigger button
function App() {
  return (
    <CDPReactProvider config={config}>
      <EnrollMfaModal>
        <button type="button">Verify</button>
      </EnrollMfaModal>
    </CDPReactProvider>
  );
}
```

```tsx lines theme={null}
// Render the EnrollMfaModal component with a custom trigger button label
function App() {
  return (
    <CDPReactProvider config={config}>
      <EnrollMfaModal>
        <EnrollMfaModalTrigger variant="secondary" label="Verify" />
      </EnrollMfaModal>
    </CDPReactProvider>
  );
}
```

```tsx lines theme={null}
// Render the EnrollMfaModal with controlled open state
function App() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <CDPReactProvider config={config}>
      <EnrollMfaModal open={isOpen} setIsOpen={setIsOpen}>
        <EnrollMfaModalTrigger />
        <EnrollMfaModalContent />
      </EnrollMfaModal>
    </CDPReactProvider>
  );
}
```

