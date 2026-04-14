# LinkAuthMethod
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/LinkAuthMethod



```ts theme={null}
type LinkAuthMethod = {
  isLinked: boolean;
  method: AuthMethod;
  userAlias: string;
};
```

Representation of auth method

## See

* [LinkAuthState](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/LinkAuthState)
* [LinkAuth](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/LinkAuth)

## Properties

| Property          | Type                                                                                   | Description                                                                         |
| ----------------- | -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| <a /> `isLinked`  | `boolean`                                                                              | Whether the user has this auth method linked to their account                       |
| <a /> `method`    | [`AuthMethod`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/AuthMethod) | The auth method                                                                     |
| <a /> `userAlias` | `string`                                                                               | The user's identifier for this auth method (i.e. email address, phone number, etc.) |

