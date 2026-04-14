# SemanticFonts
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/SemanticFonts



```ts theme={null}
type SemanticFonts = Flattened<{
  font: typeof fontSemantic;
}>;
```

Semantic fonts are the base fonts for the theme.

They are typically not used directly in the components, but are used to define the base fonts
for the components. Semantic fonts are defined based on their context (i.e. body, interactive).

## Example

```tsx lines theme={null}
const theme: Partial<SemanticFonts> = {
  "font-family-interactive": "var(--cdp-web-font-family-mono)", // Change the font for interactive elements to monospace font
};
```

## See

* [fontSemantic](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Variables/fontSemantic) for the default token values
* [ComponentFonts](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/ComponentFonts) for the component fonts that inherit from the SemanticFonts

