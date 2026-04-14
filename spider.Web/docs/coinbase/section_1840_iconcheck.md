# IconCheck
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/IconCheck



```ts theme={null}
function IconCheck(props: Omit<SVGProps<SVGSVGElement>, "viewBox">): Element;
```

Check Circle icon component.

## Parameters

| Parameter | Type                                               | Description             |
| --------- | -------------------------------------------------- | ----------------------- |
| `props`   | `Omit`\<`SVGProps`\<`SVGSVGElement`>, `"viewBox"`> | The props for the icon. |

## Returns

`Element`

The Check Circle icon.

## Example

```tsx lines theme={null}
// Icon is correctly from screen readers
<p>
  <IconCheck />
  Success!
</p>

// Icon with screen-reader accessible label only
<p>
  <IconCheck aria-label="Success" />
</p>
```

