# SendUsdcResult
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendUsdcResult



```ts theme={null}
type SendUsdcResult = 
  | {
  type: "evm-eoa";
  transactionHash: Hex;
  from: EvmAddress;
  network: SendEvmUsdcNetwork;
}
  | {
  type: "evm-smart";
  userOpHash: Hex;
  from: EvmAddress;
  network: SendEvmUsdcNetwork;
}
  | {
  type: "solana";
  transactionSignature: string;
  from: SolanaAddress;
  network: SendSolanaUsdcNetwork;
};
```

Result of sendUsdc - discriminated union based on account type.

