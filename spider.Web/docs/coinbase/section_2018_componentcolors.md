# ComponentColors
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/ComponentColors



```ts theme={null}
type ComponentColors = Flattened<{
  colors: typeof colorsComponents;
}>;
```

Component colors are the colors for the individual UI components.
They inherit values from the SemanticColors via CSS variables.

## Example

```tsx lines theme={null}
const theme: Partial<ComponentColors> = {
  "colors-cta-primary-bg-default": "var(--cdp-web-colors-bg-primary)",
};
```

## See

* [colorsComponents](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Variables/colorsComponents) for the default token values
* [SemanticColors](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/SemanticColors) for the semantic colors that the component colors inherit from

