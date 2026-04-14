# Now, use that endpoint in your curl command
curl -L -X "$HTTP_METHOD" "$API_ENDPOINT" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"
```

### Client

To authenticate your client-side code, include it with your JSON-RPC request:

```bash lines wrap theme={null}
curl -L -X https://api.developer.coinbase.com/rpc/v1/base/${CLIENT_API_KEY} \
  -H "Content-Type: application/json" \
  -d '${REQUEST_BODY_JSON}'
```

As an example, you can request the [List Historical Balances](/api-reference/json-rpc-api/address-history#cdp-listbalancehistories) JSON-RPC endpoint like so:

```bash lines wrap theme={null}
curl -L -X https://api.developer.coinbase.com/rpc/v1/base/${CLIENT_API_KEY} \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "cdp_listBalances", "params": [{"address":"0xF7DCa789B08Ed2F7995D9bC22c500A8CA715D0A8","pageToken":"","pageSize":1}]}'
```

## What to read next

* **[Security Best Practices](/get-started/authentication/security-best-practices)**: Learn how to secure your API keys and other sensitive information.
* **[CDP API Keys](/get-started/authentication/cdp-api-keys)**: Learn how to create and manage your API keys.
* **[JWT Authentication](/get-started/authentication/jwt-authentication)**: More information on JWT authentication.
* **[CDP cURL](/get-started/authentication/cdp-curl)**: Learn how to use our CLI tool to interact with the CDP API.
* **[Postman Files](/get-started/authentication/postman-files)**: Download our Postman collection and environment files to get started.

