# IconLock
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/IconLock



```ts theme={null}
function IconLock(props: Omit<SVGProps<SVGSVGElement>, "viewBox">): Element;
```

Lock icon component.

## Parameters

| Parameter | Type                                               | Description             |
| --------- | -------------------------------------------------- | ----------------------- |
| `props`   | `Omit`\<`SVGProps`\<`SVGSVGElement`>, `"viewBox"`> | The props for the icon. |

## Returns

`Element`

The Lock icon.

## Example

```tsx lines theme={null}
// Icon is correctly from screen readers
<p>
  <IconLock />
  Locked
</p>

// Icon with screen-reader accessible label only
<p>
  <IconLock aria-label="locked" />
</p>
```

