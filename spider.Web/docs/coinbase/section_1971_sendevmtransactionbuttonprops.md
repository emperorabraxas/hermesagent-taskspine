# SendEvmTransactionButtonProps
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/SendEvmTransactionButtonProps



The props for the SendEvmTransactionButton component.

## See

[SendEvmTransactionButton](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/SendEvmTransactionButton)

## Extends

* `Omit`\<[`ButtonProps`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Interfaces/ButtonProps), `"onError"`>

## Properties

| Property              | Type                                                                                                                                                            | Description                                                                              | Inherited from      |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ------------------- |
| <a /> `account`       | `` `0x${string}` ``                                                                                                                                             | The account to send the transaction from.                                                | -                   |
| <a /> `network`       | [`SendEvmTransactionWithEndUserAccountBodyNetwork`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendEvmTransactionWithEndUserAccountBodyNetwork) | The network to send the transaction on.                                                  | -                   |
| <a /> `onError?`      | (`error`: \| `Error` \| [`APIError`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Classes/APIError)) => `void`                                                 | A function to call when the transaction errors.                                          | -                   |
| <a /> `onSuccess?`    | (`hash`: `string`) => `void`                                                                                                                                    | A function to call when the transaction is successful.                                   | -                   |
| <a /> `transaction`   | [`AllowedEvmTransactionType`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/AllowedEvmTransactionType)                                            | The transaction to send.                                                                 | -                   |
| <a /> `size?`         | [`ButtonSize`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/ButtonSize)                                                                          | The size of the button. Defaults to "md".                                                | `Omit.size`         |
| <a /> `asChild?`      | `boolean`                                                                                                                                                       | Set to true to use a custom element or component in place of the default button element. | `Omit.asChild`      |
| <a /> `fullWidth?`    | `boolean`                                                                                                                                                       | Whether the button should be full width.                                                 | `Omit.fullWidth`    |
| <a /> `isPending?`    | `boolean`                                                                                                                                                       | Whether the button state is pending.                                                     | `Omit.isPending`    |
| <a /> `pendingLabel?` | `ReactNode`                                                                                                                                                     | A label to render when the button state is pending.                                      | `Omit.pendingLabel` |
| <a /> `variant?`      | [`ButtonVariant`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Type-Aliases/ButtonVariant)                                                                    | The variant of the button. Defaults to "primary".                                        | `Omit.variant`      |

