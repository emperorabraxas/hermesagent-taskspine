# IconShield
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/IconShield



```ts theme={null}
function IconShield(props: Omit<SVGProps<SVGSVGElement>, "viewBox">): Element;
```

Shield icon component.

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
  <IconShield />
  Secure your account
</p>

// Icon with screen-reader accessible label only
<p>
  <IconShield aria-label="Secure your account" />
</p>
```

