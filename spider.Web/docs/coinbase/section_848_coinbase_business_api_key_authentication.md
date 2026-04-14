# Coinbase Business API Key Authentication
Source: https://docs.cdp.coinbase.com/coinbase-business/authentication-authorization/api-key-authentication



**API Key authentication should only be used to access your own account.**  To securely access the accounts of other Coinbase users, use [Coinbase Business (OAuth2)](/coinbase-business/introduction/welcome)

<Info>
  Coinbase Business APIs can be accessed using API Keys created on the Coinbase Development Platform (CDP). See [CDP API keys](#cdp-api-keys).
</Info>

## CDP API keys

Keys created on the Coinbase Development Platform (CDP) may not yet be supported by all third-party applications.

### Creating API Keys

1. Navigate to the Coinbase Developer Platform and select [**Secret API Keys**](https://portal.cdp.coinbase.com/projects/api-keys) under the **API Keys** tab.
2. Click the **Create API key** button.
3. Enter an API key nickname and then expand **API restrictions** and **Advanced Settings**.
4. Enter your IPs in the IP allowlist section *(recommended but not required)*.
5. Set portfolio and permission restrictions.
6. Change signature algorithm to **ECDSA** if you're not developing your own authentication code.
7. Click **Create API key**.
8. Secure your private/public key pair in a safe location.

### Understanding API Key Scopes

When creating an API key, you'll need to select the appropriate permission scopes:

<Frame>
  <img alt="API key scope options" />
</Frame>

* **View (read-only)**: Grants access to APIs that do not move funds out of your Coinbase account. This includes:
  * [Payment Links API](/api-reference/business-api/rest-api/payment-links/introduction) - create, update, and manage payment links
  * [Invoices API](/api-reference/business-api/rest-api/invoicing/introduction) - retrieve invoice details
  * Any endpoints that retrieve account balances, transaction history, or other account data

* **Trade (execute trades on your behalf)**: Allows your API key to execute buy and sell orders. Use this scope when you need to:
  * Place market or limit orders
  * Execute cryptocurrency trades on your account

* **Transfer (initiate transfer of funds)**: Allows your API key to send funds out of your account. Use this scope only when you need to:
  * Create withdrawals or send cryptocurrency to external addresses
  * Initiate transfers between accounts

<Warning>
  Only enable the scopes you need. If your use case only requires reading data (viewing balances, listing transactions, fetching payment links or invoices), the **view** scope provides sufficient access with lower risk.
</Warning>

<Info>
  **Optional API Key File Download**

  For enhanced security, API key files are no longer automatically downloaded. If you need to reference your API key via file path in your code, click the **Download API key** button in the modal to save the key file. Otherwise, you can copy the key details directly from the modal and use them as environment variables (recommended for better security).
</Info>

### Making Requests

CDP API keys are used to generate a JSON Web Token (JWT) for an API. Once you've generated a JWT, set it as a Authorization Bearer header to make an authenticated request.

```shell lines wrap theme={null}