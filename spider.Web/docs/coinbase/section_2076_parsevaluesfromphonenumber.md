# parseValuesFromPhoneNumber
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Utilities/parseValuesFromPhoneNumber



```ts theme={null}
function parseValuesFromPhoneNumber(phoneNumber: string, countryCode?: CountryCode): PhoneNumber;
```

Parse a phone number into a phone number object.

## Parameters

| Parameter      | Type          | Description                                     |
| -------------- | ------------- | ----------------------------------------------- |
| `phoneNumber`  | `string`      | The phone number to parse.                      |
| `countryCode?` | `CountryCode` | The country code to parse the phone number for. |

## Returns

[`PhoneNumber`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/PhoneNumber)

A phone number object.

