# SendUsdcOptions
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendUsdcOptions



```ts theme={null}
type SendUsdcOptions = 
  | {
  from: EvmAddress;
  to: EvmAddress;
  amount: string;
  network: SendEvmUsdcNetwork;
  useCdpPaymaster?: boolean;
  paymasterUrl?: string;
  idempotencyKey?: string;
}
  | {
  from: SolanaAddress;
  to: SolanaAddress;
  amount: string;
  network: SendSolanaUsdcNetwork;
  createRecipientAta?: boolean;
  idempotencyKey?: string;
}
  | {
  to: EvmAddress;
  amount: string;
  network: SendEvmUsdcNetwork;
  useCdpPaymaster?: boolean;
  paymasterUrl?: string;
  idempotencyKey?: string;
}
  | {
  to: SolanaAddress;
  amount: string;
  network: SendSolanaUsdcNetwork;
  createRecipientAta?: boolean;
  idempotencyKey?: string;
};
```

Request parameters for sending USDC.
Uses discriminated unions to prevent invalid parameter combinations at compile-time.

## Type declaration

```ts theme={null}
{
  from: EvmAddress;
  to: EvmAddress;
  amount: string;
  network: SendEvmUsdcNetwork;
  useCdpPaymaster?: boolean;
  paymasterUrl?: string;
  idempotencyKey?: string;
}
```

| Name               | Type                                                                                                  | Description                                                             |
| ------------------ | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `from`             | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmAddress)                 | Explicitly sending from an EVM address (EOA or Smart Account).          |
| `to`               | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmAddress)                 | Recipient EVM address.                                                  |
| `amount`           | `string`                                                                                              | The amount of USDC to send (e.g., "1.50").                              |
| `network`          | [`SendEvmUsdcNetwork`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendEvmUsdcNetwork) | EVM network to send on.                                                 |
| `useCdpPaymaster?` | `boolean`                                                                                             | Whether to use CDP Paymaster to sponsor gas fees (Smart Accounts only). |
| `paymasterUrl?`    | `string`                                                                                              | Optional custom Paymaster URL (Smart Accounts only).                    |
| `idempotencyKey?`  | `string`                                                                                              | Optional idempotency key for safe retries.                              |

```ts theme={null}
{
  from: SolanaAddress;
  to: SolanaAddress;
  amount: string;
  network: SendSolanaUsdcNetwork;
  createRecipientAta?: boolean;
  idempotencyKey?: string;
}
```

| Name                  | Type                                                                                                        | Description                                                     |
| --------------------- | ----------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| `from`                | [`SolanaAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SolanaAddress)                 | Explicitly sending from a Solana address.                       |
| `to`                  | [`SolanaAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SolanaAddress)                 | Recipient Solana address.                                       |
| `amount`              | `string`                                                                                                    | The amount of USDC to send (e.g., "1.50").                      |
| `network`             | [`SendSolanaUsdcNetwork`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendSolanaUsdcNetwork) | Solana network to send on.                                      |
| `createRecipientAta?` | `boolean`                                                                                                   | Whether to create recipient's ATA if needed (\~0.002 SOL cost). |
| `idempotencyKey?`     | `string`                                                                                                    | Optional idempotency key for safe retries.                      |

```ts theme={null}
{
  to: EvmAddress;
  amount: string;
  network: SendEvmUsdcNetwork;
  useCdpPaymaster?: boolean;
  paymasterUrl?: string;
  idempotencyKey?: string;
}
```

| Name               | Type                                                                                                  | Description                                                                                             |
| ------------------ | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `to`               | [`EvmAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/EvmAddress)                 | Auto-select mode for EVM - sender address will be automatically selected if exactly one account exists. |
| `amount`           | `string`                                                                                              | The amount of USDC to send (e.g., "1.50").                                                              |
| `network`          | [`SendEvmUsdcNetwork`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendEvmUsdcNetwork) | EVM network to send on.                                                                                 |
| `useCdpPaymaster?` | `boolean`                                                                                             | Whether to use CDP Paymaster (only used if Smart Account is selected).                                  |
| `paymasterUrl?`    | `string`                                                                                              | Optional custom Paymaster URL (only used if Smart Account is selected).                                 |
| `idempotencyKey?`  | `string`                                                                                              | Optional idempotency key for safe retries.                                                              |

```ts theme={null}
{
  to: SolanaAddress;
  amount: string;
  network: SendSolanaUsdcNetwork;
  createRecipientAta?: boolean;
  idempotencyKey?: string;
}
```

| Name                  | Type                                                                                                        | Description                                                                                                |
| --------------------- | ----------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `to`                  | [`SolanaAddress`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SolanaAddress)                 | Auto-select mode for Solana - sender address will be automatically selected if exactly one account exists. |
| `amount`              | `string`                                                                                                    | The amount of USDC to send (e.g., "1.50").                                                                 |
| `network`             | [`SendSolanaUsdcNetwork`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Type-Aliases/SendSolanaUsdcNetwork) | Solana network to send on.                                                                                 |
| `createRecipientAta?` | `boolean`                                                                                                   | Whether to create recipient's ATA if needed (\~0.002 SOL cost).                                            |
| `idempotencyKey?`     | `string`                                                                                                    | Optional idempotency key for safe retries.                                                                 |

