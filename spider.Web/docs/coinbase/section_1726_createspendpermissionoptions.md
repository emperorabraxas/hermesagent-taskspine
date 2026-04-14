# CreateSpendPermissionOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/CreateSpendPermissionOptions



```ts theme={null}
type CreateSpendPermissionOptions = Omit<CoreCreateSpendPermissionOptions, "evmSmartAccount"> & {
  evmSmartAccount?: EvmAddress;
};
```

Options for the useCreateSpendPermission hook.

## Type declaration

| Name               | Type                                                                                   |
| ------------------ | -------------------------------------------------------------------------------------- |
| `evmSmartAccount?` | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/EvmAddress) |

## Param

The EVM Smart Account to create the spend permission for.

## Param

The network to create the spend permission on.

## Param

The spender of the spend permission.

## Param

The token of the spend permission.

## Param

The allowance of the spend permission.

## Param

The period of the spend permission.

## Param

The start of the spend permission.

## Param

The end of the spend permission.

## Param

The salt of the spend permission.

## Param

The extra data of the spend permission.

## Param

Whether to use the CDP Paymaster for the user operation.

## Param

The paymaster URL of the spend permission.

