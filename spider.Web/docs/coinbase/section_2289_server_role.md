# Server Role

The server is the resource provider enforcing payment for access to its services.

Servers can include:

* API services
* Content providers
* Any HTTP-accessible resource requiring monetization

### Responsibilities

* **Define payment requirements:** Respond to unauthenticated requests with an HTTP `402 Payment Required`, including all necessary payment details in the response body.
* **Verify payment payloads:** Validate incoming payment payloads, either locally or by using a facilitator service.
* **Settle transactions:** Upon successful verification, submit the payment for settlement.
* **Provide the resource:** Once payment is confirmed, return the requested resource to the client.

Servers do not need to manage client identities or maintain session state. Verification and settlement are handled per request.

## How It Works

For a detailed explanation of the complete payment flow between clients and servers, see [How x402 Works](/x402/core-concepts/how-it-works).

## Summary

In the x402 protocol:

* The **client** requests resources and supplies the signed payment payload.
* The **server** enforces payment requirements, verifies transactions, and provides the resource upon successful payment.

This interaction is stateless, HTTP-native, and compatible with both human applications and automated agents.

Next, explore:

* [How x402 Works](/x402/core-concepts/how-it-works): See the complete payment flow
* [Facilitator](/x402/core-concepts/facilitator): How servers verify and settle payments
* [HTTP 402](/x402/core-concepts/http-402): How servers communicate payment requirements to clients

