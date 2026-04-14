# FetchBuyOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/FetchBuyOptions



```ts theme={null}
type FetchBuyOptions = (params: {
  country: string;
  subdivision?: string;
}) => Promise<OnrampBuyOptionsResponse>;
```

Get Buy Options function (used for building list of payment methods)

## Parameters

| Parameter             | Type                                                |
| --------------------- | --------------------------------------------------- |
| `params`              | \{ `country`: `string`; `subdivision?`: `string`; } |
| `params.country`      | `string`                                            |
| `params.subdivision?` | `string`                                            |

## Returns

`Promise`\<[`OnrampBuyOptionsResponse`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/OnrampBuyOptionsResponse)>

