# SignInModal
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/SignInModal



```ts theme={null}
function SignInModal(props: SignInModalProps): Element;
```

A sign-in modal component that wraps the [SignIn](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/SignIn) component.
In the SignIn modal, the description is hidden on the "credentials" step, and the title is hidden on the "verification" step.

## Parameters

| Parameter | Type                                                                                             | Description                              |
| --------- | ------------------------------------------------------------------------------------------------ | ---------------------------------------- |
| `props`   | [`SignInModalProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/SignInModalProps) | The props for the SignInModal component. |

## Returns

`Element`

The SignInModal component.

## See

* [SignInModalTrigger](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/SignInModalTrigger) for the trigger button.
* [SignInModalContent](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/SignInModalContent) for the modal content.

## Examples

```tsx lines theme={null}
// Render the SignInModal component with a custom success handler
function App() {
  // optional custom success handler
  const handleSignInSuccess = useCallback(() => {
    console.log("Sign in successful");
  }, []);
  return (
    <CDPReactProvider config={config} theme={themeOverrides}>
      <SignInModal onSuccess={handleSignInSuccess} />
    </CDPReactProvider>
  );
}
```

```tsx lines theme={null}
// Render the SignInModal component with a custom trigger button
function App() {
  return (
    <CDPReactProvider config={config} theme={themeOverrides}>
      <SignInModal>
        <button type="button" className="sign-in-button">
          Sign in
        </button>
      </SignInModal>
    </CDPReactProvider>
  );
}
```

```tsx lines theme={null}
// Render the SignInModal component with a secondary variant trigger button and a custom label
function App() {
  return (
    <CDPReactProvider config={config} theme={themeOverrides}>
      <SignInModal>
        <SignInModalTrigger variant="secondary" label="Log in" />
        <!-- modal content will be rendered automatically if not provided -->
      </SignInModal>
    </CDPReactProvider>
  );
}
```

```tsx lines theme={null}
// Render the SignInModal component with a custom class on the modal overlay and window
function App() {
  return (
    <CDPReactProvider config={config} theme={themeOverrides}>
      <SignInModal>
        <!-- SignInModalTrigger must be rendered if SignInModalContent is provided and you want to display the trigger button -->
        <SignInModalTrigger />
        <SignInModalContent className="custom-class" overlayClassName="custom-overlay-class" />
      </SignInModal>
    </CDPReactProvider>
  );
}
```

