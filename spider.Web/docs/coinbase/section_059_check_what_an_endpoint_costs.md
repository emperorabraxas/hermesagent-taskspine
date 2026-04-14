# Check what an endpoint costs
npx awal@latest x402 details https://example.com/api/weather
```

## Next steps

Once you've found a service, use the [pay-for-service](/agentic-wallet/skills/pay-for-service) skill to make a paid request.

## Error handling

| Error                                | Resolution                                          |
| ------------------------------------ | --------------------------------------------------- |
| "CDP API returned 429"               | Rate limited; cached data will be used if available |
| "No X402 payment requirements found" | URL may not be an x402 endpoint                     |

