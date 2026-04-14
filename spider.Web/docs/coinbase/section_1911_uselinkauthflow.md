# useLinkAuthFlow
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Hooks/useLinkAuthFlow



```ts theme={null}
function useLinkAuthFlow(): {
  back: () => void;
  direction?: "left" | "right";
  link: (method: AuthMethod) => void;
  linkSuccess: () => void;
};
```

A hook to get the link auth flow context value.

## Returns

The link auth flow context value.

| Name            | Type                                                                                                         | Description                                                    |
| --------------- | ------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------- |
| `back()`        | () => `void`                                                                                                 | A function to call when the back button is clicked.            |
| `direction?`    | `"left"` \| `"right"`                                                                                        | The direction of the flow transition.                          |
| `link()`        | (`method`: [`AuthMethod`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/AuthMethod)) => `void` | A function to call when the user links an auth method.         |
| `linkSuccess()` | () => `void`                                                                                                 | A function to call when an auth method is successfully linked. |

## See

* [LinkAuthFlow](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/LinkAuthFlow)
* [LinkAuth](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/LinkAuth)

