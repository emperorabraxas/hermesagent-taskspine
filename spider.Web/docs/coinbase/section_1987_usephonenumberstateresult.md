# UsePhoneNumberStateResult
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/UsePhoneNumberStateResult



Return value from the usePhoneNumberState hook.

## Properties

| Property                        | Type                                                                                                     | Description                                                            |
| ------------------------------- | -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| <a /> `phoneNumberObject`       | [`PhoneNumber`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/PhoneNumber)                   | The phone number object with value and e164 fields.                    |
| <a /> `countryCode`             | `CountryCode`                                                                                            | The current country code.                                              |
| <a /> `handlePhoneNumberChange` | (`pn`: [`PhoneNumber`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/PhoneNumber)) => `void` | Handler for PhoneNumberInput/PhoneNumberForm onPhoneNumberChange prop. |
| <a /> `handleCountryCodeChange` | (`countryCode`: `CountryCode`) => `void`                                                                 | Handler for PhoneNumberInput/PhoneNumberForm onCountryCodeChange prop. |

