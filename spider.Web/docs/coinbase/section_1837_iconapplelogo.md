# IconAppleLogo
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/IconAppleLogo



```ts theme={null}
function IconAppleLogo(props: Omit<SVGProps<SVGSVGElement>, "viewBox">): Element;
```

Apple logo icon component.

## Parameters

| Parameter | Type                                               | Description             |
| --------- | -------------------------------------------------- | ----------------------- |
| `props`   | `Omit`\<`SVGProps`\<`SVGSVGElement`>, `"viewBox"`> | The props for the icon. |

## Returns

`Element`

The Apple logo icon.

## Example

```tsx theme={null}
// Icon is correctly hidden from screen readers
<p>
  <IconAppleLogo />
  Apple
</p>

// Icon with screen-reader accessible label only
<p>
  <IconAppleLogo aria-label="Apple" />
</p>
```

