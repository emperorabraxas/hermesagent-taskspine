# Offramp FAQ

### What is the recommended polling strategy for Offramp transaction status?

We recommend to avoid polling immediately after generating the URL; instead, wait until the send transaction is created. Additionally, using exponential backoff to manage polling frequency—starting with short intervals and increasing over time.

### Can users complete ACH withdrawals through the Offramp flow using guest checkout, or is a Coinbase account required?

A Coinbase account with linked bank details is required for Offramp and ACH withdrawals. Guest checkout is not supported for fiat withdrawal.

### What happens if a user sends crypto to the Coinbase-provided address after the 30-minute window in the Offramp flow?

If funds are sent after the 30-minute window, they will still arrive in the users Coinbase account as a crypto balance, but the Offramp transaction will likely move to a TRANSACTION\_STATUS\_FAILED state. The address remains valid and usable by the user, but the original sell flow will not complete automatically.

<br />

<br />

**See Also:**

* [Supported Payment Methods](/onramp/additional-resources/payment-methods)
* [Layer 2 Networks](/onramp/additional-resources/layer-2-networks)

