Webhooks 
=========

#### API reference for webhooks 

Prefer to learn by watching? Our [video tutorial](https://www.youtube.com/watch?v=0E0KEAVeDyc) walks you through the basics of incorporating Plaid webhooks into your application.

Looking for webhook schemas? The reference documentation for specific webhooks ([Transactions](https://plaid.com/docs/api/products/transactions/index.html.md#webhooks) , [Auth](https://plaid.com/docs/api/products/auth/index.html.md#webhooks) , [Assets](https://plaid.com/docs/api/products/assets/index.html.md#webhooks) , [Identity](https://plaid.com/docs/api/products/identity/index.html.md#webhooks-beta) , [Identity Verification](https://plaid.com/docs/api/products/identity-verification/index.html.md#webhooks) , [Monitor](https://plaid.com/docs/api/products/monitor/index.html.md) , [Investments](https://plaid.com/docs/api/products/investments/index.html.md#webhooks) , [Liabilities](https://plaid.com/docs/api/products/liabilities/index.html.md#webhooks) , [Payment Initiation](https://plaid.com/docs/api/products/payment-initiation/index.html.md#webhooks) , [Income](https://plaid.com/docs/api/products/income/index.html.md#webhooks) , [Virtual Accounts](https://plaid.com/docs/api/products/virtual-accounts/index.html.md#webhooks) , [Items](https://plaid.com/docs/api/items/index.html.md#webhooks) , and [Transfer](https://plaid.com/docs/api/products/transfer/index.html.md) ) has moved to its respective API reference pages.

\=\*=\*=\*=

#### Introduction to webhooks 

A webhook is an HTTP request used to provide push notifications. Plaid sends webhooks to programmatically inform you about changes to Plaid Items or the status of asynchronous processes. For example, Plaid will send a webhook when an Item is in an error state or has additional data available, or when a non-blocking process (like gathering transaction data or verifying a bank account via micro-deposits) is complete.

To receive Plaid webhooks, set up a dedicated endpoint on your server as a webhook listener that can receive POST requests, then provide this endpoint URL to Plaid as described in the next section. You can also test webhooks without setting up your own endpoint following the instructions in [Testing webhooks in Sandbox](https://plaid.com/docs/api/webhooks/index.html.md#testing-webhooks-in-sandbox) .

\=\*=\*=\*=

#### Configuring webhooks 

Webhooks are typically configured via the `webhook` parameter of [/link/token/create](https://plaid.com/docs/api/link/index.html.md#linktokencreate) , although some webhooks (especially those used in contexts where Link tokens are not always required), such as Identity Verification webhooks, are configured via the [Plaid Dashboard](https://dashboard.plaid.com/developers/webhooks) instead. When specifying a webhook, the URL must be in the standard format of `http(s)://(www.)domain.com/` and, if https, must have a valid SSL certificate.

To view response codes and debug any issues with webhook setup, see the [Logs section in the Dashboard](https://dashboard.plaid.com/activity/logs) .

Plaid sends POST payloads with raw JSON to your webhook URL from one of the following IP addresses:

*   52.21.26.131
*   52.21.47.157
*   52.41.247.19
*   52.88.82.239

Note that these IP addresses are subject to change.

You can optionally verify webhooks to ensure they are from Plaid. For more information, see [webhook verification](https://plaid.com/docs/api/webhooks/webhook-verification/index.html.md) .

\=\*=\*=\*=

#### Webhook retries 

If there is a non-200 response or no response within 10 seconds from the webhook endpoint, Plaid will keep attempting to send the webhook for up to 24 hours. Each attempt will be tried after a delay that is 4 times longer than the previous delay, starting with 30 seconds.

To avoid unnecessary retries, Plaid won't retry webhooks if we detect that the webhook receiver endpoint has rejected more than 90% of webhooks sent by Plaid over the last 24 hours.

If your endpoint returns a `429 Too Many Requests` response, Plaid will honor the `Retry-After` header if present, waiting the specified duration for up a maximum of 4 hours later before the next attempt instead of applying the standard exponential backoff. The `Retry-After` value may be an integer number of seconds (e.g. `120`), an HTTP date (e.g. `Wed, 21 Oct 2026 07:28:00 GMT`), or an ISO 8601 timestamp (e.g. `2026-10-21T07:28:00Z`).

\=\*=\*=\*=

#### Best practices for applications using webhooks 

You should design your application to handle duplicate and out-of-order webhooks. Ensure [idempotency](https://martinfowler.com/articles/patterns-of-distributed-systems/idempotent-receiver.html) on actions you take when receiving a webhook. If you drive application state with webhooks, ensure your code doesn't rely on a specific order of webhook receipt.

If you (or Plaid) experience downtime for longer than Plaid's [retry period](https://plaid.com/docs/api/webhooks/index.html.md#webhook-retries) , you will lose webhooks. Ensure your application can recover by implementing endpoint polling or other appropriate logic if a webhook is not received within an expected window. All data present in webhooks is also present in our other APIs.

It's best to keep your receiver as simple as possible, such as a receiver whose only job is to write the webhook into a queue or reliable storage. This is important for two reasons. First, if the receiver does not respond within 10 seconds, the delivery is considered failed. Second, because webhooks can arrive at unpredictable rates. Therefore if you do a lot of work in your receiver - e.g. generating and sending an email - spikes are likely to overwhelm your downstream services, or cause you to be rate-limited if the downstream is a third-party.

\=\*=\*=\*=

#### Testing webhooks in Sandbox 

Webhooks will fire as normal in the Sandbox environment, with the exception of Transfer webhooks. For testing purposes, you can also use [/sandbox/item/fire\_webhook](https://plaid.com/docs/api/sandbox/index.html.md#sandboxitemfire_webhook) , [/sandbox/income/fire\_webhook](https://plaid.com/docs/api/sandbox/index.html.md#sandboxincomefire_webhook) , or [/sandbox/transfer/fire\_webhook](https://plaid.com/docs/api/sandbox/index.html.md#sandboxtransferfire_webhook) to fire a webhook on demand. If you don't have a webhook endpoint configured yet, you can also use a tool such as [Webhook.site](https://webhook.site) or [Request Bin](https://requestbin.com/) to quickly and easily set up a webhook listener endpoint. When directing webhook traffic to third-party tools, make sure you are using Plaid's Sandbox environment and not sending out live data.

\=\*=\*=\*=

#### Example in Plaid Pattern 

For real-life examples of handling webhooks that illustrate how to handle sample transactions and Item webhooks, see [handleTransactionsWebhook.js](https://github.com/plaid/pattern/blob/master/server/webhookHandlers/handleTransactionsWebhook.js) and [handleItemWebhook.js](https://github.com/plaid/pattern/blob/master/server/webhookHandlers/handleItemWebhook.js) These files contain webhook handling code for the Node-based [Plaid Pattern](https://github.com/plaid/pattern) sample app.