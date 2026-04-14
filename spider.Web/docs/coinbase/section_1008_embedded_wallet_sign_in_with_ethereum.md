# Embedded Wallet: Sign In With Ethereum
Source: https://docs.cdp.coinbase.com/embedded-wallets/siwe



<Tags />

## Overview

Sign In With Ethereum (SIWE, [EIP-4361](https://eips.ethereum.org/EIPS/eip-4361)) lets users authenticate using an Ethereum wallet they already own. Instead of a password or OTP, the user signs a structured message with their private key, proving ownership of an address.

This approach is ideal when:

* Your users already have Ethereum wallets (MetaMask, Coinbase Wallet, hardware wallets, etc.)
* You want a crypto-native sign-in experience without email or phone number requirements
* You need to tie the embedded wallet identity to an on-chain address

## How it works

SIWE authentication is a two-step flow:

<AccordionGroup>
  <Accordion title="Step 1: Initiate — request a challenge message">
    Your app calls `signInWithSiwe` with the user's Ethereum address and context about your application. CDP returns a standards-compliant EIP-4361 message containing a cryptographic nonce, expiration time, and the parameters you provided. Present this message to the user's wallet for signing.
  </Accordion>

  <Accordion title="Step 2: Verify — submit the signature">
    After the user signs the message with their wallet, call `verifySiweSignature` with the `flowId` from step 1 and the resulting signature. CDP verifies the signature on-chain, and on success, returns an authenticated user with an embedded wallet.
  </Accordion>

  <Accordion title="Security features">
    * **Cryptographic proof**: Authentication requires a valid signature from the private key controlling the address — no credential sharing
    * **Replay protection**: Each challenge contains a unique nonce and an expiration time
    * **Domain binding**: The `domain` field ties the signed message to your application, preventing cross-site replay attacks
    * **Rate limiting**: Protection against brute force attempts
  </Accordion>
</AccordionGroup>

## SDK integration

### React

Use the `useSignInWithSiwe` and `useVerifySiweSignature` hooks from `@coinbase/cdp-hooks`:

<CodeGroup>
  ```tsx React hooks theme={null}
  import { useSignInWithSiwe, useVerifySiweSignature, useSignOut } from '@coinbase/cdp-hooks';

  function SignInWithEthereum({ walletClient }) {
    const { signInWithSiwe } = useSignInWithSiwe();
    const { verifySiweSignature } = useVerifySiweSignature();
    const { signOut } = useSignOut();

    const handleSignIn = async () => {
      const address = walletClient.account.address;

      // Step 1: Request the challenge message
      const { message, flowId } = await signInWithSiwe({
        address,
        chainId: 1,
        domain: window.location.hostname,
        uri: window.location.origin,
      });

      // Step 2: Ask the user's wallet to sign the message
      const signature = await walletClient.signMessage({ message });

      // Step 3: Verify the signature and complete sign-in
      const { user, isNewUser } = await verifySiweSignature({ flowId, signature });

      console.log(`Signed in as ${user.userId} (${isNewUser ? 'new' : 'returning'} user)`);
    };

    return <button onClick={handleSignIn}>Sign In With Ethereum</button>;
  }
  ```
</CodeGroup>

### Non-React

For vanilla JavaScript/TypeScript or other frameworks, import directly from `@coinbase/cdp-core`:

<CodeGroup>
  ```typescript Vanilla JS theme={null}
  import { initialize, signInWithSiwe, verifySiweSignature } from '@coinbase/cdp-core';

  await initialize({ projectId: 'your-project-id' });

  async function signInWithEthereum(walletClient) {
    const address = walletClient.account.address;

    // Step 1: Request the challenge message
    const { message, flowId } = await signInWithSiwe({
      address,
      chainId: 1,
      domain: window.location.hostname,
      uri: window.location.origin,
    });

    // Step 2: Sign the message with the user's wallet
    const signature = await walletClient.signMessage({ message });

    // Step 3: Verify the signature and complete sign-in
    const { user, isNewUser } = await verifySiweSignature({ flowId, signature });

    console.log(`Signed in as ${user.userId} (${isNewUser ? 'new' : 'returning'} user)`);
  }
  ```
</CodeGroup>

## Parameters

### `signInWithSiwe` options

| Parameter        | Type       | Required | Description                                                                |
| ---------------- | ---------- | -------- | -------------------------------------------------------------------------- |
| `address`        | `string`   | Yes      | ERC-55 checksummed Ethereum address of the user                            |
| `chainId`        | `number`   | Yes      | EIP-155 chain ID (e.g. `1` for Ethereum mainnet)                           |
| `domain`         | `string`   | Yes      | RFC 3986 authority of your app (e.g. `"example.com"`)                      |
| `uri`            | `string`   | Yes      | RFC 3986 URI of the resource being accessed (e.g. `"https://example.com"`) |
| `statement`      | `string`   | No       | Human-readable ASCII assertion shown to the user                           |
| `resources`      | `string[]` | No       | Additional URIs the user acknowledges                                      |
| `idempotencyKey` | `string`   | No       | Safe retry key                                                             |

### `signInWithSiwe` result

| Field            | Type     | Description                                          |
| ---------------- | -------- | ---------------------------------------------------- |
| `message`        | `string` | EIP-4361-formatted message for the user to sign      |
| `flowId`         | `string` | Pass this to `verifySiweSignature`                   |
| `nonce`          | `string` | Cryptographic nonce embedded in the message          |
| `expirationTime` | `string` | ISO 8601 timestamp after which the challenge expires |

### `verifySiweSignature` options

| Parameter        | Type     | Required | Description                                                  |
| ---------------- | -------- | -------- | ------------------------------------------------------------ |
| `flowId`         | `string` | Yes      | The `flowId` returned by `signInWithSiwe`                    |
| `signature`      | `string` | Yes      | ERC-191 hex signature (`0x`-prefixed) from the user's wallet |
| `idempotencyKey` | `string` | No       | Safe retry key                                               |

### `verifySiweSignature` result

| Field       | Type      | Description                                |
| ----------- | --------- | ------------------------------------------ |
| `user`      | `User`    | The authenticated user object              |
| `message`   | `string`  | Confirmation message                       |
| `isNewUser` | `boolean` | `true` if this is the user's first sign-in |

## Optional message fields

You can include a `statement` to display a human-readable action the user is approving, and `resources` to enumerate URIs the user acknowledges:

```typescript theme={null}
const { message, flowId } = await signInWithSiwe({
  address: '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045',
  chainId: 1,
  domain: 'example.com',
  uri: 'https://example.com',
  statement: 'Sign in to Example App to access your wallet.',
  resources: ['https://example.com/terms', 'https://example.com/privacy'],
});
```

The resulting EIP-4361 message will include these fields, making the user's intent explicit in the signature payload.

<Warning>
  **Challenge expiration:** The signed message must be submitted to `verifySiweSignature` before the `expirationTime` returned in step 1. Expired challenges will be rejected.
</Warning>

## What to read next

* **[Authentication Methods](/embedded-wallets/authentication-methods)**: Overview of all authentication options
* **[Auth Method Linking](/embedded-wallets/auth-method-linking)**: Link SIWE to email, SMS, or OAuth on the same wallet
* **[Session Management](/embedded-wallets/session-management)**: Understand session lifecycle and token management
* **[Implementation Guide](/embedded-wallets/implementation-guide)**: Step-by-step integration patterns

