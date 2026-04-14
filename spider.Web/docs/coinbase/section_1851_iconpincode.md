# IconPinCode
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/IconPinCode



```ts theme={null}
function IconPinCode(props: Omit<SVGProps<SVGSVGElement>, "viewBox">): Element;
```

Pin code icon component.

## Parameters

| Parameter | Type                                               | Description             |
| --------- | -------------------------------------------------- | ----------------------- |
| `props`   | `Omit`\<`SVGProps`\<`SVGSVGElement`>, `"viewBox"`> | The props for the icon. |

## Returns

`Element`

The chat bubble icon.

## Example

```tsx lines theme={null}
// Icon is correctly from screen readers
<p>
  <IconPinCode />
  Enter code from your authenticator app
</p>

// Icon with screen-reader accessible label only
<p>
  <IconPinCode aria-label="Enter code from your authenticator app" />
</p>
```

