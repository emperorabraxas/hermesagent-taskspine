# themeToCssVariables
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Utilities/themeToCssVariables



```ts theme={null}
function themeToCssVariables(theme: Record<string, string>): CDPWebCSSVariables;
```

Converts a theme object to a CSS variables object for the CDP web component library.

## Parameters

| Parameter | Type                          | Description                  |
| --------- | ----------------------------- | ---------------------------- |
| `theme`   | `Record`\<`string`, `string`> | The theme object to convert. |

## Returns

[`CDPWebCSSVariables`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/CDPWebCSSVariables)

A CSS variables object.

## Example

```tsx lines theme={null}
const themeOverrides: Partial<Theme> = {
  "color-bg-primary": "red",
};

// { "--cdp-web-color-bg-primary": "red" }
const cssVariables = themeToCssVariables(themeOverrides);
```

