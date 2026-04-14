# Coinbase App API Key Authentication
Source: https://docs.cdp.coinbase.com/coinbase-app/authentication-authorization/api-key-authentication



**API Key authentication should only be used to access your own account.**  To securely access the accounts of other Coinbase users, use [Coinbase App (OAuth2)](/coinbase-app/introduction/welcome)

<Info>
  API keys for Coinbase App are created through the CDP portal but have specific requirements outlined below.
</Info>

<Tip>
  **Looking for Coinbase Developer Platform (CDP) authentication?**

  This page covers authentication for Coinbase App APIs (consumer account access). If you're building Web3 applications, managing programmatic wallets, or using CDP's  APIs, see the [CDP API Authentication documentation](/api-reference/v2/authentication).
</Tip>

## CDP API keys

Keys created on the Coinbase Development Platform (CDP) may not yet be supported by all third-party applications.

<Warning>
  **Important key type requirement**

  When using Coinbase App SDKs, Ed25519 (EdDSA) keys are **NOT** supported. You must use ES256 key format.

  When creating your API key to use with Coinbase App in step 6 below, you should select **ECDSA** as the signature algorithm. If you select Ed25519, your authentication attempts may fail.
</Warning>

### Creating API Keys

<Info>
  **Optional API Key File Download**

  For enhanced security, API key files are no longer automatically downloaded. If you need to reference your API key via file path in your code, click the **Download API key** button in the modal to save the key file. Otherwise, you can copy the key details directly from the modal and use them as environment variables (recommended for better security).
</Info>

1. Navigate to the Coinbase Developer Platform and select [**Secret API Keys**](https://portal.cdp.coinbase.com/projects/api-keys) under the **API Keys** tab.
2. Click the **Create API key** button.
3. Enter an API key nickname and then expand **API restrictions** and **Advanced Settings**.
4. Enter your IPs in the IP allowlist section *(recommended but not required)*.
5. Set portfolio and permission restrictions.
6. **Required**: Change signature algorithm to **ECDSA**. Do NOT select Ed25519 as it is not supported by Coinbase App APIs.
7. Click **Create API key**.
8. Secure your private/public key pair in a safe location.

### Making Requests

CDP API keys are used to generate a JSON Web Token (JWT) for an API. Once you've generated a JWT, set it as a Authorization Bearer header to make an authenticated request.

```shell lines wrap theme={null}