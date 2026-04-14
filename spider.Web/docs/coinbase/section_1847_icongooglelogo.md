# IconGoogleLogo
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/IconGoogleLogo



```ts theme={null}
function IconGoogleLogo(props: Omit<SVGProps<SVGSVGElement>, "viewBox">): Element;
```

Google logo icon component.

## Parameters

| Parameter | Type                                               | Description             |
| --------- | -------------------------------------------------- | ----------------------- |
| `props`   | `Omit`\<`SVGProps`\<`SVGSVGElement`>, `"viewBox"`> | The props for the icon. |

## Returns

`Element`

The Google logo icon.

## Example

```tsx lines theme={null}
// Icon is correctly hidden from screen readers
<p>
  <IconGoogleLogo />
  Google
</p>

// Icon with screen-reader accessible label only
<p>
  <IconGoogleLogo aria-label="Google" />
</p>
```

