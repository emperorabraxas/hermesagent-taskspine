# CdpWalletAccount
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-solana-standard-wallet/Classes/CdpWalletAccount



CDP Wallet Account implementation for Solana accounts.

This class represents a Solana account within the CDP wallet ecosystem.

## Implements

* `WalletAccount`

## Accessors

### address

#### Get Signature

```ts theme={null}
get address(): string;
```

Get the base58 encoded address of this account.

##### Returns

`string`

The base58 encoded Solana address

#### Implementation of

```ts theme={null}
WalletAccount.address
```

***

### publicKey

#### Get Signature

```ts theme={null}
get publicKey(): Uint8Array<ArrayBuffer>;
```

Get the public key bytes of this account.

##### Returns

`Uint8Array`\<`ArrayBuffer`>

A copy of the public key bytes

#### Implementation of

```ts theme={null}
WalletAccount.publicKey
```

***

### chains

#### Get Signature

```ts theme={null}
get chains(): readonly ["solana:mainnet", "solana:devnet"];
```

Get the supported chains for this account.

##### Returns

readonly \[`"solana:mainnet"`, `"solana:devnet"`]

Array of supported Solana chains

#### Implementation of

```ts theme={null}
WalletAccount.chains
```

***

### features

#### Get Signature

```ts theme={null}
get features(): readonly ["solana:signAndSendTransaction", "solana:signTransaction", "solana:signMessage"];
```

Get the supported features for this account.

##### Returns

readonly \[`"solana:signAndSendTransaction"`, `"solana:signTransaction"`, `"solana:signMessage"`]

Array of supported wallet standard features

#### Implementation of

```ts theme={null}
WalletAccount.features
```

## Constructors

### Constructor

```ts theme={null}
new CdpWalletAccount(publicKey: Uint8Array): CdpWalletAccount;
```

Create a new CDP Wallet Account.

#### Parameters

| Parameter   | Type         | Description                                                                 |
| ----------- | ------------ | --------------------------------------------------------------------------- |
| `publicKey` | `Uint8Array` | The public key bytes for this account (must be exactly 32 bytes for Solana) |

#### Returns

`CdpWalletAccount`

#### Throws

If publicKey is null, undefined, or not exactly 32 bytes

