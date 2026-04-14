# GetUserOperationOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/GetUserOperationOptions



```ts theme={null}
type GetUserOperationOptions = {
  userOperationHash: Hex;
  evmSmartAccount: EvmAddress;
  network: SendEvmTransactionWithEndUserAccountBodyNetwork;
};
```

Request parameters for getting a user operation.

## Properties

| Property                  | Type                                                                                                                                                            | Description                                         |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| <a /> `userOperationHash` | [`Hex`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/Hex)                                                                                         | The user operation hash.                            |
| <a /> `evmSmartAccount`   | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmAddress)                                                                           | The EVM Smart Account that sent the user operation. |
| <a /> `network`           | [`SendEvmTransactionWithEndUserAccountBodyNetwork`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendEvmTransactionWithEndUserAccountBodyNetwork) | The network the user operation was sent on.         |

