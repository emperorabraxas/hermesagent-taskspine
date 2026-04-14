# Advanced Trade International Derivatives
Source: https://docs.cdp.coinbase.com/coinbase-app/advanced-trade-apis/guides/perpetual



The Advanced Trade API supports trading for International Derivatives products (a.k.a. INTX perpetuals) via the following endpoints (for users in eligible regions):

* [Order Management](/api-reference/advanced-trade-api/rest-api/orders/create-order)
* [Market Data](/api-reference/advanced-trade-api/rest-api/products/get-best-bid-ask)
* [Perpetuals-specific](/api-reference/advanced-trade-api/rest-api/perpetuals/get-perpetuals-portfolio-summary)

For an overview of our perpetual futures trading offering, see the Coinbase [help pages](https://help.coinbase.com/en/coinbase/trading-and-funding/derivatives/pf-intro).

<Info>
  eligibility

  To use the Advanced Trade API, you must be in an eligible region and successfully [onboard](#onboarding-requirements). In addition, all perpetual orders are subject to a 10 USDC min notional value.
</Info>

## API Authentication

[Advanced Trade REST API Authentication](/coinbase-app/advanced-trade-apis/rest-api) explains how to authenticate requests to the Advanced REST API endpoints and WebSocket server channels.

## Onboarding Requirements

For users in eligible regions, getting access to perpetual futures functionality requires completing a few additional onboarding steps in our [Advanced Trade UI](https://www.coinbase.com/advanced-trade/perpetuals/BTC-PERP-INTX), from the right-hand side of the BTC-PERP market page.

## Transferring Collateral for Margin

To trade perpetual futures, you must have USDC in your perpetuals portfolio to use as margin. You can transfer any existing USDC in your default portfolio to your perpetuals portfolio with the [Move Portfolio Funds](/api-reference/advanced-trade-api/rest-api/portfolios/move-portfolios-funds) endpoint.

## Multi-Asset Collateral

To use Bitcoin and Ethereum as collateral for your perpetual futures trades, you can opt-in to the multi-asset collateral feature with the [Opt-In Multi-Asset Collateral](/api-reference/advanced-trade-api/rest-api/perpetuals/opt-in-or-out) endpoint.

## Perp Listings, Leverage, & Order Types

We regularly update our perp listings for trading and support up to a max of 10x leverage. You can always see our current listings on the [International Exchange](https://international.coinbase.com/?tab=derivatives).

<Info>
  We support both Market and Limit orders and are actively working on adding more order types.
</Info>

## Margin Health Management

For each of your [open positions](/api-reference/advanced-trade-api/rest-api/perpetuals/list-perpetuals-positions), we provide information to track your current margin and maintenance margin, and understand your liquidation thresholds.

## Trading Fees

You can view your current trading fees on the Coinbase [Advanced Portfolio](https://www.coinbase.com/advanced-portfolio) Page

<Info>
  Currently, we offer low promotional fee rates of 0.00% maker and 0.03% taker.
</Info>

## Quick Start

Make your first perpetual futures trade with the following steps:

1. Onboard via [Advanced Trade UI](https://www.coinbase.com/advanced-trade/perpetuals/BTC-PERP-INTX).
2. [Transfer Funds](/api-reference/advanced-trade-api/rest-api/portfolios/move-portfolios-funds) to your Perpetuals Portfolio.
3. [List Perpetual Futures](/api-reference/advanced-trade-api/rest-api/products/get-product) products offered by Coinbase with `product_type` as `future` and `contract_expiry_type` as `perpetual`.
4. Get a summary of your [Perpetuals Portfolio](/api-reference/advanced-trade-api/rest-api/perpetuals/get-perpetuals-portfolio-summary)
5. [Create an Order](/api-reference/advanced-trade-api/rest-api/orders/create-order) to buy or sell a perpetual futures contract.
6. [List your open positions](/api-reference/advanced-trade-api/rest-api/perpetuals/list-perpetuals-positions) and track your margin health.

