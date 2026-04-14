# ProviderRequest
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/ProviderRequest



```ts theme={null}
type ProviderRequest = 
  | AccountsRequest
  | RequestAccountsRequest
  | PersonalSignRequest
  | SendTransactionRequest
  | SignTypedDataRequest
  | EthSignRequest
  | ChainIdRequest
  | WalletDisconnectRequest
  | SwitchEthereumChainRequest
  | SendCallsRequest
  | GetCallsStatusRequest
  | GetCapabilitiesRequest;
```

A type representing all supported EIP-1193 requests, strongly typed

