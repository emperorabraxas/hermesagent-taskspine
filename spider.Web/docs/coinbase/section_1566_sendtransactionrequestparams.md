# SendTransactionRequestParams
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendTransactionRequestParams



```ts theme={null}
type SendTransactionRequestParams = [{
  chainId?: `0x${string}`;
  data?: Hex;
  from: EvmAddress;
  to: EvmAddress;
  value: Hex;
  nonce?: Hex;
  gas?: Hex;
  maxFeePerGas?: Hex;
  maxPriorityFeePerGas?: Hex;
  type?: "eip1559";
}];
```

Transaction parameters for the eth\_sendTransaction method.

