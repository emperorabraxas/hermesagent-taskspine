# IconEnvelope
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/IconEnvelope



```ts theme={null}
function IconEnvelope(props: Omit<SVGProps<SVGSVGElement>, "viewBox">): Element;
```

Envelope icon component.

## Parameters

| Parameter | Type                                               | Description             |
| --------- | -------------------------------------------------- | ----------------------- |
| `props`   | `Omit`\<`SVGProps`\<`SVGSVGElement`>, `"viewBox"`> | The props for the icon. |

## Returns

`Element`

The Envelope icon.

## Example

```tsx lines theme={null}
// Icon is correctly from screen readers
<p>
  <IconEnvelope />
  Email me a code
</p>

// Icon with screen-reader accessible label only
<p>
  <IconEnvelope aria-label="Email me a code" />
</p>
```

