# IconExclamationTriangle
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/IconExclamationTriangle



```ts theme={null}
function IconExclamationTriangle(props: Omit<SVGProps<SVGSVGElement>, "viewBox">): Element;
```

Exclamation Triangle icon component.

## Parameters

| Parameter | Type                                               | Description             |
| --------- | -------------------------------------------------- | ----------------------- |
| `props`   | `Omit`\<`SVGProps`\<`SVGSVGElement`>, `"viewBox"`> | The props for the icon. |

## Returns

`Element`

The Exclamation Triangle icon.

## Example

```tsx lines theme={null}
// Icon is correctly hidden from screen readers
<p>
  <IconExclamationTriangle />
  Warning!
</p>

// Icon with screen-reader accessible label only
<p>
  <IconExclamationTriangle aria-label="Warning" />
</p>
```

