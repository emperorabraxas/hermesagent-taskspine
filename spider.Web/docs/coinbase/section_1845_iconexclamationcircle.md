# IconExclamationCircle
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/IconExclamationCircle



```ts theme={null}
function IconExclamationCircle(props: Omit<SVGProps<SVGSVGElement>, "viewBox">): Element;
```

Exclamation Circle icon component.

## Parameters

| Parameter | Type                                               | Description             |
| --------- | -------------------------------------------------- | ----------------------- |
| `props`   | `Omit`\<`SVGProps`\<`SVGSVGElement`>, `"viewBox"`> | The props for the icon. |

## Returns

`Element`

The Exclamation Circle icon.

## Example

```tsx lines theme={null}
// Icon is correctly from screen readers
<p>
  <IconExclamationCircle />
  Warning!
</p>

// Icon with screen-reader accessible label only
<p>
  <IconExclamationCircle aria-label="Warning" />
</p>
```

