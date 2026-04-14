# Embedded Wallets
Source: https://docs.cdp.coinbase.com/api-reference/v2/rest-api/embedded-wallets/embedded-wallets



The Embedded Wallet APIs enable end users to directly create, manage, and use their accounts. They are typically accessed via the CDP Web SDK. End users authenticate with the APIs via the `InitiateAuthentication` endpoint, and use the returned access token and refresh token to authenticate with the other endpoints. The Embedded Wallet APIs offer end users full control over their accounts, including the ability to sign transactions and messages, and to export their accounts' private keys.

There are three authentication credentials involved in the Embedded Wallet APIs:

1. **Access Token**: A JWT signed by CDP, encoded in base64. This is used to identify the end user, and is
   issued after the end user has signed in using one of the provided authentication methods.
   The APIs provide multiple mechanisms for end user authentication, including custom auth JWT authentication,
   email one-time-password (OTP) authentication, and social sign-in.

2. **Refresh Token**: A cryptographically random string, set as the `cdp_refresh_token` cookie in the end user's browser.
   By hitting the `RefreshAccessToken` endpoint, the included refresh token can be used to obtain a new access token
   without requiring the end user to sign in again.

3. **Temporary Wallet Secret (TWS)**: Requests to signing-related endpoints must also be authenticated using a
   **Temporary Wallet Secret** (TWS) generated on the end user's browser/device. Typically, this is done using the CDP Embedded Wallet SDK. The Temporary Wallet Secret
   follows similar semantics to the Wallet Secret used by the EVM and Solana Account APIs, with the following key differences:

* The end user must register their TWS with the End User Accounts APIs before it can be used.
* Temporary Wallet Secrets have a time-to-live (TTL) defined by the `validUntil` field in the TWS registration request.
* A maximum of five TWS's can be registered for a single end user at any given time.

