# Overview
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/index



This package contains ready-made, customizable React UI components that wrap
the CDP frontend SDK.

## Components

* [SignInModal](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/SignInModal) - a button that triggers a modal with the sign-in flow
* [SignIn](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/SignIn) - the forms for the sign in flow, a logo, heading, and description text
* [SignOutButton](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/SignOutButton) - a sign out button
* [AuthButton](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/AuthButton) - the `SignOutButton` when logged in, and the `SignInModal` when logged out
* [SendEvmTransactionButton](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/SendEvmTransactionButton) - a button that signs and sends an EVM transaction
* [SendSolanaTransactionButton](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/SendSolanaTransactionButton) - a button that signs and sends a Solana transaction
* [Fund](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/Fund) - the fund flow
* [FundModal](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/FundModal) - a button that triggers a modal with the fund flow
* [LinkAuth](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/LinkAuth) - a component to link or unlink auth methods
* [LinkAuthModal](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/LinkAuthModal) - a button that triggers a modal with the link / unlink flow
* [CopyAddress](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/CopyAddress) - a component that renders a truncated address with a copy button
* [CopyEvmKeyButton](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/CopyEvmKeyButton) - a button for copying the private key of a user's EVM EOA address
* [CopySolanaKeyButton](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/CopySolanaKeyButton) - a button for copying the private key of a user's Solana address
* [ExportWallet](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/ExportWallet) - a component for exporting a user's wallet; includes a title, a warning about keeping private keys secure, the CopyAddress component, and either the CopyEvmKeyButton or CopySolanaKeyButton depending on the type of address provided
* [ExportWalletModal](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/ExportWalletModal) - a button that triggers a modal with the ExportWallet component
* [EnrollMfa](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/EnrollMfa) - a component for MFA enrollment; guides users through setting up two-factor authentication via TOTP
* [EnrollMfaModal](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/EnrollMfaModal) - a button that triggers a modal with the MFA enrollment flow
* [VerifyMfa](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/VerifyMfa) - a component for MFA verification; prompts enrolled users to enter their authenticator code
* [VerifyMfaModal](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/VerifyMfaModal) - a button that triggers a modal with the MFA verification flow
* [VerifyMfaInline](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/VerifyMfaInline) - a wrapper component for embedding MFA verification within existing UI flows

## Quickstart

This guide will help you get started with `@coinbase/cdp-react`. You'll learn how to install the package, set up the provider, and render your first component.

### Installation

First, add the package to your project using your preferred package manager.

```bash theme={null}