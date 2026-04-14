# fontSemantic
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Variables/fontSemantic



```ts theme={null}
const fontSemantic: {
  family: {
     mono: {
        value: "\"DM Mono\", monospace";
     };
     sans: {
        value: "\"Rethink Sans\", -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, Helvetica, Arial, sans-serif, \"Apple Color Emoji\", \"Segoe UI Emoji\", \"Segoe UI Symbol\"";
     };
     body: {
        value: "{font.family.sans}";
     };
     interactive: {
        value: "{font.family.sans}";
     };
  };
  size: {
     base: {
        value: 16;
     };
  };
};
```

Semantic font tokens.

## Type declaration

| Name                       | Type                                                                                                                                                                                                                                                                                                                                             | Default value                                                                                                                                                     |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <a /> `family`             | \{ `mono`: \{ `value`: ""DM Mono", monospace"; }; `sans`: \{ `value`: ""Rethink Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol""; }; `body`: \{ `value`: `"{font.family.sans}"`; }; `interactive`: \{ `value`: `"{font.family.sans}"`; }; } | -                                                                                                                                                                 |
| `family.mono`              | \{ `value`: ""DM Mono", monospace"; }                                                                                                                                                                                                                                                                                                            | -                                                                                                                                                                 |
| `family.mono.value`        | ""DM Mono", monospace"                                                                                                                                                                                                                                                                                                                           | `'"DM Mono", monospace'`                                                                                                                                          |
| `family.sans`              | \{ `value`: ""Rethink Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol""; }                                                                                                                                                                   | -                                                                                                                                                                 |
| `family.sans.value`        | ""Rethink Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol""                                                                                                                                                                                  | `'"Rethink Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"'` |
| `family.body`              | \{ `value`: `"{font.family.sans}"`; }                                                                                                                                                                                                                                                                                                            | -                                                                                                                                                                 |
| `family.body.value`        | `"{font.family.sans}"`                                                                                                                                                                                                                                                                                                                           | `"{font.family.sans}"`                                                                                                                                            |
| `family.interactive`       | \{ `value`: `"{font.family.sans}"`; }                                                                                                                                                                                                                                                                                                            | -                                                                                                                                                                 |
| `family.interactive.value` | `"{font.family.sans}"`                                                                                                                                                                                                                                                                                                                           | `"{font.family.sans}"`                                                                                                                                            |
| <a /> `size`               | \{ `base`: \{ `value`: `16`; }; }                                                                                                                                                                                                                                                                                                                | -                                                                                                                                                                 |
| `size.base`                | \{ `value`: `16`; }                                                                                                                                                                                                                                                                                                                              | -                                                                                                                                                                 |
| `size.base.value`          | `16`                                                                                                                                                                                                                                                                                                                                             | `16`                                                                                                                                                              |

