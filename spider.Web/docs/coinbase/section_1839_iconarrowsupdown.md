# IconArrowsUpDown
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/IconArrowsUpDown



```ts theme={null}
function IconArrowsUpDown(props: Omit<SVGProps<SVGSVGElement>, "viewBox">): Element;
```

Arrows Up/Down icon component.

## Parameters

| Parameter | Type                                               | Description             |
| --------- | -------------------------------------------------- | ----------------------- |
| `props`   | `Omit`\<`SVGProps`\<`SVGSVGElement`>, `"viewBox"`> | The props for the icon. |

## Returns

`Element`

The Arrow Left icon.

## Example

```tsx lines theme={null}
// Icon is correctly hidden from screen readers
<p>
  <IconArrowsUpDown />
  Swap
</p>

// Icon with screen-reader accessible label only
<p>
  <IconArrowsUpDown aria-label="Swap" />
</p>
```

