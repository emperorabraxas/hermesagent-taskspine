# IconPlus
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/IconPlus



```ts theme={null}
function IconPlus(props: Omit<SVGProps<SVGSVGElement>, "viewBox">): Element;
```

Plus icon component.

## Parameters

| Parameter | Type                                               | Description             |
| --------- | -------------------------------------------------- | ----------------------- |
| `props`   | `Omit`\<`SVGProps`\<`SVGSVGElement`>, `"viewBox"`> | The props for the icon. |

## Returns

`Element`

The Plus icon.

## Example

```tsx lines theme={null}
// Icon is correctly from screen readers
<p>
  <IconPlus />
</p>

// Icon with screen-reader accessible label only
<p>
  <IconPlus aria-label="Plus" />
</p>
```

