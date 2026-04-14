# SecureIframeThemeMessage
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SecureIframeThemeMessage



```ts theme={null}
type SecureIframeThemeMessage = {
  type: SecureIframeEventType["THEME"];
  payload: {
     theme: Partial<SecureIframeTheme>;
  };
};
```

The message sent to the secure iframe to update the theme.

## Properties

| Property        | Type                                                                                                                           |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| <a /> `type`    | [`SecureIframeEventType`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SecureIframeEventType)\[`"THEME"`]        |
| <a /> `payload` | \{ `theme`: `Partial`\<[`SecureIframeTheme`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SecureIframeTheme)>; } |
| `payload.theme` | `Partial`\<[`SecureIframeTheme`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SecureIframeTheme)>                |

