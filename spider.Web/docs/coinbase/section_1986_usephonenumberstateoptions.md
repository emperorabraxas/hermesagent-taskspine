# UsePhoneNumberStateOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/UsePhoneNumberStateOptions



Options for the usePhoneNumberState hook.

## Properties

| Property                     | Type                                     | Description                                   |
| ---------------------------- | ---------------------------------------- | --------------------------------------------- |
| <a /> `phoneNumber?`         | `string`                                 | The initial E.164 phone number string.        |
| <a /> `countryCode?`         | `CountryCode`                            | The initial country code. Defaults to "US".   |
| <a /> `onPhoneNumberChange?` | (`e164`: `string`) => `void`             | Callback when the E.164 phone number changes. |
| <a /> `onCountryCodeChange?` | (`countryCode`: `CountryCode`) => `void` | Callback when the country code changes.       |

