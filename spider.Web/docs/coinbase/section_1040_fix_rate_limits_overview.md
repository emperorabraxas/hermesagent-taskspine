# FIX Rate Limits Overview
Source: https://docs.cdp.coinbase.com/exchange/fix-api/rate-limits



### FIX 5.0

* 2 logons per second per API key
* 100 requests per second

<Warning>
  Your FIX 5 session is disconnected if your messages exceed 200 messages per second
</Warning>

### FIX Maximums

* Maximum API keys per session/connection: 1
* Maximum connections per profile: 75. See [FIX Best Practices](/exchange/fix-api/best-practices).
* Maximum connections per user across all profiles: 175
* Maximum profiles per user: 100
* Maximum orders per batch message (new and cancelled): 15

## How Rate Limits Work

Rate-limiting for FIX API uses a fixed window implementation.

