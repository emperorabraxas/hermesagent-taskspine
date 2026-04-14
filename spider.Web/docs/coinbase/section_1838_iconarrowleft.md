# IconArrowLeft
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/IconArrowLeft



```ts theme={null}
function IconArrowLeft(props: Omit<SVGProps<SVGSVGElement>, "viewBox">): Element;
```

Arrow Left icon component.

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
  <IconArrowLeft />
  Back
</p>

// Icon with screen-reader accessible label only
<p>
  <IconArrowLeft aria-label="Back" />
</p>
```

