# Create webhook subscription
Source: https://docs.cdp.coinbase.com/api-reference/payment-apis/rest-api/webhooks-under-development/create-webhook-subscription

post /v2/data/webhooks/subscriptions
Subscribe to real-time events across CDP products using flexible filtering.

### Event Types

**Onchain Events** - Monitor Base mainnet with microsecond precision:
- `onchain.activity.detected` - Smart contract events, transfers, swaps, NFT activity
- **Requires** `labels` for filtering (e.g., `contract_address`, `event_name`)

**Onramp/Offramp Events** - Transaction lifecycle notifications:
- `onramp.transaction.created`, `onramp.transaction.updated`
- `onramp.transaction.success`, `onramp.transaction.failed`
- `offramp.transaction.created`, `offramp.transaction.updated`
- `offramp.transaction.success`, `offramp.transaction.failed`
- **No labels required** - maximum simplicity for transaction monitoring

**Payments Transfers Events** - Transfer lifecycle notifications:
- `payments.transfers.quoted` - Transfer created and awaiting execution
- `payments.transfers.processing` - Transfer execution in progress
- `payments.transfers.completed` - Transfer completed successfully
- `payments.transfers.failed` - Transfer failed
- `payments.transfers.travel_rule_incomplete` - Travel rule information is missing
- `payments.transfers.travel_rule_completed` - Travel rule information has been provided and the transfer will proceed
- **No labels required** - enable the transfers webhook to monitor status transitions

**Wallet Events** - Wallet activity notifications:
- `wallet.activity.detected`

### Webhook Signature Verification
All webhooks include cryptographic signatures for security.
The signature secret is returned in `secret` field when creating a subscription.

**Note:** Webhooks are in beta and this interface is subject to change.

See the [verification guide](https://docs.cdp.coinbase.com/onramp-&-offramp/webhooks#webhook-signature-verification) for implementation details.

### Onchain Label Filtering

For `onchain.activity.detected` events, use `labels` for precise filtering with AND logic (max 20 labels per webhook).

**Allowed labels** (all in snake_case format):
- `network` (required) - Blockchain network
- `contract_address` - Smart contract address
- `event_name` - Event name (e.g., "Transfer", "Burn")
- `event_signature` - Event signature hash
- `transaction_from` - Transaction sender address
- `transaction_to` - Transaction recipient address
- `params.*` - Any event parameter (e.g., `params.from`, `params.to`, `params.sender`, `params.tokenId`)

**Examples**:
- **Liquidity Pool Monitor**: `{"network": "base-mainnet", "contract_address": "0xcd1f9777571493aeacb7eae45cd30a226d3e612d", "event_name": "Burn"}`
- **Price Oracle Tracker**: `{"network": "base-mainnet", "contract_address": "0xbac4a9428ea707c51f171ed9890c3c2fa810305d", "event_name": "PriceUpdated"}`
- **DeFi Protocol Activity**: `{"network": "base-mainnet", "contract_address": "0x45c6e6a47a711b14d8357d5243f46704904578e3", "event_name": "Deposit"}`



