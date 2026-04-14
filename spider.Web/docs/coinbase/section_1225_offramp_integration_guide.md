# Offramp Integration Guide
Source: https://docs.cdp.coinbase.com/onramp/offramp/offramp-integration-guide



Offramp lets your users convert crypto into fiat and send funds directly to a bank account (ACH) or a Coinbase account. Follow these steps to create and complete an offramp transaction:

1. Create an offramp transaction by generating an Offramp URL with a session token
2. Create an onchain transaction to send user funds from your App to Coinbase
3. Coinbase process the transaction and deposits into your users account

<Warning>
  **Session tokens:** You must create a new [session token](/api-reference/rest-api/onramp-offramp/create-session-token) from your backend for each user session. Tokens are single-use and expire after 5 minutes.
</Warning>

<Tip>
  **See it live**
  Check out our [Onramp + Offramp Demo App repo](https://github.com/coinbase/onramp-demo-app).
</Tip>

## Step 1: [Generate an Offramp URL](/onramp/offramp/generating-offramp-url) with your parameters

Create a `https://pay.coinbase.com/v3/sell/<params>` URL which you direct your users to. Be sure to include the following parameters:

* `partnerUserRef`: Your App's unique user identifier
* `redirectUrl`: Where users are redirected after submitting an offramp transaction. Add your production URL to your domain allowlist (see [Security Requirements](/onramp/security-requirements)). Localhost URLs work for testing.
* `addresses`: The address of the user cashing out crypto for fiat. This address must contain the funds to be sold when the offramp transaction is created.
* `sessionToken`: used to securely authenticate users and manage sessions.

*Note:* Offramp transactions time out 30 mins after users click the "Cash out now" button in the Coinbase widget. Users must perform the onchain send transaction within this time.

### Example Offramp URL

The URL should look like this:

```bash theme={null}
https://pay.coinbase.com/v3/sell/input?partnerUserRef=userId&redirectUrl=https://homebase.coinbase.com&sessionToken=<token>
```

## Step 2: Create an onchain transaction to send user funds from your App to Coinbase

* Call the [Offramp Transaction Status API](/onramp/offramp/transaction-status#offramp-transaction-status) using `partnerUserRef`.
* Use the returned `sell_amount`, `asset`, `network`, and `to_address` to create an onchain send transaction in your App.
  * Note: `to_address` is a Coinbase managed onchain address where send funds to be offramped
* User signs the send transaction in your App.
* Once this transaction is created, Coinbase will wait for onchain confirmation and process the transaction.

## Step 3: Coinbase processes the transaction and deposits fiat into the user's account!

* Coinbase validates the onchain send transaction to match `from_address`, `to_address`, `amount`, `network`, and `asset`.
  * Note: for offramp transactions on Bitcoin and Bitcoin-based crypto assets (e.g. Zcash – ZEC, Litecoin – LTC, Bitcoin Cash – BCH, DogeCoin-DOGE) we do not validate `from_address` as it changes after every transaction.
* Users will receive a status notification via SMS or email and in their Coinbase App based on the transaction's state:
  * Initiated: eg. "Your sell for \$100.00 of BTC has been started"
  * Success: eg. "You've sold \$100.00 of BTC"
  * Fail: eg. "Your BTC was deposited to your Coinbase account"
* If after the onchain send, the price of the asset falls below the "Receive at least" amount in a user's transaction, Coinbase will cancel the transaction and deposit the full crypto amount in the user's Coinbase account
* Your App can pull the latest offramp transaction status from the [Offramp Transaction Status API](/onramp/offramp/transaction-status#offramp-transaction-status)

## See it live!

Check out our [Onramp + Offramp Demo App](https://github.com/coinbase/onramp-demo-app).
Have questions? Drop us a message in the **#onramp** channel of the [CDP Discord](https://discord.com/invite/cdp)!

## Offramp API Endpoints

The Offramp API has the following endpoints:

| Method                                                                              | Description                                                                                                                                              |
| :---------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Session Token](/onramp/offramp/generating-offramp-url)                             | Provides a secure way for the client to initialize the Onramp and Offramp widget.                                                                        |
| [Offramp Config](/onramp/coinbase-hosted-onramp/countries-&-currencies)             | Returns list of countries supported by Coinbase Offramp, and the payment methods available in each country.                                              |
| [Offramp Options](/onramp/coinbase-hosted-onramp/countries-&-currencies)            | Returns supported fiat currencies and available crypto assets that can be passed into the Offramp Quote API.                                             |
| [Offramp Quote](/onramp/offramp/generating-offramp-url)                             | Provides a quote based on the asset the user would like to sell, plus the network, the crypto amount, the cashout currency, payment method, and country. |
| [Transaction Status](/onramp/offramp/transaction-status#offramp-transaction-status) | Real time transaction status updates.                                                                                                                    |
| [Transactions](/onramp/offramp/transaction-status#offramp-transactions)             | Historical transaction status.                                                                                                                           |

<Tip>
  Full API endpoint list

  For a complete list of all API endpoints supported by Onramp/Offramp, visit our [API Reference section](/api-reference/rest-api/onramp-offramp/create-buy-quote).
</Tip>

## Rate Limiting

The **Buy Quote API and Sell Quote API** are rate limited to prevent abuse that would degrade our ability to maintain consistent API performance for all users.
Throttling is enforced per endpoint by app ID at **10 requests per second**.

If your requests are being rate limited, HTTP response code 429 is returned with a `rate_limit_exceeded` error.
Rate limiting is implemented using a sliding window algorithm.

