# Trading Balance
Source: https://docs.cdp.coinbase.com/prime/concepts/trading-balance



Coinbase Prime includes multiple wallet types with different operational behaviors. This page covers Trading Balance wallets, which use an omnibus (pooled) model, and how they differ from Vault wallets, which use a segregated model. For a refresher on Wallet Types and Wallet IDs, see the [Wallets Overview](/prime/concepts/wallets/wallets-overview) page.

## Wallet Types

A Trading Balance is designed for trading and uses an omnibus/pooled model. Funds are held together, with ownership tracked as separate balances on an internal Coinbase Prime ledger. Each asset within a portfolio has exactly one Trading Wallet ID, and balances are directly available for trading.

A Vault wallet is designed for offline, segregated storage. Multiple Vault wallets can be created per asset, and each has its own Wallet ID. To learn more about creating Vault wallets, see [Creating a Wallet](/prime/concepts/wallets/wallets-overview#creating-a-wallet).

## Omnibus Model

Trading Balance wallets use a pooled model with internal ledgering. This means onchain funds are not necessarily isolated per client or per portfolio at the address level. Instead, Prime tracks allocation by maintaining separate internal ledger balances per portfolio, wallet, and asset. Coinbase maintains the majority of assets held by Trading Balance wallets in offline storage and automatically moves assets to hot wallets based on client activity.

Because of this model, reconciliation should rely on Prime balances and transaction/activity records rather than assuming onchain address-level segregation. For more detail on querying balances, see the [Balances](/prime/concepts/balances) page.

## Trading

Trading uses Trading Balance wallets. Order placement references a portfolio, and the portfolio, product symbol, and side together determine which Trading Balance is used for debits and credits. For details on order placement and execution, see [Trading Overview](/prime/concepts/trading/trading).

## Deposits

Getting deposit instructions for a Trading Balance is possible and is requested using a Wallet ID. Repeated calls for the same Wallet ID return the same deposit address for supported networks — the endpoint does not generate a new address for each request. For more on deposit workflows, see the [Deposits](/prime/concepts/transactions/deposits) page.

Prime also supports generating unique deposit addresses to differentiate deposits into the same Trading Balance. Unique addresses enable deposit attribution and reconciliation while crediting the same underlying balance. This is particularly useful for Crypto-as-a-Service (CaaS) use cases. See [Creating unique deposit addresses](/prime/concepts/transactions/deposits#creating-unique-deposit-addresses) for details.

## Multi-Network Assets

Certain assets support deposits and withdrawals on multiple networks. Transaction records can include network-scoped symbols to represent the specific network used, while Trading Balance totals remain consolidated per asset for trading and balance queries. For more on multinetwork behavior, see the [Multinetwork](/prime/concepts/transactions/multinetwork) page.

## Transfers between Wallet Types

Transfers are created by specifying a source and destination Wallet ID. Prime determines internally how a transfer is settled. For more on creating transfers, see the [Transfers](/prime/concepts/transactions/transfers) page.

## Withdrawals

Trading Balance wallets support concurrent withdrawals. However, Trading Balance withdrawals are subject to rebalancing, which can introduce delays in availability or completion.

Vault wallets support one withdrawal at a time per Vault wallet. Batching is not supported for Vault wallet withdrawals. For full withdrawal workflows, see the [Withdrawals](/prime/concepts/transactions/withdrawals) page.

## Reconciliation

When reconciling Trading Balance activity, use Prime balances (by portfolio and asset) as the source of truth for available trading balances. Use transaction and [activity](/prime/concepts/activities) history for network context, deposit address attribution (including unique deposit addresses), and onchain settlement records for vault-related movements.

Because Trading Balance wallets use a pooled model, a wallet address does not imply segregated storage. Do not assume that a deposit address corresponds to an isolated onchain balance.

