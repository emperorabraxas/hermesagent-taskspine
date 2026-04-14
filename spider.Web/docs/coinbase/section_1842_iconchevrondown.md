# IconChevronDown
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/IconChevronDown



```ts theme={null}
function IconChevronDown(props: Omit<SVGProps<SVGSVGElement>, "viewBox">): Element;
```

Chevron down icon component.

## Parameters

| Parameter | Type                                               | Description             |
| --------- | -------------------------------------------------- | ----------------------- |
| `props`   | `Omit`\<`SVGProps`\<`SVGSVGElement`>, `"viewBox"`> | The props for the icon. |

## Returns

`Element`

The chevron down icon.

## Example

```tsx lines theme={null}
// Icon is correctly hidden from screen readers
<p>
  <IconChevronDown />
  Expand
</p>

// Icon with screen-reader accessible label only
<p>
  <IconChevronDown aria-label="Expand" />
</p>
```

