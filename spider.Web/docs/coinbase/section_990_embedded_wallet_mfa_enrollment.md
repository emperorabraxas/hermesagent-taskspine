# Embedded Wallet: MFA Enrollment
Source: https://docs.cdp.coinbase.com/embedded-wallets/mfa/enrollment



<Tags />

MFA enrollment is a one-time setup process where users add an authenticator app or phone number to their account. Users can enroll in both methods for backup.

## Choose your approach

<CardGroup>
  <Card title="Pre-built components" icon="puzzle-piece" href="#ready-to-use-components-recommended">
    Drop-in React UI with polished design. **Best for most apps.**
  </Card>

  <Card title="React hooks" icon="code" href="#custom-uis-using-react-hooks">
    Build custom UI with React. **For full control over the enrollment flow.**
  </Card>

  <Card title="Core SDK" icon="terminal" href="#direct-api-calls-for-non-react">
    Direct API calls. **For non-React apps.**
  </Card>
</CardGroup>

### Ready-to-use components (recommended)

[`@coinbase/cdp-react`](/embedded-wallets/react-components) provides ready-to-use components with a polished UI.

<Note>
  Pre-built components support both TOTP (authenticator apps) and SMS enrollment. The available methods are determined by your project's [MFA configuration](/embedded-wallets/mfa/overview#configuration).
</Note>

```tsx theme={null}
import { EnrollMfaModal } from "@coinbase/cdp-react";

function App() {
  return (
    <EnrollMfaModal onEnrollSuccess={() => console.log("Enrolled!")}>
      <button>Set up MFA</button>
    </EnrollMfaModal>
  );
}
```

<Note>
  For controlled modals, see the [EnrollMfaModal component reference](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/EnrollMfaModal). For custom layouts or embedding enrollment in non-modal containers, see the [EnrollMfa component reference](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-react/Components/EnrollMfa.README).
</Note>

### Custom UIs using React Hooks

For custom UI or SMS enrollment, use hooks from [`@coinbase/cdp-hooks`](/embedded-wallets/react-hooks).

Enrollment is a two-step process:

1. **Initiate** — Call `useInitiateMfaEnrollment` to start enrollment (returns QR code for TOTP, sends SMS for text message)
2. **Submit** — Call `useSubmitMfaEnrollment` with the 6-digit code to complete enrollment

<Tabs>
  <Tab title="TOTP">
    ```tsx theme={null}
    import { useState } from "react";
    import { useInitiateMfaEnrollment, useSubmitMfaEnrollment } from "@coinbase/cdp-hooks";

    function TotpEnrollment() {
      const [qrCodeUrl, setQrCodeUrl] = useState<string | null>(null);
      const { initiateMfaEnrollment } = useInitiateMfaEnrollment();
      const { submitMfaEnrollment } = useSubmitMfaEnrollment();

      async function startEnrollment() {
        // Step 1: Initiate — returns QR code data
        const result = await initiateMfaEnrollment({ mfaMethod: "totp" });
        setQrCodeUrl(result.authUrl); // Display as QR code
        // result.secret → manual entry fallback
      }

      async function completeEnrollment(code: string) {
        // Step 2: Submit — user enters code from authenticator app
        await submitMfaEnrollment({ mfaMethod: "totp", mfaCode: code });
      }

      // Render: QR code from qrCodeUrl, input for code, submit button
    }
    ```
  </Tab>

  <Tab title="SMS">
    ```tsx theme={null}
    import { useState } from "react";
    import { useInitiateMfaEnrollment, useSubmitMfaEnrollment } from "@coinbase/cdp-hooks";

    function SmsEnrollment() {
      const [codeSent, setCodeSent] = useState(false);
      const { initiateMfaEnrollment } = useInitiateMfaEnrollment();
      const { submitMfaEnrollment } = useSubmitMfaEnrollment();

      async function startEnrollment(phoneNumber: string) {
        // Step 1: Initiate — sends SMS to phone number (E.164 format)
        await initiateMfaEnrollment({ mfaMethod: "sms", phoneNumber });
        setCodeSent(true);
      }

      async function completeEnrollment(code: string) {
        // Step 2: Submit — user enters code from SMS
        await submitMfaEnrollment({ mfaMethod: "sms", mfaCode: code });
      }

      // Render: phone input, send button, then code input + verify button
    }
    ```
  </Tab>
</Tabs>

