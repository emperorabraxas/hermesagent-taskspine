# IconPhone
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/IconPhone



```ts theme={null}
function IconPhone(props: Omit<SVGProps<SVGSVGElement>, "viewBox">): Element;
```

Phone icon component.

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
  <IconPhone />
  Text me a code
</p>

// Icon with screen-reader accessible label only
<p>
  <IconPhone aria-label="Text me a code" />
</p>
```

