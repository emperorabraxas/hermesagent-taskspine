# Transfer status changed
Source: https://docs.cdp.coinbase.com/api-reference/payment-apis/rest-api/transfers-under-development/transfer-status-changed

webhook transferStatusChanged
Triggered when a transfer's status changes. Your API will send a POST request to the  webhook URL you configured when subscribing to transfer events.

This webhook is sent for all status transitions including:
* `quoted` → `processing` (when execute is called)
* `processing` → `completed` (successful completion)
* `processing` → `failed` (transfer failed)

Valid webhook `eventType` values:
* `payments.transfers.quoted`
* `payments.transfers.processing`
* `payments.transfers.completed`
* `payments.transfers.failed`

**Security**: Webhooks requests include an `X-Hook0-Signature` header containing an HMAC-SHA256  signature of the request body using your webhook secret. Always verify this signature  before processing webhook events.


