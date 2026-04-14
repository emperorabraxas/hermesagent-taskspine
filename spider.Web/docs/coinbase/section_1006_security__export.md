# Security & Export
Source: https://docs.cdp.coinbase.com/embedded-wallets/security-export



## Overview

While Embedded Wallets are designed to eliminate the complexity of private key management for users, there are scenarios where developers may need to export private keys for wallet migration, user preference, or other legitimate use cases. This page covers the security considerations, implementation, and best practices for handling private key exports.

<Warning>
  Private key export is a high-risk operation that should be implemented with extreme caution. Exported private keys provide complete control over wallet funds and should never be logged, displayed, or transmitted insecurely.
</Warning>

## Prerequisites

* A [CDP Portal](https://portal.cdp.coinbase.com/) account and project
* Embedded Wallets enabled in your project with [configured domains](/embedded-wallets/domains)
* [`@coinbase/cdp-react`](https://www.npmjs.com/package/@coinbase/cdp-react) installed and configured
* User successfully authenticated with embedded wallet

<Note>
  **Privacy Notice**: This feature uses a strictly necessary, 1st party Coinbase cookie to grant end users new refresh tokens with a 7-day expiry. You may need to include this information in your privacy policy for user transparency.
</Note>

## When to consider

Private key export should only be considered in specific scenarios:

<AccordionGroup>
  <Accordion title="Valid use cases">
    * **Wallet migration**: Users need to import a wallet into another wallet or application
    * **User preference**: Users specifically request full custody of their private keys
    * **Account recovery**: Users need to recover access when other authentication methods fail
    * **General export**: Users want to export their keys for any legitimate purpose
  </Accordion>

  <Accordion title="Invalid use cases">
    * **Debugging**: Never export keys for troubleshooting
    * **Analytics**: Never export keys for analytics or logs
    * **Backup storage**: Don't export keys to store as backups on your servers
    * **Default behavior**: This should never be automatic or default functionality
  </Accordion>
</AccordionGroup>

## Best practices

<Warning>
  **Critical security principles:**

  * **Private keys provide complete wallet control**: Anyone with the private key can access all funds
  * **This is a high-risk operation**: Implement with extreme caution and clear user warnings
</Warning>

1. **Never log or store private keys in plaintext**
   * Avoid console.log, file logging, or unencrypted persistent storage
   * Clear private key variables from memory when done
   * Let the browser's garbage collector handle cleanup

2. **Require explicit user consent**
   * Don't make key export automatic or hidden
   * Show clear security warnings before export
   * Make the export process deliberate, not accidental

3. **Use secure UI patterns**
   * Clipboard copy is safer than displaying keys on screen
   * Provide clear instructions for secure handling
   * Consider offering alternatives like asset transfer when appropriate

4. **Educate users on security**
   * Explain what private keys are and why they're sensitive
   * Provide guidance on secure storage options
   * Link to general wallet security resources

### For users

For comprehensive guidance on private key security and storage best practices, refer to [Coinbase's guide on private key security](https://www.coinbase.com/learn/crypto-basics/what-is-a-private-key).

## Export scenarios

Here are common scenarios where users might need to export their private keys from embedded wallets. Each scenario should be implemented with the security measures outlined above.

<AccordionGroup>
  <Accordion title="Wallet migration to external providers">
    * Users want to import their account into third-party wallet applications
    * Copy the exported private key to clipboard for secure transfer
    * Provide clear instructions for the import process in the destination wallet
  </Accordion>

  <Accordion title="Hardware wallet import">
    * Users can import the private key into compatible hardware wallets
    * Note: This reduces some hardware wallet security benefits since the key was previously software-based
    * Recommend this primarily for users who want to upgrade their security model
  </Accordion>

  <Accordion title="Cold storage creation">
    * Users create offline paper wallets or other cold storage solutions
    * Suitable for long-term storage of funds with minimal transaction needs
    * Emphasize the importance of secure physical storage
  </Accordion>
</AccordionGroup>

## Implementation

The SDK provides a secure, built-in UI component for wallet export that handles all security warnings, confirmations, and private key management automatically. This is the recommended approach as it ensures consistent security practices across all implementations.

### Why use the secure export component

The `ExportWalletModal` component provides critical security features that protect both you and your users:

<AccordionGroup>
  <Accordion title="Runs in a secure iframe">
    * The export flow operates within an isolated, sandboxed environment
    * Prevents your application code from accessing or intercepting the private key
    * Protects against malicious scripts or compromised dependencies
  </Accordion>

  <Accordion title="Only end users can copy the private key">
    * The private key is copied to the clipboard in a secure UI that only the user can interact with
    * Your application cannot programmatically access or copy the key
    * Ensures true user consent and control over their private key
  </Accordion>

  <Accordion title="Private key never loads in application memory">
    * The private key stays isolated within the secure iframe
    * Your application's JavaScript context never has access to the raw key material
    * Eliminates the risk of accidental logging, memory dumps, or debugger access
  </Accordion>
</AccordionGroup>

<Warning>
  The `exportEvmAccount` and `exportSolanaAccount` core actions and `useExportEvmAccount` and `useExportSolanaAccount` React hooks are deprecated.
  Using the `ExportWalletModal` component is the recommended approach, and will soon be required.
</Warning>

### Using the secure export component

<Tabs>
  <Tab title="EVM">
    ```tsx theme={null}
    import { useEvmAddress, ExportWalletModal } from "@coinbase/cdp-react";

    const Export = () => {
      const { evmAddress } = useEvmAddress();

      if (!evmAddress) return null;

      return (
        <ExportWalletModal address={evmAddress} />
      );
    };
    ```
  </Tab>

  <Tab title="Solana">
    ```tsx theme={null}
    import { useSolanaAddress, ExportWalletModal } from "@coinbase/cdp-react";

    const Export = () => {
      const { solanaAddress } = useSolanaAddress();

      if (!solanaAddress) return null;

      return (
        <ExportWalletModal address={solanaAddress} />
      );
    };
    ```
  </Tab>
</Tabs>

The `ExportWalletModal` component:

* Displays appropriate security warnings and confirmations
* Securely handles the private key export flow
* Provides a safe UI for the end user to copy the private key
* Works with both EVM and Solana addresses

The `address` prop is required and accepts either an EVM address or Solana address.

## What to read next

* **[React Hooks](/embedded-wallets/react-hooks)** - Learn about all available hooks for embedded wallet operations
* **[CDP SDK Documentation](/sdks/cdp-sdks-v2/frontend)** - Complete SDK reference and API documentation
* **[Smart Accounts](/embedded-wallets/smart-accounts)** - Explore account abstraction as an alternative to private key management
* **[Authentication Methods](/embedded-wallets/authentication-methods)**: Learn about available authentication options
* **[Best Practices](/embedded-wallets/best-practices)**: Security recommendations and production readiness

