# useCdpSolanaStandardWallet
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-solana-standard-wallet/Functions/useCdpSolanaStandardWallet



```ts theme={null}
function useCdpSolanaStandardWallet(config?: Config): {
  ready: boolean;
  wallet:   | null
     | CdpSolanaWallet;
};
```

Hook to get the CDP Standard Solana Wallet with ready state.

This hook monitors the user's Solana accounts from CDP core and:

* Creates and registers a CdpSolanaWallet when accounts are available
* Returns a ready flag indicating when the wallet is instantiated and registered
* Returns the wallet instance for direct usage
* Handles cleanup/unregistration on unmount

## Parameters

| Parameter | Type     | Description                                                                                                                                    |
| --------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `config?` | `Config` | Optional CDP configuration. If provided, will initialize the SDK. If omitted, assumes SDK is already initialized (e.g., via CDPHooksProvider). |

## Returns

```ts theme={null}
{
  ready: boolean;
  wallet:   | null
     | CdpSolanaWallet;
}
```

Object containing ready flag and wallet instance

| Name     | Type                                                                                                                      |
| -------- | ------------------------------------------------------------------------------------------------------------------------- |
| `ready`  | `boolean`                                                                                                                 |
| `wallet` | \| `null` \| [`CdpSolanaWallet`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-solana-standard-wallet/Classes/CdpSolanaWallet) |

## Example

```tsx theme={null}
// Within CDPHooksProvider (SDK already initialized)
function MyComponent() {
  const { ready, wallet } = useCdpSolanaStandardWallet();
  // ...
}

// Standalone usage (initialize SDK)
function MyComponent() {
  const { ready, wallet } = useCdpSolanaStandardWallet({
    projectId: "your-project-id"
  });
  // ...
}
```

