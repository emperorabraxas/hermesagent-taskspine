# EIP712TypedData
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/EIP712TypedData



The message to sign using EIP-712.

## Properties

| Property            | Type                                                                                        | Description                                                                                                            |
| ------------------- | ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| <a /> `domain`      | [`EIP712Domain`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/EIP712Domain)     | -                                                                                                                      |
| <a /> `types`       | [`EIP712Types`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/EIP712Types)       | -                                                                                                                      |
| <a /> `primaryType` | `string`                                                                                    | The primary type of the message. This is the name of the struct in the `types` object that is the root of the message. |
| <a /> `message`     | [`EIP712Message`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EIP712Message) | The message to sign. The structure of this message must match the `primaryType` struct in the `types` object.          |

