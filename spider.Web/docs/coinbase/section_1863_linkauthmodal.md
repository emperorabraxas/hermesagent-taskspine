# LinkAuthModal
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/LinkAuthModal



```ts theme={null}
function LinkAuthModal(props: LinkAuthModalProps): Element;
```

A link auth modal component that wraps the [LinkAuth](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/LinkAuth) component.

## Parameters

| Parameter | Type                                                                                                 | Description                                |
| --------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| `props`   | [`LinkAuthModalProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/LinkAuthModalProps) | The props for the LinkAuthModal component. |

## Returns

`Element`

The LinkAuthModal component.

## See

* [LinkAuthModalTrigger](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/LinkAuthModalTrigger) for the trigger button.
* [LinkAuthModalContent](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/LinkAuthModalContent) for the modal content.

## Examples

```tsx lines theme={null}
// Render the LinkAuthModal component with a custom success handler
function App() {
  const handleLinkSuccess = (method: string) => {
    console.log(`Successfully linked ${method}`);
  };

  return (
    <CDPReactProvider config={config}>
      <LinkAuthModal onLinkSuccess={handleLinkSuccess} />
    </CDPReactProvider>
  );
}
```

```tsx lines theme={null}
// Render the LinkAuthModal component with a custom trigger button
function App() {
  return (
    <CDPReactProvider config={config}>
      <LinkAuthModal>
        <button type="button">Manage linked accounts</button>
      </LinkAuthModal>
    </CDPReactProvider>
  );
}
```

```tsx lines theme={null}
// Render the LinkAuthModal component with a custom trigger button label
function App() {
  return (
    <CDPReactProvider config={config}>
      <LinkAuthModal>
        <LinkAuthModalTrigger variant="secondary" label="Link more accounts" />
      </LinkAuthModal>
    </CDPReactProvider>
  );
}
```

```tsx lines theme={null}
// Render the LinkAuthModal with controlled open state
function App() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <CDPReactProvider config={config}>
      <LinkAuthModal open={isOpen} setIsOpen={setIsOpen}>
        <LinkAuthModalTrigger />
        <LinkAuthModalContent />
      </LinkAuthModal>
    </CDPReactProvider>
  );
}
```

