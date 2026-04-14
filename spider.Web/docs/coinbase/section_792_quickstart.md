# Quickstart
Source: https://docs.cdp.coinbase.com/coinbase-app/oauth2-integration/quickstart

Get started with OAuth2 to connect to Coinbase users

<Warning title="OAuth client creation & editing is currently unavailable">
  New OAuth client creation is temporarily disabled. Existing clients will continue to work normally.
</Warning>

## Prerequisites

Before integrating OAuth2, ensure you have the following:

<AccordionGroup>
  <Accordion title="OAuth client access">
    OAuth client creation is currently limited to approved partners. To request access:

    1. Create an account on the [CDP Portal](https://portal.cdp.coinbase.com/)
    2. Contact your Coinbase representative to request OAuth whitelisting
    3. Once approved, you can create OAuth clients under **API Keys > OAuth**

    You can invite team members to your CDP organization to share access.
  </Accordion>

  <Accordion title="Testing requirements">
    OAuth2 testing requires **real Coinbase accounts** as there is no sandbox or test user functionality. All testing occurs in the production environment.

    To test the OAuth flow, you will need:

    * A [Coinbase account](https://www.coinbase.com/signup)
    * Completed identity verification (KYC), which includes providing ID and SSN for US accounts

    <Tip>
      Your team can use a shared Coinbase account for development and testing.
    </Tip>
  </Accordion>

  <Accordion title="Geographic availability">
    OAuth2 integration is primarily designed for **US-based users**. Team members in other regions may face limitations when testing:

    * Some features may not be available in all jurisdictions
    * KYC requirements vary by country
    * Certain API endpoints are US-only
  </Accordion>

  <Accordion title="Firewall allowlisting">
    If your organization requires firewall allowlisting, add the following domains:

    * `api.coinbase.com` — All API requests (auth and feature APIs)
    * `login.coinbase.com` — OAuth authorization flow

    <Info>
      There are no separate staging or non-prod hosts. All development, testing, and production use the same endpoints.
    </Info>
  </Accordion>
</AccordionGroup>

## Overview

This guide walks you through integrating OAuth2 to access Coinbase user accounts:

* Register an OAuth application
* Redirect users to authorize
* Exchange the authorization code for tokens
* Make authenticated API requests

## 1. Register your OAuth application

Go to [CDP Portal OAuth settings](https://portal.cdp.coinbase.com/projects/api-keys/oauth) and create a new OAuth2 application. You'll receive:

* **Client ID**: Public identifier for your application
* **Client Secret**: Keep this secure—never expose in client-side code

## 2. Redirect users to authorize

```bash theme={null}
GET https://login.coinbase.com/oauth2/auth
  ?response_type=code
  &client_id=YOUR_CLIENT_ID
  &redirect_uri=https://your-app.com/callback
  &scope=wallet:accounts:read,wallet:transactions:send
  &state=SECURE_RANDOM_STRING
```

## 3. Exchange code for tokens

```bash theme={null}
curl -X POST https://login.coinbase.com/oauth2/token \
  -d "grant_type=authorization_code" \
  -d "code=AUTHORIZATION_CODE" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "redirect_uri=https://your-app.com/callback"
```

## 4. Make authenticated requests

```bash theme={null}
curl https://api.coinbase.com/v2/accounts \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

## Token lifecycle

| Token Type    | Lifetime  | Usage                     |
| :------------ | :-------- | :------------------------ |
| Access Token  | 1 hour    | Authenticate API requests |
| Refresh Token | 1.5 years | Obtain new access tokens  |

<Warning>
  Refresh tokens can only be used **once**. Each token exchange returns a new refresh token that must be stored for future use.
</Warning>

## What to read next

<CardGroup>
  <Card title="Full integration guide" icon="code" href="/coinbase-app/oauth2-integration/integrations">
    Step-by-step OAuth2 implementation with PKCE
  </Card>

  <Card title="Available scopes" icon="list-check" href="/coinbase-app/oauth2-integration/scopes">
    Complete list of permissions your app can request
  </Card>

  <Card title="Security best practices" icon="shield-check" href="/coinbase-app/oauth2-integration/security-best-practices">
    PKCE, state validation, and secure token storage
  </Card>

  <Card title="Code samples" icon="file-code" href="/coinbase-app/oauth2-integration/oauth2-code-samples">
    Ready-to-use examples in Go, PHP, and more
  </Card>
</CardGroup>

