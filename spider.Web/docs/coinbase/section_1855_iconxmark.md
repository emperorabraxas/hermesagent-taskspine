# IconXMark
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/IconXMark



```ts theme={null}
function IconXMark(props: Omit<SVGProps<SVGSVGElement>, "viewBox">): Element;
```

Close icon component.

## Parameters

| Parameter | Type                                               | Description             |
| --------- | -------------------------------------------------- | ----------------------- |
| `props`   | `Omit`\<`SVGProps`\<`SVGSVGElement`>, `"viewBox"`> | The props for the icon. |

## Returns

`Element`

The Close icon.

## Example

```tsx lines theme={null}
// Icon is correctly from screen readers
<p>
  <IconXMark />
  Close
</p>

// Icon with screen-reader accessible label only
<p>
  <IconXMark aria-label="Close" />
</p>
```

