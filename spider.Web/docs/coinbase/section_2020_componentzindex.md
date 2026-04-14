# ComponentZIndex
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/ComponentZIndex



```ts theme={null}
type ComponentZIndex = Flattened<{
  zIndex: typeof zIndexComponents;
}>;
```

Component z-index values for individual UI components.
They inherit from the SemanticZIndex via CSS variables.

## Example

```tsx lines theme={null}
const theme: Partial<ComponentZIndex> = {
  "zIndex-modal-overlay": "1000",
  "zIndex-modal-dialog": "1001",
};
```

## See

* [zIndexComponents](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Variables/zIndexComponents) for the default token values
* [SemanticZIndex](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/SemanticZIndex) for the semantic z-index values that component values inherit from

