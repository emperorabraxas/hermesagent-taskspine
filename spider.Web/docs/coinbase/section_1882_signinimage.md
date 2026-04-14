# SignInImage
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/SignInImage



```ts theme={null}
function SignInImage(props: SignInImageProps): null | Element;
```

A logo or success icon for the SignIn component.

## Parameters

| Parameter | Type                                                                                             | Description                  |
| --------- | ------------------------------------------------------------------------------------------------ | ---------------------------- |
| `props`   | [`SignInImageProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/SignInImageProps) | The props for the component. |

## Returns

`null` | `Element`

The rendered component.

## Example

```tsx lines theme={null}
function App() {
  // Use a different image from your app logo in the SignIn component
  return (
    <CDPReactProvider config={config} theme={themeOverrides}>
      <SignIn>
        <SignInBackButton />
        <SignInImage src="https://example.com/image.png" alt="Example Image" />
        <SignInTitle />
        <SignInDescription />
        <SignInForm />
        <SignInFooter />
      </SignIn>
    </CDPReactProvider>
  );
}
```

