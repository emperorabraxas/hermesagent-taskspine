# ComponentBorderRadius
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/ComponentBorderRadius



```ts theme={null}
type ComponentBorderRadius = Flattened<{
  borderRadius: typeof borderRadiusComponents;
}>;
```

Component border radii are the border radius values for the individual UI components.
They inherit values from the SemanticBorderRadius via CSS variables.

## Example

```tsx lines theme={null}
const theme: Partial<ComponentBorderRadius> = {
  "border-radius-cta": "var(--cdp-web-border-radius-none)", // Remove border radius for ctas only
};
```

## See

* [borderRadiusComponents](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Variables/borderRadiusComponents) for the default token values
* [SemanticBorderRadius](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/SemanticBorderRadius) for the semantic border radius values that the component border radius values inherit from

