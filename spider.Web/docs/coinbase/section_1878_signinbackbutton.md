# SignInBackButton
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/SignInBackButton



```ts theme={null}
function SignInBackButton(props: SignInBackButtonProps): null | Element;
```

A button to go back to the previous step of the sign-in flow.

## Parameters

| Parameter | Type                                                                                                       | Description                  |
| --------- | ---------------------------------------------------------------------------------------------------------- | ---------------------------- |
| `props`   | [`SignInBackButtonProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/SignInBackButtonProps) | The props for the component. |

## Returns

`null` | `Element`

The sign-in back button.

## Example

```tsx lines theme={null}
function App() {
  // Customize the back button icon and label
  return (
    <CDPReactProvider config={config} theme={themeOverrides}>
      <SignIn>
        <SignInBackButton aria-label="go back">
          <MyCustomIcon />
        </SignInBackButton>
        <SignInImage />
        <SignInTitle />
        <SignInDescription />
        <SignInForm />
        <SignInFooter />
      </SignIn>
    </CDPReactProvider>
  );
}
```

