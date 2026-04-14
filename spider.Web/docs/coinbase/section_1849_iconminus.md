# IconMinus
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/IconMinus



```ts theme={null}
function IconMinus(props: Omit<SVGProps<SVGSVGElement>, "viewBox">): Element;
```

Minus icon component.

## Parameters

| Parameter | Type                                               | Description             |
| --------- | -------------------------------------------------- | ----------------------- |
| `props`   | `Omit`\<`SVGProps`\<`SVGSVGElement`>, `"viewBox"`> | The props for the icon. |

## Returns

`Element`

The Minus icon.

## Example

```tsx lines theme={null}
// Icon is correctly from screen readers
<p>
  <IconMinus />
</p>

// Icon with screen-reader accessible label only
<p>
  <IconMinus aria-label="Minus" />
</p>
```