<Note>
  For complete UI implementations with error handling, loading states, and form validation, see the [MFA section in the cdp-hooks reference](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks#multi-factor-authentication-mfa).
</Note>

### Direct API calls for non-React

For non-React applications, use functions from [`@coinbase/cdp-core`](/embedded-wallets/quickstart).

<Tabs>
  <Tab title="TOTP">
    ```typescript theme={null}
    import { initiateMfaEnrollment, submitMfaEnrollment } from "@coinbase/cdp-core";

    // Step 1: Initiate — returns QR code data
    const enrollment = await initiateMfaEnrollment({ mfaMethod: "totp" });
    // enrollment.authUrl → use with any QR code library
    // enrollment.secret → manual entry fallback

    // Step 2: Submit — user enters code from authenticator app
    await submitMfaEnrollment({ mfaMethod: "totp", mfaCode: "123456" });
    ```
  </Tab>

  <Tab title="SMS">
    ```typescript theme={null}
    import { initiateMfaEnrollment, submitMfaEnrollment } from "@coinbase/cdp-core";

    // Step 1: Initiate — sends SMS to phone number (E.164 format)
    await initiateMfaEnrollment({ mfaMethod: "sms", phoneNumber: "+14155552671" });

    // Step 2: Submit — user enters code from SMS
    await submitMfaEnrollment({ mfaMethod: "sms", mfaCode: "123456" });
    ```
  </Tab>
</Tabs>

<Note>
  For full API details, see the [cdp-core reference](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core).
</Note>

## Checking enrollment status

Before prompting users to enroll, check if they already have MFA enabled.

<Tabs>
  <Tab title="React">
    ```tsx theme={null}
    import { useCurrentUser } from "@coinbase/cdp-hooks";
    import { getEnrolledMfaMethods, isEnrolledInMfa } from "@coinbase/cdp-core";

    function MyComponent() {
      const { currentUser } = useCurrentUser();

      if (!currentUser) return null;

      const hasMfa = isEnrolledInMfa(currentUser);
      const methods = getEnrolledMfaMethods(currentUser);
      // methods: ['totp'], ['sms'], ['totp', 'sms'], or []

      // Use hasMfa and methods to drive your UI
    }
    ```
  </Tab>

  <Tab title="Core SDK">
    ```typescript theme={null}
    import { getCurrentUser, getEnrolledMfaMethods, isEnrolledInMfa } from "@coinbase/cdp-core";

    const user = await getCurrentUser();

    // Check if user has any MFA method enrolled
    const hasMfa = isEnrolledInMfa(user);

    // Get list of enrolled methods
    const methods = getEnrolledMfaMethods(user);
    // methods: ['totp'], ['sms'], ['totp', 'sms'], or []

    // Check specific method
    isEnrolledInMfa(user, "totp"); // true or false
    isEnrolledInMfa(user, "sms");  // true or false
    ```
  </Tab>
</Tabs>

## Validating phone numbers

For SMS enrollment, validate phone numbers before submission:

```typescript theme={null}
import { validatePhoneNumber } from "@coinbase/cdp-core";

try {
  validatePhoneNumber("+14155552671"); // Valid
  validatePhoneNumber("+442071838750"); // Valid (UK)
  validatePhoneNumber("4155552671");    // Throws - missing +
} catch (error) {
  console.error(error.message);
}
```

<Accordion title="E.164 format requirements">
  * Must start with `+` followed by country code
  * No spaces, hyphens, or parentheses
  * Examples: `+14155552671` (US), `+442071838750` (UK), `+81312345678` (Japan)
</Accordion>

## Troubleshooting

<AccordionGroup>
  <Accordion title="Invalid TOTP code">
    **Common causes:**

    * Time synchronization issues between device and server
    * User entering an expired code (TOTP codes refresh every 30 seconds)
    * Incorrect authenticator app setup

    **Solutions:**

    * Ensure device time is synchronized with network time
    * Ask users to wait for a new code and try again
    * Provide option to re-enroll in MFA
    * Verify the QR code was scanned correctly during enrollment
  </Accordion>

  <Accordion title="SMS not received">
    **Common causes:**

    * Invalid phone number format (not E.164)
    * Carrier delays or filtering
    * Phone number not capable of receiving SMS
    * Rate limiting exceeded

    **Solutions:**

    * Validate phone number format before submission using `validatePhoneNumber()`
    * Provide clear error messages for rate limiting
    * Offer TOTP as alternative method
    * Allow users to check and update their phone number
  </Accordion>

  <Accordion title="Invalid phone number format">
    **Error message:**
    `Invalid phone number format. Phone number must be in E.164 format (e.g., +14155552671)`

    **Solutions:**

    * Use E.164 format: `+[country code][subscriber number]`
    * Examples:
      * US: `+14155552671`
      * UK: `+442071838750`
      * Japan: `+81312345678`
    * Remove any spaces, hyphens, or parentheses
    * Must start with `+` and country code (never `0`)
    * Use `validatePhoneNumber()` helper to validate before submission
  </Accordion>

  <Accordion title="Lost authenticator app or phone access">
    **Recovery options:**

    * If user has both TOTP and SMS enrolled, they can use the other method
    * Implement account recovery through primary authentication method
    * Allow MFA reset after verifying via email or other auth method
    * Provide customer support flow for account recovery
    * Consider implementing backup codes for recovery (future enhancement)
  </Accordion>
</AccordionGroup>

