# Coinbase App Rate Limiting
Source: https://docs.cdp.coinbase.com/coinbase-app/api-architecture/rate-limiting



The Coinbase App API is rate limited to prevent abuse that would degrade our ability to maintain consistent API performance for all users.

By default, each API key or OAuth-authenticated Coinbase user is rate limited to **10,000** requests per hour.

For apps using OAuth, rate limits scale with the number of unique Coinbase users who have granted access where each authorized user is allotted **10,000** requests per hour.

If you exceed your rate limit, you'll receive an HTTP `429` response with a `rate_limit_exceeded error`.

> Rate limiting error (429)

```json lines wrap theme={null}
{
  "errors": [
    {
      "id": "rate_limit_exceeded",
      "message": "Too many requests"
    }
  ]
}
```

