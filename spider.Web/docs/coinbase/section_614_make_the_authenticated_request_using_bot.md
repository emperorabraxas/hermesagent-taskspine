# Make the authenticated request using both JWT tokens
curl -L -X ${REQUEST_METHOD} "${API_ENDPOINT}" \
  -H "Authorization: Bearer ${JWT}" \
  -H "X-Wallet-Auth: ${WALLET_AUTH_JWT}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d "${REQUEST_BODY}"
```

This example uses the environment variables we set earlier.

## What to read next

* **[Security Best Practices](/get-started/authentication/security-best-practices)**: Learn how to secure your API keys and other sensitive information.
* **[CDP API Keys](/get-started/authentication/cdp-api-keys)**: Learn how to create and manage your API keys.
* **[JWT Authentication](/get-started/authentication/jwt-authentication)**: More information on JWT authentication.
* **[CDP cURL](/get-started/authentication/cdp-curl)**: Learn how to use our CLI tool to interact with the CDP API.
* **[Postman Files](/get-started/authentication/postman-files)**: Download our Postman collection and environment files to get started.

