# IconSmartPhone
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/IconSmartPhone



```ts theme={null}
function IconSmartPhone(props: Omit<SVGProps<SVGSVGElement>, "viewBox">): Element;
```

Smart phone icon component.

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
  <IconSmartPhone />
  Enter code from your authenticator app
</p>

// Icon with screen-reader accessible label only
<p>
  <IconSmartPhone aria-label="Enter code from your authenticator app" />
</p>
```

