# Theme
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/Theme



```ts theme={null}
type Theme = ColorTokens & FontTokens & BorderRadiusTokens & ZIndexTokens;
```

The theme is a flattened tokens object with values appropriate for web environments
(i.e. CSS properties & CSS Variables).

It DOES NOT include the namespace (`--cdp-web-`) in the keys.

