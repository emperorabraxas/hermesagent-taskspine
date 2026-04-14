# Embedded Wallet: Multi-Factor Authentication (MFA)
Source: https://docs.cdp.coinbase.com/embedded-wallets/mfa/overview



<Tags />

## Overview

Multi-Factor Authentication (MFA) adds an extra layer of security to Embedded Wallets by requiring users to verify their identity through a secondary authentication method.

<CardGroup>
  <Card title="TOTP" icon="mobile">
    Time-based codes from authenticator apps like Google Authenticator, Authy, or 1Password
  </Card>

  <Card title="SMS" icon="message-sms">
    Verification codes sent via text message to the user's phone
  </Card>
</CardGroup>

<Tip>
  MFA is optional but strongly recommended for production applications handling significant value or sensitive operations. It provides defense against account takeover attacks even if the primary authentication method is compromised.
</Tip>

These guides will walk you through how to integrate Coinbase Developer Platform's MFA into your application. For more detailed customization options, see the [SDK reference](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks).

## How it works

<Steps>
  <Step title="Enrollment">
    * **Authenticator app**: User scans a QR code and registers the app in their authenticator app
    * **Text message**: User provides their phone number in E.164 format (e.g., `+14155552671`)
  </Step>

  <Step title="Verification">
    * **Authenticator app**: User confirms by entering a 6-digit code
    * **Text message**: User confirms by entering a 6-digit code sent via SMS
  </Step>

  <Step title="Future authentication">
    * **Authenticator app**: User provides a 6-digit code for sensitive operations
    * **Text message**: User receives a new 6-digit code via SMS for sensitive operations
  </Step>
</Steps>

<Note>
  Users must be authenticated (signed in) before they can enroll in MFA. Users can enroll in both TOTP and SMS for maximum flexibility.
</Note>

## Configuration

Configure which MFA methods (TOTP, SMS, or both) are available for your project in the [CDP Portal](https://portal.cdp.coinbase.com/products/embedded-wallets/authentication).

You can update these settings at any time; changes apply to new enrollments only and don't affect users who are already enrolled.

<Note>
  Portal settings only control what the pre-built components display. If you're using [hooks](/embedded-wallets/mfa/enrollment#custom-uis-using-react-hooks) or the [Core SDK](/embedded-wallets/mfa/enrollment#direct-api-calls-for-non-react) directly, you can initiate enrollment for any method regardless of portal configuration.
</Note>

## MFA-protected operations

The following actions automatically trigger MFA verification when the user is enrolled:

<AccordionGroup>
  <Accordion title="EVM">
    * `signEvmHash`
    * `signEvmTypedData`
    * `signEvmMessage`
    * `signEvmTransaction`
    * `sendEvmTransaction`
    * `sendUserOperation`
    * `createEvmKeyExportIframe`
  </Accordion>

  <Accordion title="Solana">
    * `signSolanaMessage`
    * `signSolanaTransaction`
    * `sendSolanaTransaction`
    * `createSolanaKeyExportIframe`
  </Accordion>
</AccordionGroup>

## Supported authenticator apps

Any TOTP-compatible authenticator app works. These are commonly used:

* [Google Authenticator](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2)
* [Microsoft Authenticator](https://play.google.com/store/apps/details?id=com.azure.authenticator)
* [Authy](https://authy.com/)
* [1Password](https://1password.com/)
* [Duo Mobile](https://duo.com/product/multi-factor-authentication-mfa/duo-mobile-app)

## Quickstart

If you're using `@coinbase/cdp-react`, use the pre-built enrollment component to let users enable MFA:

```tsx theme={null}
import { EnrollMfaModal } from "@coinbase/cdp-react";

function Settings() {
  return (
    <EnrollMfaModal onEnrollSuccess={() => console.log("MFA enabled!")}>
      <button>Enable Two-Factor Authentication</button>
    </EnrollMfaModal>
  );
}
```

Once enrolled in MFA, users see a verification modal whenever they attempt a [protected operation](/embedded-wallets/mfa/protected-operations):

```tsx theme={null}
import { CDPReactProvider } from "@coinbase/cdp-react";
import { useSendEvmTransaction } from "@coinbase/cdp-hooks";

function App() {
  return (
    <CDPReactProvider config={{ projectId: "your-project-id" }}>
      <SendButton />
    </CDPReactProvider>
  );
}

function SendButton() {
  const { sendEvmTransaction, isPending } = useSendEvmTransaction();

  const handleSend = async () => {
    // If user is enrolled in MFA, modal appears automatically
    const hash = await sendEvmTransaction({
      to: "0x...",
      value: "1000000000000000000",
    });
  };

  return <button onClick={handleSend} disabled={isPending}>Send</button>;
}
```

That's it! The SDK handles:

1. Detecting when MFA verification is needed
2. Showing the verification modal
3. Completing the operation after successful verification

## What to read next

<CardGroup>
  <Card title="Enrollment" icon="user-plus" href="/embedded-wallets/mfa/enrollment">
    Set up MFA for your users with pre-built components or custom UI
  </Card>

  <Card title="MFA Prompts" icon="shield-check" href="/embedded-wallets/mfa/verification">
    Handle MFA prompts for sensitive operations
  </Card>

  <Card title="Customizing Triggers" icon="sliders" href="/embedded-wallets/mfa/protected-operations">
    Learn what triggers MFA and how to customize behavior
  </Card>

  <Card title="Best Practices" icon="lightbulb" href="/embedded-wallets/best-practices">
    Security recommendations and UX considerations
  </Card>
</CardGroup>

