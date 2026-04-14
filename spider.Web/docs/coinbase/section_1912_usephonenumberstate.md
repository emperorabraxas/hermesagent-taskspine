# usePhoneNumberState
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Hooks/usePhoneNumberState



```ts theme={null}
function usePhoneNumberState(options: UsePhoneNumberStateOptions): UsePhoneNumberStateResult;
```

A hook for managing phone number state with conversion between E.164 string
and PhoneNumber object formats.

This hook handles the bidirectional sync between:

* An E.164 formatted string (used for API calls)
* A PhoneNumber object with value/e164 fields (used by PhoneNumberInput/PhoneNumberForm)

## Parameters

| Parameter | Type                                                                                                                 | Description                         |
| --------- | -------------------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| `options` | [`UsePhoneNumberStateOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/UsePhoneNumberStateOptions) | Configuration options for the hook. |

## Returns

[`UsePhoneNumberStateResult`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/UsePhoneNumberStateResult)

Phone number state and handlers for use with PhoneNumberInput/PhoneNumberForm.

## Example

```tsx theme={null}
const { phoneNumberObject, countryCode, handlePhoneNumberChange, handleCountryCodeChange } =
  usePhoneNumberState({
    phoneNumber: state.phoneNumber,
    onPhoneNumberChange: (e164) => dispatch({ type: "SET_PHONE_NUMBER", payload: { phoneNumber: e164 } }),
  });

<PhoneNumberForm
  phoneNumber={phoneNumberObject}
  countryCode={countryCode}
  onPhoneNumberChange={handlePhoneNumberChange}
  onCountryCodeChange={handleCountryCodeChange}
/>
```

