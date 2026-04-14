# IconCheckCircle
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/IconCheckCircle



```ts theme={null}
function IconCheckCircle(props: Omit<SVGProps<SVGSVGElement>, "viewBox">): Element;
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
  <IconCheckCircle />
  Success!
</p>

// Icon with screen-reader accessible label only
<p>
  <IconCheckCircle aria-label="Success" />
</p>
```

