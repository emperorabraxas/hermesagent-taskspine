# SecureIframeTheme
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SecureIframeTheme



```ts theme={null}
type SecureIframeTheme = {
  pageBg: string;
  buttonBg: string;
  buttonBgHover: string;
  buttonBgPressed: string;
  buttonBgFocus: string;
  buttonBorder: string;
  buttonBorderHover: string;
  buttonBorderPressed: string;
  buttonBorderFocus: string;
  buttonBorderFocusInset: string;
  buttonText: string;
  buttonTextHover: string;
  buttonTextPressed: string;
  buttonTextFocus: string;
  buttonBorderRadius: number;
  buttonFontSize: number;
  buttonFontWeight: number;
  buttonSize: "xs" | "sm" | "md" | "lg";
  fontUrl: string;
  fontFamily: string;
};
```

The theme for the secure iframe.
Colors should be hex strings (with or without alpha) or the string "transparent".

## Properties

| Property                       | Type                                 | Description                                                              |
| ------------------------------ | ------------------------------------ | ------------------------------------------------------------------------ |
| <a /> `pageBg`                 | `string`                             | The background color of the page.                                        |
| <a /> `buttonBg`               | `string`                             | The background color of the button.                                      |
| <a /> `buttonBgHover`          | `string`                             | The background color of the button when hovered.                         |
| <a /> `buttonBgPressed`        | `string`                             | The background color of the button when pressed.                         |
| <a /> `buttonBgFocus`          | `string`                             | The background color of the button when focused.                         |
| <a /> `buttonBorder`           | `string`                             | The border color of the button.                                          |
| <a /> `buttonBorderHover`      | `string`                             | The border color of the button when hovered.                             |
| <a /> `buttonBorderPressed`    | `string`                             | The border color of the button when pressed.                             |
| <a /> `buttonBorderFocus`      | `string`                             | The ring color of the button when focused.                               |
| <a /> `buttonBorderFocusInset` | `string`                             | The inner ring color of the button when focused.                         |
| <a /> `buttonText`             | `string`                             | The text color of the button.                                            |
| <a /> `buttonTextHover`        | `string`                             | The text color of the button when hovered.                               |
| <a /> `buttonTextPressed`      | `string`                             | The text color of the button when pressed.                               |
| <a /> `buttonTextFocus`        | `string`                             | The text color of the button when focused.                               |
| <a /> `buttonBorderRadius`     | `number`                             | The border radius of the button.                                         |
| <a /> `buttonFontSize`         | `number`                             | The font size of the button.                                             |
| <a /> `buttonFontWeight`       | `number`                             | The font weight of the button.                                           |
| <a /> `buttonSize`             | `"xs"` \| `"sm"` \| `"md"` \| `"lg"` | The size of the button.                                                  |
| <a /> `fontUrl`                | `string`                             | The URL of the font to use for the button. Must be a google webfont URL. |
| <a /> `fontFamily`             | `string`                             | The font family to use for the button.                                   |

