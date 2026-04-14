# Overview
Source: https://docs.cdp.coinbase.com/get-started/authentication/overview



This guide helps you choose the right CDP authentication approach for your use case.

<Info>
  Looking to access **other users'** Coinbase accounts? See [OAuth2 Integration](/coinbase-app/oauth2-integration/overview).
</Info>

<CardGroup>
  <Card title="Building a server-side application?">
    Use **Secret API Keys** with JWT authentication for maximum security and control.

    * ✓ Backend servers
    * ✓ Automated trading systems
    * ✓ Data processing pipelines
  </Card>

  <Card title="Building a client-side application?">
    Use **Client API Keys** for public-facing apps or **OAuth** for user account access.

    * ✓ Web applications
    * ✓ Mobile apps
    * ✓ Browser extensions
  </Card>
</CardGroup>

## 1. Where will you use it?

CDP offers three types of keys based on **where** you'll use them:

| Key Type           | When to Use                                          | Example                            |
| ------------------ | ---------------------------------------------------- | ---------------------------------- |
| **Secret API Key** | Server-side code only (never exposed)                | Backend API, automated trading bot |
| **Client API Key** | Client-side code (can be exposed)                    | React app, mobile app              |
| **OAuth Client**   | When users need to login with their Coinbase account | "Sign in with Coinbase" feature    |

## 2. Choose your key algorithm

When creating a **Secret API Key**, you'll also choose between two cryptographic algorithms:

* **Ed25519** (default, recommended): Newer, faster algorithm
* **ECDSA**: Older algorithm, required for some SDKs. See [product compatibility](#product-compatibility) for more details.

<Tip>
  Use **Ed25519** unless you're using the Coinbase App SDK or Advanced Trade SDK, which only support ECDSA.
</Tip>

<Accordion title="More on key algorithms">
  Both Ed25519 and ECDSA are cryptographic algorithms used to create digital signatures - think of them as ultra-secure ways to prove your identity when making API calls.

  **Ed25519**

  * Based on cutting-edge cryptography
  * Faster signature generation and verification
  * Smaller key size (more efficient)
  * Better resistance to certain types of attacks
  * Default for new CDP API keys as of February 2025

  **ECDSA (Elliptic Curve Digital Signature Algorithm)**

  * Older standard, widely used since early 2000s
  * Well-established and battle-tested
  * Required by some legacy SDKs that haven't updated yet
  * Still secure and fully supported

  **Why do some SDKs only support ECDSA?**

  Some SDKs were built before Ed25519 became available or haven't been updated to support it yet. We're working on adding Ed25519 support across all SDKs.
</Accordion>

## Product compatibility

The following describes which products work with default CDP API keys and which algorithm is supported:

| Product                    | Ed25519 Keys | ECDSA Keys | Documentation                                                                                                       | Notes                                                                                                                          |
| -------------------------- | ------------ | ---------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **CDP APIs**               | ✅            | ✅          | [CDP API Authentication](/api-reference/v2/authentication)                                                          |                                                                                                                                |
| **CDP SDK**                | ✅            | ✅          | [TypeScript](/get-started/authentication/cdp/sdk-typescript) / [Python](/get-started/authentication/cdp/sdk-python) |                                                                                                                                |
| **Advanced Trade API**     | ✅            | ✅          | [Coinbase App API Key Authentication](/coinbase-app/authentication-authorization/api-key-authentication)            | Direct API calls work with both                                                                                                |
| **Advanced Trade SDK**     | ❌            | ✅          | [Coinbase App API Key Authentication](/coinbase-app/authentication-authorization/api-key-authentication)            | Use ECDSA keys only                                                                                                            |
| **AgentKit**               | ✅            | ✅          | [AgentKit Quickstart](/agent-kit/getting-started/quickstart)                                                        | Supports Ed25519 via CDP Server Wallets; [Eliza framework](/agent-kit/core-concepts/frameworks#eliza-framework) requires ECDSA |
| **Coinbase App API**       | ✅            | ✅          | [Coinbase App API Key Authentication](/coinbase-app/authentication-authorization/api-key-authentication)            | Direct API calls work with both                                                                                                |
| **Coinbase App SDK**       | ❌            | ✅          | [Coinbase App API Key Authentication](/coinbase-app/authentication-authorization/api-key-authentication)            | Use ECDSA keys only                                                                                                            |
| **Exchange API**           | ✅            | ✅          | [Exchange Authentication](/exchange/rest-api/authentication)                                                        | Separate key system with passphrase                                                                                            |
| **International Exchange** | ✅            | ✅          | [Intl Exchange Authentication](/international-exchange/websocket-feed/authentication)                               | Separate key system with passphrase                                                                                            |
| **Prime API**              | ✅            | ✅          | [Prime Authentication](/prime/rest-api/authentication)                                                              | Separate key system with passphrase                                                                                            |
| **Sign in with Coinbase**  | ✅            | ✅          | [OAuth Documentation](/get-started/authentication/cdp-api-keys#oauth-client-user-authentication)                    | OAuth flow                                                                                                                     |

<Info>
  **Other Coinbase products**: Exchange, Prime, and International Exchange have their own separate API key systems. See their specific documentation for authentication details
</Info>

### Choosing a key type

* **New projects (default):** Ed25519 keys offer better performance and security
* **Using Advanced Trade SDK or Coinbase App SDK:** Request ECDSA keys during creation
* **Direct API integration:** Either algorithm works perfectly

<Warning>
  **Security reminder**: Never commit API keys to version control. Use environment variables for key storage, implement regular key rotation, and monitor usage for anomalies. Read our full [security best practices](/get-started/authentication/security-best-practices) guide.
</Warning>

## What to read next

* [CDP API authentication](/api-reference/v2/authentication) - Complete implementation guide with code examples
* [CDP API keys](/get-started/authentication/cdp-api-keys) - Set up your authentication credentials
* [JWT authentication](/get-started/authentication/jwt-authentication) - Generate secure authentication tokens
* [Security best practices](/get-started/authentication/security-best-practices) - Keep your keys and applications secure
* [cdpcurl](/get-started/authentication/cdp-curl) - Test API calls from the command line
* [Postman collection](/get-started/authentication/postman-files) - Import pre-configured API requests

