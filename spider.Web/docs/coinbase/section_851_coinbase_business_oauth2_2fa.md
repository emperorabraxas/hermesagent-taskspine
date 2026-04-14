# Coinbase Business OAuth2 2FA
Source: https://docs.cdp.coinbase.com/coinbase-business/authentication-authorization/oauth2/2fa



OAuth2 authentication requires two-factor authentication (2FA) when debiting funds with the `wallet:transactions:send` scope.

When 2FA is required, the API responds with a `402` status and [`two_factor_required` error](/coinbase-app/api-architecture/error-messages). To successfully complete the request, you must make the same request again with the user's 2FA token in the `CB-2FA-TOKEN` header together with the current access token.

Here's a step by step example:

1. User sends funds and the app calls [`POST api.coinbase.com/v2/accounts/primary/transactions`](/coinbase-app/track-apis/transactions).
2. Server responds with `402` and sends the user a 2FA token via SMS if he doesn't have Authy installed.
3. App re-plays the request from step 1 with exactly same parameters and the 2FA token in the `CB-2FA-TOKEN` header.
4. Transaction is sent and `201 CREATED` status code is returned.

<Warning>
  2FA tokens expire quickly, so you must re-try the request after the user supplies their token.
</Warning>

Two-factor authentication affects only users who have 2FA enabled in their user settings. Those settings determine whether the token is delivered via SMS, or if the user must obtain the 2FA token from their Authy application.

