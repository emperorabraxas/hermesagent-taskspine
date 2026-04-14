# IconCopy
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/IconCopy



```ts theme={null}
function IconCopy(props: Omit<SVGProps<SVGSVGElement>, "viewBox">): Element;
```

Copy icon component.

## Parameters

| Parameter | Type                                               | Description             |
| --------- | -------------------------------------------------- | ----------------------- |
| `props`   | `Omit`\<`SVGProps`\<`SVGSVGElement`>, `"viewBox"`> | The props for the icon. |

## Returns

`Element`

The copy icon.

## Example

```tsx theme={null}
// Icon is correctly hidden from screen readers
<button type="button" onClick={handleClick}>
  <IconCopy />
  Copy address
</button>

// Icon with screen-reader accessible label only
<button type="button" onClick={handleClick}>
  <IconCopy aria-label="Copy address" />
</button>
```

