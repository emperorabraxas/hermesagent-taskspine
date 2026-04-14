# SignOutButton
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/SignOutButton



```ts theme={null}
function SignOutButton(props?: SignOutButtonProps): Element;
```

A button that signs the user out.

## Parameters

| Parameter | Type                                                                                                 | Description                  |
| --------- | ---------------------------------------------------------------------------------------------------- | ---------------------------- |
| `props?`  | [`SignOutButtonProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/SignOutButtonProps) | The props for the component. |

## Returns

`Element`

The rendered component.

## Examples

```tsx lines theme={null}
// Render a sign out button
<SignOutButton onSuccess={() => console.log("Sign out success")} />
```

```tsx lines theme={null}
// Render a sign out button with a custom label, size, and variant
<SignOutButton size="sm" variant="secondary">Log out</SignOutButton>
```

```tsx lines theme={null}
// Render a sign out button with a custom button element
<SignOutButton asChild>
  <button className="custom-button">Log out</button>
</SignOutButton>
```

