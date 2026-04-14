# LinkAuth
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/LinkAuth



```ts theme={null}
function LinkAuth(props: LinkAuthProps): Element;
```

A component for managing linked authentication methods for the current user.

This component displays a list of available authentication methods (email, phone, OAuth providers)
and allows users to link or unlink them from their account.

## Parameters

| Parameter | Type                                                                                       | Description                  |
| --------- | ------------------------------------------------------------------------------------------ | ---------------------------- |
| `props`   | [`LinkAuthProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/LinkAuthProps) | The props for the component. |

## Returns

`Element`

The LinkAuth component.

## See

* [LinkAuthError](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/LinkAuthError)
* [LinkAuthFlow](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/LinkAuthFlow)
* [LinkAuthFlowBackButton](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/LinkAuthFlowBackButton)
* [LinkAuthItem](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/LinkAuthItem)
* [LinkAuthItems](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/LinkAuthItems)
* [LinkAuthTitle](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/LinkAuthTitle)
* [useLinkAuthContext](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Hooks/useLinkAuthContext)
* [useLinkAuthFlow](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Hooks/useLinkAuthFlow)

## Examples

```tsx lines theme={null}
// Render the LinkAuth component with a custom success handler

function App() {
  return (
    <CDPReactProvider config={config}>
      <LinkAuth onLinkSuccess={method => console.log(`Linked ${method}`)} />
    </CDPReactProvider>
  );
}
```

```tsx lines theme={null}
// Recreate the default UI

function App() {
  return (
    <CDPReactProvider config={config}>
      <LinkAuth>
        <div className="header">
          <LinkAuthTitle />
          <LinkAuthFlowBackButton />
        </div>
        <div className="error">
          <LinkAuthError />
        </div>
        <LinkAuthFlow />
      </LinkAuth>
    </CDPReactProvider>
  );
}
```

```tsx lines theme={null}
// Add a message based on the LinkAuth state

function App() {
  return (
    <CDPReactProvider config={config}>
      <LinkAuth>
        {state => (
          <>
            <div className="header">
              <LinkAuthTitle />
              <LinkAuthFlowBackButton />
            </div>
            {state.methodToLink && (
              <p className="message">
                Linking {state.methodToLink}...
              </p>
            )}
            <div className="error">
              <LinkAuthError />
            </div>
            <LinkAuthFlow />
          </>
        )}
      </LinkAuth>
    </CDPReactProvider>
  );
}
```

```tsx lines theme={null}
// Customize LinkAuthItems to show a modal for non-OAuth methods instead of transitioning in place.

function CustomLinkAuthItems() {
  const { link, back } = useLinkAuthFlow();
  const { authMethods } = useAppConfig();
  const [openModal, setOpenModal] = useState<AuthMethod | null>(null);

  const modalMethods = useMemo(
    () => authMethods.filter(method => !method.startsWith("oauth:")),
    [authMethods],
  );

  const handleClose = useCallback(() => {
    setOpenModal(null);
    back();
  }, [back, setOpenModal]);

 const handleLink = useCallback(
   (method: AuthMethod) => {
     link(method);
     if (!method.startsWith("oauth:")) {
       setOpenModal(method);
     }
   },
   [link, setOpenModal],
 );

  return (
    <>
      <LinkAuthItems onLink={handleLink} />
      {modalMethods.map(method => {
        return (
          <SignInModal
            key={method}
            open={openModal === method}
            authMethods={[method]}
            setIsOpen={isOpen => (isOpen ? setOpenModal(method) : handleClose())}
            onSuccess={() => setOpenModal(null)}
          >
            <SignInModalTrigger>null</SignInModalTrigger>
          </SignInModal>
        );
      })}
    </>
  );
};

function App() {
  return (
    <CDPReactProvider config={config}>
      <LinkAuth>
        <h2>Link a profile</h2>
        <CustomLinkAuthItems />
      </LinkAuth>
    </CDPReactProvider>
  );
}
```

## Further reading

* [LinkAuth Overview](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/LinkAuth.README)

