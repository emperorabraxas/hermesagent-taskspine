# Client / Server Flow
Source: https://docs.cdp.coinbase.com/x402/core-concepts/client-server



This page explains the roles and responsibilities of the **client** and **server** in the x402 protocol.

Understanding these roles is essential to designing, building, or integrating services that use x402 for programmatic payments.

<Info>
  Client refers to the technical component making an HTTP request. In practice, this is often the buyer of the resource.

  Server refers to the technical component responding to the request. In practice, this is typically the seller of the resource
</Info>

## Client Role

The client is the entity that initiates a request to access a paid resource.

Clients can include:

* Human-operated applications
* Autonomous agents
* Programmatic services acting on behalf of users or systems

### Responsibilities

* **Initiate requests:** Send an HTTP request to the resource server.
* **Handle payment requirements:** Read the `402 Payment Required` response and extract payment details.
* **Prepare payment payload:** Use the provided payment requirements to construct a valid payment payload.
* **Resubmit request with payment:** Retry the request with the `X-PAYMENT` header containing the signed payment payload.

Clients do not need to manage accounts, credentials, or session tokens beyond their crypto wallet. All interactions are stateless and occur over standard HTTP requests.
