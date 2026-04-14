# FundProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/FundProps



All the props for the Fund component.

## Extends

* [`FundStateProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/FundStateProps).`FundLifecycleEvents`

## Properties

| Property                     | Type                                                                                                                                    | Inherited from                       |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| <a /> `children?`            | \| `ReactNode` \| (`state`: [`FundState`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/FundState)) => `ReactNode`          | -                                    |
| <a /> `className?`           | `string`                                                                                                                                | -                                    |
| <a /> `fetchBuyOptions`      | [`FetchBuyOptions`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/FetchBuyOptions)                                        | -                                    |
| <a /> `fetchBuyQuote`        | [`FetchBuyQuote`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/FetchBuyQuote)                                            | -                                    |
| <a /> `inputType?`           | [`InputType`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/InputType)                                                    | -                                    |
| <a /> `openIn?`              | `"popup"` \| `"tab"`                                                                                                                    | -                                    |
| <a /> `redirectUrl?`         | `string`                                                                                                                                | -                                    |
| <a /> `style?`               | `CSSProperties`                                                                                                                         | -                                    |
| <a /> `submitLabel?`         | `ReactNode`                                                                                                                             | -                                    |
| <a /> `title?`               | `ReactNode`                                                                                                                             | -                                    |
| <a /> `country`              | `string`                                                                                                                                | `FundStateProps.country`             |
| <a /> `locale?`              | `string`                                                                                                                                | `FundStateProps.locale`              |
| <a /> `cryptoDecimalPlaces?` | `number`                                                                                                                                | `FundStateProps.cryptoDecimalPlaces` |
| <a /> `cryptoCurrency`       | `string`                                                                                                                                | `FundStateProps.cryptoCurrency`      |
| <a /> `fiatCurrency`         | `string`                                                                                                                                | `FundStateProps.fiatCurrency`        |
| <a /> `fiatDecimalPlaces?`   | `number`                                                                                                                                | `FundStateProps.fiatDecimalPlaces`   |
| <a /> `network`              | `string`                                                                                                                                | `FundStateProps.network`             |
| <a /> `presetAmountInputs?`  | [`FundPresetAmountInputs`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/FundPresetAmountInputs)                          | `FundStateProps.presetAmountInputs`  |
| <a /> `subdivision?`         | `string`                                                                                                                                | `FundStateProps.subdivision`         |
| <a /> `destinationAddress`   | `string`                                                                                                                                | `FundStateProps.destinationAddress`  |
| <a /> `onError?`             | (`e`: \| `undefined` \| [`OnrampError`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/OnrampError)) => `void`               | `FundLifecycleEvents.onError`        |
| <a /> `onStatus?`            | (`lifecycleStatus`: [`FundLifecycleStatus`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/FundLifecycleStatus)) => `void` | `FundLifecycleEvents.onStatus`       |
| <a /> `onSuccess?`           | (`result?`: [`OnrampSuccessEventData`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/OnrampSuccessEventData)) => `void`   | `FundLifecycleEvents.onSuccess`      |

