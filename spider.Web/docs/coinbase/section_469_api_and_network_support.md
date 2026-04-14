# API and Network Support
Source: https://docs.cdp.coinbase.com/api-reference/payment-apis/supported-networks-assets

API and network support for CDP Payments API.

## By product

Payment API features and network support vary depending on whether you're using [Coinbase Business](/coinbase-business/introduction/welcome) for business payments and trading, or [Coinbase Prime](/prime/introduction/welcome) for institutional-grade brokerage.

| Feature                      | Coinbase Business            | Coinbase Prime               |
| ---------------------------- | ---------------------------- | ---------------------------- |
| **Accounts API**             | <Icon icon="circle-check" /> | <Icon icon="circle-check" /> |
| **Deposit Destinations API** | <Icon icon="circle-check" /> | <Icon icon="circle-check" /> |
| **Payment Methods API**      | -                            | <Icon icon="circle-check" /> |
| **Transfers API**            | <Icon icon="circle-check" /> | <Icon icon="circle-check" /> |
| **Webhooks API**             | <Icon icon="circle-check" /> | <Icon icon="circle-check" /> |

<Info>
  **Accounts:** In Production, Coinbase Business and Coinbase Prime both support creating accounts via CDP Portal, not APIs. The Accounts API is for listing and viewing account details.

  **Payment Methods:** Currently only available for Coinbase Prime accounts linked to CDP. Payment methods allow you to transfer funds to external bank accounts via Fedwire (domestic USD) or SWIFT (international).
</Info>

## By asset and network

The table below shows which crypto networks and assets are supported by CDP Payments APIs. Use the **Network identifier** when specifying a network in API requests.

| Network  | Network identifier | Coinbase Business | Coinbase Prime |
| -------- | ------------------ | ----------------- | -------------- |
| Aptos    | `aptos`            | USDC              | -              |
| Arbitrum | `arbitrum`         | -                 | USDC           |
| Base     | `base`             | USDC              | USDC           |
| Ethereum | `ethereum`         | USDC              | USDC           |
| Optimism | `optimism`         | USDC              | USDC           |
| Polygon  | `polygon`          | USDC              | -              |
| Solana   | `solana`           | USDC              | USDC           |
| Sui      | `sui`              | USDC              | -              |

<Warning>
  Only send **supported assets** to your deposit destinations. While other tokens and crypto deposits may be accepted at these addresses, we cannot guarantee their support.

  Sending unsupported assets may result in loss of funds. If you accidentally send unsupported crypto, you may be able to recover it using Coinbase's [asset recovery service](https://help.coinbase.com/en/coinbase/trading-and-funding/sending-or-receiving-cryptocurrency/recover-unsupported-crypto).
</Warning>

