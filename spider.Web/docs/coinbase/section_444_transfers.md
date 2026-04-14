# Transfers
Source: https://docs.cdp.coinbase.com/api-reference/payment-apis/rest-api/transfers-under-development/transfers-under-development



**Transfers** represent both the request and execution of fund transfers from a source to a target. They provide upfront fee quotes and track the complete lifecycle from initiation through completion, failure, or reversal.

## Fee Quotes

Every transfer provides a comprehensive fee quote in the `fees` array. This allows you to show users exactly what they'll pay before any money moves.

To review fees before execution:

1. Create a transfer with `execute: false`
2. Review the `fees` array in the response
3. Call `POST /transfers/{transferId}/execute` when ready to proceed

For automatic execution without fee review, create a transfer with `execute: true`.

**Fee Expiration**: Fee quotes are valid for a limited time (typically 10-15 minutes from creation). The `expiresAt` field shows exactly when the fee quote will expire. If you don't execute before this time, you'll need to create a new transfer to get updated fees.

## Fees

Transfer fees vary by source, target, amount and transfer type:

* **Bank fees** - Traditional banking fees for depositing funds (e.g., \$15.00 wire transfer fee)
* **Conversion fees** - Fees for exchanging between different assets
* **Network fees** - Onchain transaction costs to complete the transfer (e.g., ETH gas fees)

All fees are disclosed upfront in the `fees` array when you create a transfer.

## Transfer Lifecycle

When you create a transfer, it will be in one of these statuses that determine what action you need to take:

* **`quoted`** - Transfer is ready but requires manual execution via the `/execute` endpoint
* **`processing`** - Transfer is being executed (no action needed - poll for completion)
* **`completed`** - Transfer completed successfully
* **`failed`** - Transfer failed (see `failureReason` for details)

## Execution Control

* **`execute: true`**: Transfer will automatically attempt to execute
* **`execute: false`**: Transfer will be created in `quoted` status and you must call the `/execute` endpoint. Use this to obtain a fee quote or validate a transfer destination before deciding whether to execute the Transfer.

## Sources and Targets

* A **source** can be an Account or a Payment Method
* A **target** can be an Account, Payment Method, Onchain Address, or Email Address

## Transfer Execution

When a transfer reaches `completed` status, it contains the final execution details that delivered funds to the target and completion timestamps.

## Failure Reasons

When a transfer fails, the `failureReason` field provides a human-readable description of what went wrong.
Common failure reasons include:

* "Insufficient balance to complete this transfer."
* "The recipient address is invalid for the selected network."
* "The recipient address failed security validation checks."
* "Unable to send to this recipient."

Failure reason is only present when the transfer's status is `failed`.

