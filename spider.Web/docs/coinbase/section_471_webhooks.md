# Webhooks
Source: https://docs.cdp.coinbase.com/api-reference/payment-apis/webhooks



CDP Transfers webhooks provide your app with real-time transfer status updates. By subscribing your webhook endpoint you will receive a notification every time a transfer made by your users is created or updated.

## Getting started

<Steps>
  <Step title="Subscribe">
    Set up a [subscription](/api-reference/payment-apis/webhooks/subscriptions) to transfer webhook events.
  </Step>

  <Step title="Verify">
    Implement [signature verification](/api-reference/payment-apis/webhooks/verification) in your receiver.
  </Step>

  <Step title="Inspect payloads">
    See [example payloads](/api-reference/payment-apis/webhooks/example-payloads) for event shapes.
  </Step>
</Steps>

## Best practices

* **Test locally first** before enabling production subscriptions.
* **Support concurrent delivery** at your webhook endpoint.
* **Acknowledge quickly** (`200`), then process in the background.
* **Monitor delivery health** and alert on failures.
* **Check subscriptions regularly** and confirm critical ones remain `isEnabled: true`.

<Note>
  Subscriptions can be auto-disabled after sustained delivery failures. Fix the endpoint issue, then re-enable with the [Update Subscription API](/api-reference/payment-apis/rest-api/webhooks/update-webhook-subscription).
</Note>

