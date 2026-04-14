# FundState
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/FundState



The state of the Fund component.

## Properties

| Property                         | Type                                                                                                           |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| <a /> `country`                  | `string`                                                                                                       |
| <a /> `cryptoAmount?`            | `number`                                                                                                       |
| <a /> `cryptoCurrency`           | `string`                                                                                                       |
| <a /> `cryptoDecimalPlaces?`     | `number`                                                                                                       |
| <a /> `exchangeRate?`            | `number`                                                                                                       |
| <a /> `exchangeRateError?`       | \| `null` \| [`FundStateError`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/FundStateError)    |
| <a /> `isExchangeRatePending?`   | `boolean`                                                                                                      |
| <a /> `isPaymentMethodsPending?` | `boolean`                                                                                                      |
| <a /> `fiatAmount?`              | `number`                                                                                                       |
| <a /> `fiatCurrency`             | `string`                                                                                                       |
| <a /> `fiatDecimalPlaces?`       | `number`                                                                                                       |
| <a /> `locale?`                  | `string`                                                                                                       |
| <a /> `network`                  | `string`                                                                                                       |
| <a /> `paymentMethods?`          | [`FundPaymentMethod`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/FundPaymentMethod)\[]          |
| <a /> `paymentMethodsError?`     | \| `null` \| [`FundStateError`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/FundStateError)    |
| <a /> `presetAmountInputs?`      | [`FundPresetAmountInputs`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/FundPresetAmountInputs) |
| <a /> `selectedInputType`        | [`InputType`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/InputType)                           |
| <a /> `selectedPaymentMethod?`   | [`FundPaymentMethod`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/FundPaymentMethod)             |
| <a /> `subdivision?`             | `string`                                                                                                       |
| <a /> `transactionStatus`        | [`FundLifecycleStatus`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/FundLifecycleStatus)       |
| <a /> `destinationAddress`       | `string`                                                                                                       |

