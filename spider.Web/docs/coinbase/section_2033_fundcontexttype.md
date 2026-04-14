# FundContextType
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/FundContextType



```ts theme={null}
type FundContextType = {
  state: FundState;
  dispatch: Dispatch<FundAction>;
  fetchBuyUrl: (params: FetchBuyUrlParams, onError?: (e: 
     | OnrampError
    | undefined) => void) => Promise<string>;
};
```

The context type for the Fund component.

## Properties

| Property            | Type                                                                                                                                                                                                                                                                          |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <a /> `state`       | [`FundState`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/FundState)                                                                                                                                                                                            |
| <a /> `dispatch`    | `Dispatch`\<[`FundAction`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/FundAction)>                                                                                                                                                                           |
| <a /> `fetchBuyUrl` | (`params`: [`FetchBuyUrlParams`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/FetchBuyUrlParams), `onError?`: (`e`: \| [`OnrampError`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/OnrampError) \| `undefined`) => `void`) => `Promise`\<`string`> |

