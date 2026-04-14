# API Errors

The Payment APIs uses conventional HTTP response codes to indicate the success or failure of an API request.
In general:

* Codes in the `2xx` range indicate success
* Codes in the `4xx` range indicate an error that failed given the information provided (e.g., a
  required parameter was omitted)
* Codes in the `5xx` range indicate an error on CDP's backend servers.

  <Info>
    `5xx` errors are not a guarantee of failure; there's always the chance that the operation may have
    succeeded in our back-end. Therefore, your application should treat the operation's status as
    **unknown**.
  </Info>

Each error response includes:

* `errorType`: A machine-readable error code
* `errorMessage`: A human-readable message providing more detail
* `correlationId`: A unique identifier for the request that can help with debugging
* `errorLink`: A link to detailed documentation about the specific error type

## HTTP 400

<a />

### Client closed request

This error occurs when the client closes the connection before the server can send a response.

**Common causes:**

* The client timed out waiting for the server response
* The client application was terminated during a pending request
* Network interruption caused the client connection to drop

**Steps to resolve:**

1. Increase client-side timeout settings if applicable
2. Implement retry logic with exponential backoff for long-running queries
3. Consider optimizing the request to reduce server processing time

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "client_closed_request",
  "errorMessage": "Client closed request.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#client_closed_request"
}
```

<a />

### Invalid request

This error occurs when the request is malformed or contains invalid data, including issues with the request body, query parameters, path parameters, or headers.

**Steps to resolve:**

1. Check all required fields and parameters are present
2. Ensure request body (if applicable) follows the correct schema
3. Verify all parameter formats match the API specification:
   * Query parameters
   * Path parameters
   * Request headers
4. Validate any addresses, IDs, or other formatted strings meet requirements

**Common validation issues:**

* Missing required parameters
* Invalid parameter types or formats
* Malformed JSON in request body
* Invalid enum values

#### Transfer-specific validation errors

The following transfer validation scenarios return `errorType: "invalid_request"`. Use the `errorMessage` field to identify the specific case.

| Scenario                                      | Example `errorMessage`                                                                                                                         |
| --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Source account ID is malformed                | `"source is invalid."`                                                                                                                         |
| Target account ID is malformed                | `"target is invalid."`                                                                                                                         |
| Source account does not exist                 | `"source not found."`                                                                                                                          |
| Target account does not exist                 | `"target not found."`                                                                                                                          |
| Asset not supported at source                 | `"source is not supported."`                                                                                                                   |
| Asset not supported at target                 | `"target is not supported."`                                                                                                                   |
| Target email address is malformed             | `"target has an invalid email format."`                                                                                                        |
| Target onchain address is invalid for network | `"The recipient address is invalid for the selected network."`                                                                                 |
| Asset not supported for this transfer route   | `"Transfer asset pair is not supported."`                                                                                                      |
| Insufficient balance                          | `"Insufficient funds to complete this transfer."`                                                                                              |
| Asset mismatch between request fields         | `"Currency mismatch in request."`                                                                                                              |
| Metadata has too many keys                    | `"Metadata has too many keys. Up to 10 key/value pairs are permitted."`                                                                        |
| Metadata key exceeds length limit             | `"Metadata key is too long. Each key must be less than or equal to 40 characters."`                                                            |
| Metadata value exceeds length limit           | `"Metadata value is too long. Each value must be less than or equal to 500 characters."`                                                       |
| Travel rule fields missing                    | `"Travel rule information is incomplete. Missing fields: ..."`                                                                                 |
| Recipient address not in account allowlist    | `"Your coinbase account allowlist does not include this address. Please update your allowlist at https://www.coinbase.com/settings/allowlist"` |

**Example 1:**

```json lines wrap theme={null}
{
  "errorType": "invalid_request",
  "errorMessage": "Invalid query parameters.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#invalid_request"
}
```

**Example 2:**

```json lines wrap theme={null}
{
  "errorType": "invalid_request",
  "errorMessage": "Invalid account ID.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#invalid_request"
}
```

**Example 3:**

```json lines wrap theme={null}
{
  "errorType": "invalid_request",
  "errorMessage": "Invalid account ID or query parameters.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#invalid_request"
}
```

<a />

### Payment required

This error occurs when an x402 payment is required to access the requested resource.

**Steps to resolve:**

1. Include a valid x402 payment header in your request
2. Ensure the payment meets the resource's pricing requirements

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "payment_required",
  "errorMessage": "Payment required.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#payment_required"
}
```

<a />

### Settlement failed

This error occurs when an x402 payment was verified but settlement on-chain failed.

**Steps to resolve:**

1. Retry the request with a new payment
2. Ensure the payment asset has sufficient balance for settlement

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "settlement_failed",
  "errorMessage": "Settlement failed.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#settlement_failed"
}
```

<a />

### Request canceled

This error occurs when the client cancels an in-progress request before it completes.

**Steps to resolve:**

1. Check client-side timeout configurations
2. Review request cancellation logic in your code
3. Consider increasing timeout thresholds for long-running operations
4. Implement request tracking to identify premature cancellations

**Best practices:**

```typescript lines wrap theme={null}
async function withTimeout<T>(promise: Promise<T>, timeoutMs: number): Promise<T> {
  const timeout = new Promise((_, reject) => {
    setTimeout(() => {
      reject(new Error("Operation timed out"));
    }, timeoutMs);
  });

  try {
    return await Promise.race([promise, timeout]);
  } catch (error) {
    // Handle timeout or cancellation
    throw error;
  }
}
```

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "request_canceled",
  "errorMessage": "Request canceled.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#request_canceled"
}
```

<a />

### Timed out

This error occurs when a request exceeds the maximum allowed processing time.

**Steps to resolve:**

1. Break down large requests into smaller chunks (if applicable)
2. Implement retry logic with exponential backoff
3. Use streaming endpoints for large data sets

**Example retry implementation:**

```typescript lines wrap theme={null}
async function withRetryAndTimeout<T>(
  operation: () => Promise<T>,
  maxRetries = 3,
  timeout = 30000,
): Promise<T> {
  let attempts = 0;
  while (attempts < maxRetries) {
    try {
      return await Promise.race([
        operation(),
        new Promise((_, reject) =>
          setTimeout(() => reject(new Error("Timeout")), timeout)
        ),
      ]);
    } catch (error) {
      attempts++;
      if (attempts === maxRetries) throw error;
      // Exponential backoff
      await new Promise(resolve =>
        setTimeout(resolve, Math.pow(2, attempts) * 1000)
      );
    }
  }
  throw new Error("Max retries exceeded");
}
```

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "timed_out",
  "errorMessage": "Timed out.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#timed_out"
}
```

<a />

### Recipient allowlist violation

This error occurs when the user is not allowed to receive funds at this address, according to their coinbase account allowlist.
**Steps to resolve:**

1. Either disable the allowlist or add the wallet address at [https://www.coinbase.com/settings/allowlist](https://www.coinbase.com/settings/allowlist)
2. Wait approximately 2 days for updates to take effect.

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "recipient_allowlist_violation",
  "errorMessage": "Recipient allowlist violation.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#recipient_allowlist_violation"
}
```

<a />

### Recipient allowlist pending

This error occurs when the user is not allowed to receive funds at this address, because changes to their coinbase account allowlist are pending.
**Steps to resolve:**

1. Wait approximately 2 days for updates to take effect.

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "recipient_allowlist_pending",
  "errorMessage": "Recipient allowlist pending.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#recipient_allowlist_pending"
}
```

<a />

### Mfa already enrolled

This error occurs when attempting to enroll in an MFA method that the user has already enrolled in.

**Steps to resolve:**

1. Check if the user is already enrolled in the MFA method before initiating enrollment
2. To update or reset MFA, remove the existing enrollment first (if supported)
3. Use a different MFA method if multiple options are available

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "mfa_already_enrolled",
  "errorMessage": "Mfa already enrolled.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#mfa_already_enrolled"
}
```

<a />

### Mfa invalid code

This error occurs when the MFA code provided is incorrect or has already been used.

**Steps to resolve:**

1. Verify the user entered the correct code from their authenticator app
2. Ensure the code is current (TOTP codes expire after 30 seconds)
3. Check that the device time is synchronized correctly
4. Ask the user to generate a new code and try again

**Common causes:**

* Typing errors in the 6-digit code
* Using an expired TOTP code
* Device clock drift on user's authenticator app
* Attempting to reuse a previously submitted code

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "mfa_invalid_code",
  "errorMessage": "Mfa invalid code.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#mfa_invalid_code"
}
```

<a />

### Mfa flow expired

This error occurs when the MFA enrollment or verification session has expired.

**Steps to resolve:**

1. Restart the MFA enrollment or verification flow
2. Complete the flow within the allowed time window (typically 5 minutes)
3. Ensure the user doesn't leave the flow idle for extended periods

**Note:** MFA sessions expire automatically for security purposes.

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "mfa_flow_expired",
  "errorMessage": "Mfa flow expired.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#mfa_flow_expired"
}
```

<a />

### Mfa required

This error occurs when attempting to perform a sensitive operation that requires MFA verification, but the user has not completed MFA verification.

**Steps to resolve:**

1. Initiate the MFA verification flow using the `/mfa/verify/{mfaMethod}/init` endpoint
2. Prompt the user to enter their MFA code
3. Submit the verification using the `/mfa/verify/{mfaMethod}/submit` endpoint
4. Use the returned access token with MFA claim for the sensitive operation
5. Retry the original request with the new MFA-verified token

**Operations requiring MFA:**

* Transactions Sign/Send
* Key export
* Account management actions (when configured)

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "mfa_required",
  "errorMessage": "Mfa required.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#mfa_required"
}
```

<a />

### Mfa not enrolled

This error occurs when attempting to verify MFA for a user who has not enrolled in any MFA method.

**Steps to resolve:**

1. Check if the user has enrolled in MFA before attempting verification
2. Guide the user through MFA enrollment first using the `/mfa/enroll/{mfaMethod}/init` endpoint
3. Complete enrollment before requiring MFA verification

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "mfa_not_enrolled",
  "errorMessage": "Mfa not enrolled.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#mfa_not_enrolled"
}
```

<a />

### Source account invalid

This error occurs when the source account specified in the transfer request is invalid or malformed.

**Steps to resolve:**

1. Verify the account ID format is correct (e.g., `account_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)
2. Ensure the account ID belongs to your CDP entity
3. Verify the account ID exists by calling `GET /v2/accounts/{accountId}` or `GET /v2/accounts`

**Common causes:**

* Malformed account ID
* Typo in the account ID

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "source_account_invalid",
  "errorMessage": "Source account invalid.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#source_account_invalid"
}
```

<a />

### Target account invalid

This error occurs when the target account specified in the transfer request is invalid or malformed.

**Steps to resolve:**

1. Verify the account ID format is correct (e.g., `account_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)
2. Ensure the account exists and can receive funds
3. Verify the account ID exists by calling `GET /v2/accounts/{accountId}` or `GET /v2/accounts`

**Common causes:**

* Malformed account ID
* Typo in the account ID

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "target_account_invalid",
  "errorMessage": "Target account invalid.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#target_account_invalid"
}
```

<a />

### Source account not found

This error occurs when the source account specified in the transfer does not exist.

**Steps to resolve:**

1. Verify the account ID exists by calling `GET /v2/accounts/{accountId}` or `GET /v2/accounts`

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "source_account_not_found",
  "errorMessage": "Source account not found.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#source_account_not_found"
}
```

<a />

### Target account not found

This error occurs when the target account specified in the transfer does not exist.

**Steps to resolve:**

1. Verify the account ID exists by calling `GET /v2/accounts/{accountId}` or `GET /v2/accounts`

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "target_account_not_found",
  "errorMessage": "Target account not found.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#target_account_not_found"
}
```

<a />

### Source asset not supported

This error occurs when the asset specified in the transfer source is not supported for this transfer type.

**Steps to resolve:**

1. Check the list of supported assets for the source account type
2. Verify the asset symbol is correctly specified (e.g., `usdc`, `usdt`)

**Common causes:**

* Unsupported asset for the transfer route
* Incorrect asset symbol

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "source_asset_not_supported",
  "errorMessage": "Source asset not supported.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#source_asset_not_supported"
}
```

<a />

### Target asset not supported

This error occurs when the asset specified in the transfer target is not supported for this transfer type.

**Steps to resolve:**

1. Check the list of supported assets for the target
2. Verify the asset symbol is correctly specified (e.g., `usdc`, `usdt`)
3. Ensure the target can receive this asset type

**Common causes:**

* Asset not supported by the target
* Unsupported conversion between source and target assets

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "target_asset_not_supported",
  "errorMessage": "Target asset not supported.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#target_asset_not_supported"
}
```

<a />

### Target email invalid

This error occurs when the email address specified as the transfer target is invalid.

**Steps to resolve:**

1. Verify the email address format is valid (e.g., `user@example.com`)
2. Check for typos in the email address
3. Ensure the email domain is valid

**Common causes:**

* Invalid email format
* Missing @ symbol or domain
* Typo in the email address

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "target_email_invalid",
  "errorMessage": "Target email invalid.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#target_email_invalid"
}
```

<a />

### Target onchain address invalid

This error occurs when the onchain address specified as the transfer target is invalid for the specified network.

**Steps to resolve:**

1. Ensure the network is supported for the transfer type
2. Verify the address format matches the target network
3. Ensure you haven't mixed up addresses from different networks

**Common causes:**

* Network not supported for the transfer type
* Address format doesn't match network
* Address from a different blockchain network

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "target_onchain_address_invalid",
  "errorMessage": "Target onchain address invalid.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#target_onchain_address_invalid"
}
```

<a />

### Transfer amount invalid

This error occurs when the transfer amount is invalid.

**Steps to resolve:**

1. Ensure the amount is a positive number and greater than \$1 USD equivalent amount
2. Verify the amount format is a valid decimal string (e.g., `"100.50"`)
3. Check the number of decimal places for the asset

**Common causes:**

* Zero or negative amount
* Too many decimal places for the asset
* Amount below minimum threshold (\$1 USD equivalent amount)

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "transfer_amount_invalid",
  "errorMessage": "Transfer amount invalid.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#transfer_amount_invalid"
}
```

<a />

### Transfer asset not supported

This error occurs when the asset specified for the transfer is not supported.

**Steps to resolve:**

1. Check the list of supported assets for transfers
2. Verify the asset symbol is correctly specified
3. Ensure the asset is supported for the transfer route (source → target)

**Common causes:**

* Asset not supported for transfers
* Incorrect asset symbol

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "transfer_asset_not_supported",
  "errorMessage": "Transfer asset not supported.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#transfer_asset_not_supported"
}
```

<a />

### Insufficient balance

This error occurs when the source account does not have enough funds to complete the transfer including fees.

**Steps to resolve:**

1. Check the source account balance
2. Ensure the balance covers both the transfer amount and any fees
3. Consider using `amountType: "source"` to transfer the maximum available amount minus fees
4. Add funds to the source account if needed

**Common causes:**

* Transfer amount exceeds available balance
* Not accounting for transfer fees
* Pending transactions reducing available balance

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "insufficient_balance",
  "errorMessage": "Insufficient balance.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#insufficient_balance"
}
```

<a />

### Metadata too many entries

This error occurs when the transfer metadata contains more entries than allowed.

**Steps to resolve:**

1. Reduce the number of metadata entries (maximum 10 allowed)
2. Consolidate related data into fewer keys
3. Store additional data externally and reference it with a single metadata entry

**Limits:**

* Maximum entries: 10

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "metadata_too_many_entries",
  "errorMessage": "Metadata too many entries.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#metadata_too_many_entries"
}
```

<a />

### Metadata key too long

This error occurs when a metadata key exceeds the maximum allowed length.

**Steps to resolve:**

1. Shorten the metadata key to 40 characters or less
2. Use abbreviations or shorter naming conventions
3. Consider using a key-value structure where the value contains the longer identifier

**Limits:**

* Maximum key length: 40 characters

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "metadata_key_too_long",
  "errorMessage": "Metadata key too long.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#metadata_key_too_long"
}
```

<a />

### Metadata value too long

This error occurs when a metadata value exceeds the maximum allowed length.

**Steps to resolve:**

1. Shorten the metadata value to 500 characters or less
2. Store longer data externally and reference it with a shorter identifier
3. Consider compressing or encoding the data if appropriate

**Limits:**

* Maximum value length: 500 characters

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "metadata_value_too_long",
  "errorMessage": "Metadata value too long.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#metadata_value_too_long"
}
```

<a />

### Travel rules field missing

This error occurs when required travel rule fields are missing from the transfer request.

**Steps to resolve:**

1. Include the `travelRule` object in your transfer request
2. Supply the required missing fields prompted by the error message
3. Review the travel rule requirements for your jurisdiction

Note: Required fields may vary by region.

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "travel_rules_field_missing",
  "errorMessage": "Travel rules field missing.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#travel_rules_field_missing"
}
```

<a />

### Asset mismatch

This error occurs when the assets specified in the transfer are incompatible or don't match expected values.

**Steps to resolve:**

1. Ensure the `asset` field matches either the source or target asset
2. Verify that the source and target assets are compatible for conversion (if different)
3. Check that the asset symbols are correctly specified

**Common causes:**

* Transfer asset doesn't match source or target
* Attempting an unsupported asset conversion
* Typo in asset symbols

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "asset_mismatch",
  "errorMessage": "Asset mismatch.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#asset_mismatch"
}
```

<a />

### Order quote expired

This error occurs when attempting to execute an order whose quote has expired.

**Steps to resolve:**

1. Create a new order with `execute: false` to get an updated quote.
2. Execute the new order before the quote expires (check the `expiresAt` field).
3. Alternatively, create a new order with `execute: true` to skip the quote step and execute immediately.

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "order_quote_expired",
  "errorMessage": "Order quote expired.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#order_quote_expired"
}
```

<a />

### Order already filled

This error occurs when attempting to cancel or modify an order that has already been filled.

**Steps to resolve:**

1. Check the current status of the order using `GET /v2/orders/{orderId}`.
2. A filled order cannot be canceled or re-executed.

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "order_already_filled",
  "errorMessage": "Order already filled.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#order_already_filled"
}
```

<a />

### Order already canceled

This error occurs when attempting to cancel or execute an order that has already been canceled.

**Steps to resolve:**

1. Check the current status of the order using `GET /v2/orders/{orderId}`.
2. Create a new order if you still want to trade.

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "order_already_canceled",
  "errorMessage": "Order already canceled.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#order_already_canceled"
}
```

<a />

### Account not ready

This error occurs when an operation is attempted on an account that is still being provisioned.

**Steps to resolve:**

1. Wait a few moments and retry the request
2. If the error persists, the account may still be completing setup — retry with exponential backoff

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "account_not_ready",
  "errorMessage": "Account not ready.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#account_not_ready"
}
```

<a />

### Insufficient liquidity

This error occurs when no swap route is available for the requested token pair or amount.

**Steps to resolve:**

1. Try a smaller `fromAmount` — large orders may exceed available liquidity
2. Try a different token pair
3. Retry after a short delay; liquidity conditions change with market activity

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "insufficient_liquidity",
  "errorMessage": "Insufficient liquidity.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#insufficient_liquidity"
}
```

<a />

### Insufficient allowance

This error occurs when the taker has not approved the Permit2 contract to spend the `fromToken`
on their behalf. ERC-20 swaps require a Permit2 allowance. Native ETH swaps do not.

**Steps to resolve:**

1. Submit an ERC-20 `approve` transaction on the `fromToken` contract, granting the Permit2
   contract (`0x000000000022D473030F116dDEE9F6B43aC78BA3`) an allowance of at least `fromAmount`
2. Wait for the approval transaction to be confirmed on-chain
3. Retry the swap

**Example:**

```typescript lines wrap theme={null}
// Approve Permit2 to spend fromToken
await walletClient.writeContract({
  address: fromToken,
  abi: erc20Abi,
  functionName: "approve",
  args: ["0x000000000022D473030F116dDEE9F6B43aC78BA3", fromAmount],
});
```

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "insufficient_allowance",
  "errorMessage": "Insufficient allowance.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#insufficient_allowance"
}
```

<a />

### Transaction simulation failed

This error occurs when the pre-broadcast simulation of the swap transaction predicted a revert.
No transaction was submitted and no gas was spent.

**Common causes:**

* The on-chain price moved past the `slippageBps` tolerance between the price estimate and execution
* Taker balance changed between the price estimate and execution

**Steps to resolve:**

1. Retry immediately — prices change quickly and a new quote may succeed
2. Increase `slippageBps` if retries continue to fail (e.g. from 100 to 200)
3. For large swaps, consider splitting into smaller amounts to reduce price impact

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "transaction_simulation_failed",
  "errorMessage": "Transaction simulation failed.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#transaction_simulation_failed"
}
```

## HTTP 401

<a />

### Unauthorized

This error occurs when authentication fails.

**Steps to resolve:**

1. Verify your CDP API credentials:
   * Check that your API key is valid
   * Check that your Wallet Secret is properly configured
2. Validate JWT token:
   * Not expired
   * Properly signed
   * Contains required claims
3. Check request headers:
   * Authorization header present
   * X-Wallet-Auth header included when required

**Security note:** Never share your Wallet Secret or API keys.

**Example 1:**

```json lines wrap theme={null}
{
  "errorType": "unauthorized",
  "errorMessage": "Authentication required.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#unauthorized"
}
```

**Example 2:**

```json lines wrap theme={null}
{
  "errorType": "unauthorized",
  "errorMessage": "Authentication error.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#unauthorized"
}
```

**Example 3:**

```json lines wrap theme={null}
{
  "errorType": "unauthorized",
  "errorMessage": "The request is not properly authenticated.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#unauthorized"
}
```

## HTTP 402

<a />

### Payment method required

This error occurs when a payment method is required to complete the requested operation but none is configured or available.

**Steps to resolve:**

1. Add a valid payment method to your account using the [CDP Portal](https://portal.cdp.coinbase.com)
2. Ensure your payment method is valid and not expired

**Common causes:**

* No payment method configured on the account
* Payment method is expired

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "payment_method_required",
  "errorMessage": "Payment method required.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#payment_method_required"
}
```

## HTTP 403

<a />

### Forbidden

This error occurs when you don't have permission to access the resource.

**Steps to resolve:**

1. Verify your permissions to access the resource
2. Ensure that you are the owner of the requested resource

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "forbidden",
  "errorMessage": "Forbidden.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#forbidden"
}
```

## HTTP 404

<a />

### Not found

This error occurs when the resource specified in your request doesn't exist or you don't have access to it.

**Steps to resolve:**

1. Verify the resource ID/address/account exists
2. Check your permissions to access the resource
3. Ensure you're using the correct network/environment
4. Confirm the resource hasn't been deleted

**Common causes:**

* Mistyped addresses
* Accessing resources from the wrong CDP project
* Resource was deleted or hasn't been created yet

**Example 1:**

```json lines wrap theme={null}
{
  "errorType": "not_found",
  "errorMessage": "Account not found.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#not_found"
}
```

**Example 2:**

```json lines wrap theme={null}
{
  "errorType": "not_found",
  "errorMessage": "Account or asset not found.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#not_found"
}
```

**Example 3:**

```json lines wrap theme={null}
{
  "errorType": "not_found",
  "errorMessage": "Deposit address not found.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#not_found"
}
```

## HTTP 409

<a />

### Already exists

This error occurs when trying to create a resource that already exists.

**Steps to resolve:**

1. Check if the resource exists before creation
2. Use GET endpoints to verify resource state
3. Use unique identifiers/names for resources

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "already_exists",
  "errorMessage": "Already exists.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#already_exists"
}
```

## HTTP 422

<a />

### Idempotency error

This error occurs when an idempotency key is reused with different parameters.

**Steps to resolve:**

1. Generate a new UUID v4 for each unique request
2. Only reuse idempotency keys for exact request duplicates
3. Track used keys within your application

**Example idempotency key implementation:**

```typescript lines wrap theme={null}
import { v4 as uuidv4 } from 'uuid';

function createIdempotencyKey() {
  return uuidv4();
}
```

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "idempotency_error",
  "errorMessage": "Idempotency key '8e03978e-40d5-43e8-bc93-6894a57f9324' was already used with a different request payload. Please try again with a new idempotency key.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#idempotency_error"
}
```

<a />

### Travel rules recipient violation

This error occurs when the user is not allowed to receive funds at this address, because it violates travel rules.
**Steps to resolve:**

1. Ensure your desired transfer is not blocked by local travel regulations.

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "travel_rules_recipient_violation",
  "errorMessage": "Travel rules recipient violation.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#travel_rules_recipient_violation"
}
```

## HTTP 429

<a />

### Rate limit exceeded

This error occurs when you've exceeded the API rate limits.

**Steps to resolve:**

1. Implement exponential backoff
2. Cache responses where possible
3. Wait for rate limit window to reset

**Best practices:**

```typescript lines wrap theme={null}
async function withRetry(fn: () => Promise<any>) {
  let delay = 1000;
  while (true) {
    try {
      return await fn();
    } catch (e) {
      if (e.errorType === "rate_limit_exceeded") {
        await sleep(delay);
        delay *= 2;
        continue;
      }
      throw e;
    }
  }
}
```

**Example 1:**

```json lines wrap theme={null}
{
  "errorType": "rate_limit_exceeded",
  "errorMessage": "Rate limit exceeded.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#rate_limit_exceeded"
}
```

**Example 2:**

```json lines wrap theme={null}
{
  "errorType": "rate_limit_exceeded",
  "errorMessage": "Too many requests. Please try again later.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#rate_limit_exceeded"
}
```

## HTTP 500

<a />

### Internal server error

This indicates an unexpected error that occurred on the CDP servers.

**Important**: If you encounter this error, please note that your operation's status should be treated as unknown by your application, as it could have been a success within the CDP back-end.

**Steps to resolve:**

1. Retry your request after a short delay
2. If persistent, contact CDP support with:
   * Your correlation ID
   * Timestamp of the error
   * Request details
3. Consider implementing retry logic with an exponential backoff

**Note:** These errors are automatically logged and monitored by CDP.

**Example 1:**

```json lines wrap theme={null}
{
  "errorType": "internal_server_error",
  "errorMessage": "An internal server error occurred.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#internal_server_error"
}
```

**Example 2:**

```json lines wrap theme={null}
{
  "errorType": "internal_server_error",
  "errorMessage": "An internal server error occurred. Please try again later.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#internal_server_error"
}
```

## HTTP 502

<a />

### Bad gateway

This error occurs when the CDP API is unable to connect to the backend service.

**Steps to resolve:**

1. Retry your request after a short delay
2. If persistent, contact CDP support with:
   * The timestamp of the error
   * Request details
3. Consider implementing retry logic with an exponential backoff

**Note:** These errors are automatically logged and monitored by CDP.

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "bad_gateway",
  "errorMessage": "Bad gateway. Please try again later.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#bad_gateway"
}
```

## HTTP 503

<a />

### Service unavailable

This error occurs when the CDP API is temporarily unable to handle requests due to maintenance or high load.

**Steps to resolve:**

1. Retry your request after a short delay
2. If persistent, contact CDP support with:
   * The timestamp of the error
   * Request details
3. Consider implementing retry logic with an exponential backoff

**Note:** These errors are automatically logged and monitored by CDP.

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "service_unavailable",
  "errorMessage": "Service unavailable. Please try again later.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#service_unavailable"
}
```

## Network Errors

Network errors occur when there is a problem establishing or maintaining a connection to the CDP API at the network layer. These errors are distinct from API service errors - they indicate that your request never reached the CDP API or was blocked before it could be processed.

### Understanding Network Errors

When you encounter a network error via the CDP SDK, you'll receive a `NetworkError` object with:

* `statusCode`: Always 0 (indicating no HTTP response was received)
* `errorType`: Specific type of network error
* `errorMessage`: Human-readable description
* `networkDetails`: Additional information including:
  * `code`: Technical error code
  * `message`: Original error message
  * `retryable`: Whether the operation should be retried

### Types of Network Errors

#### 1. **IP Blocked** (`network_ip_blocked`)

Your IP address has been blocked at the gateway level.

**Common causes:**

* Geographic restrictions.
* Rate limiting at infrastructure level.
* Security policies or DDoS protection.
* Corporate firewall/proxy restrictions.

**What to do:**

* Verify you're not accessing from a [restricted region](https://help.coinbase.com/en/coinbase/managing-my-account/other/prohibited-regions).
* Check if you're behind a VPN or proxy that might be blocked.
* Contact [CDP support on Discord](https://discord.com/channels/1220414409550336183/1271495764580896789) if you believe this is in error.
* This error is **not retryable**.

#### 2. **Connection Failed** (`network_connection_failed`)

Unable to establish a connection to the CDP API.

**Common causes:**

* CDP API is temporarily unavailable. Check the [CDP Status Page](https://cdpstatus.coinbase.com/#status) for any ongoing issues.
* Network connectivity issues.
* Firewall blocking outbound HTTPS connections.
* Incorrect API endpoint configuration.

**What to do:**

* Check your internet connection.
* Verify firewall settings allow HTTPS traffic to `api.cdp.coinbase.com`.
* Ensure you're using the correct API endpoint.
* This error is **retryable**. Retry the request with [exponential backoff](/api-reference/v2/errors#handling-network-errors-in-code).

#### 3. **Timeout** (`network_timeout`)

The request took too long and was terminated.

**Common causes:**

* Network congestion.
* Slow internet connection.

**What to do:**

* Increase timeout settings if consistently timing out.
* This error is **retryable**. Retry the request with [exponential backoff](/api-reference/v2/errors#handling-network-errors-in-code).

#### 4. **DNS Failure** (`network_dns_failure`)

Unable to resolve the CDP API domain name.

**Common causes:**

* DNS configuration issues.
* Network connectivity problems.
* DNS server unavailable.
* Incorrect API endpoint URL.

**What to do:**

* Check your DNS settings.
* Verify network connectivity with `nslookup api.cdp.coinbase.com`.
* Try using a different DNS server (e.g., 8.8.8.8).
* Ensure the API URL is correct.
* This error is **not retryable** until DNS is fixed.

### Handling Network Errors in Code

<CodeGroup>
  ```typescript main.ts lines wrap theme={null}
  import { NetworkError } from '@coinbase/cdp-sdk';

  try {
    const account = await cdp.evm.getAccount({ address: '0x...' });
  } catch (error) {
    if (error instanceof NetworkError) {
      console.error(`Network error: ` + error.errorMessage);
      console.error(`Type: ` + error.errorType);
      console.error(`Details:` + error.networkDetails);

      // Check if the error is retryable
      if (error.networkDetails?.retryable) {
        // Implement retry logic with exponential backoff
        await retryWithBackoff(async () => {
          return await cdp.evm.getAccount({ address: '0x...' });
        });
      } else {
        // Handle non-retryable errors
        if (error.errorType === "network_ip_blocked") {
          console.error('Your IP appears to be blocked. Please check your network configuration.');
        }
      }
    }
  }
  ```

  ```python main.py lines wrap theme={null}
  from cdp import CdpClient, NetworkError, HttpErrorType
  import time

  cdp = CdpClient()

  try:
      account = await cdp.evm.get_account(address="0x...")
  except NetworkError as e:
      print(f"Network error: {e.error_message}")
      print(f"Type: {e.error_type}")
      print(f"Details: {e.network_details}")

      # Check if the error is retryable
      if e.network_details.get("retryable", False):
          # Implement retry logic with exponential backoff
          retry_with_backoff(lambda: cdp.evm.get_account(address="0x..."))
      else:
          # Handle non-retryable errors
          if e.error_type == HttpErrorType.NETWORK_IP_BLOCKED:
              print("Your IP appears to be blocked. Please check your network configuration.")
  ```
</CodeGroup>

### Best Practices

1. **Implement Retry Logic**: For retryable errors, use exponential backoff:

<CodeGroup>
  ```typescript retry-with-backoff.ts lines wrap theme={null}
  async function retryWithBackoff<T>(
    fn: () => Promise<T>,
    maxRetries = 3,
    baseDelay = 1000
  ): Promise<T> {
    for (let i = 0; i < maxRetries; i++) {
      try {
        return await fn();
      } catch (error) {
        if (error instanceof NetworkError && error.networkDetails?.retryable && i < maxRetries - 1) {
          await new Promise(resolve => setTimeout(resolve, baseDelay * Math.pow(2, i)));
          continue;
        }
        throw error;
      }
    }
    throw new Error('Max retries exceeded');
  }
  ```

  ```python retry-with-backoff.py lines wrap theme={null}
  def retry_with_backoff(fn, max_retries=3, base_delay=1000):
    for attempt in range(max_retries):
      try:
        return await fn()
      except Exception as e:
        if isinstance(e, NetworkError) and e.network_details.get("retryable", False) and attempt < max_retries - 1:
          await asyncio.sleep((base_delay / 1000) * 2 ** attempt)
          continue
        raise e
  ```
</CodeGroup>

2. **Log Network Errors**: Always log network errors with full details for debugging.

3. **Monitor Patterns**: Track network errors to identify patterns (time of day, specific operations, etc.).

4. **Have Fallback Strategies**: Consider implementing fallback mechanisms for critical operations.

### Troubleshooting Checklist

* Verify internet connectivity.
* Check if you're behind a proxy or VPN.
* Ensure firewall allows HTTPS traffic to `api.cdp.coinbase.com`.
* Verify you're not in a restricted geographic region.
* Check DNS resolution: `nslookup api.cdp.coinbase.com`.
* Test with `curl` or similar: `curl -I https://api.cdp.coinbase.com/platform`.
* Check if the issue is consistent or intermittent.

### Getting Help

If you continue to experience network errors after following this guide:

1. Collect error details including:
   * Full error message and type.
   * Network details from the error.
   * Time and frequency of occurrence.
   * Your network configuration (proxy, VPN, region).

2. Contact [CDP support on Discord](https://discord.com/channels/1220414409550336183/1271495764580896789) with this information.

3. Check the [CDP Status Page](https://cdpstatus.coinbase.com/#status) for any ongoing issues.

Remember: Network errors are typically environmental issues rather than code problems. Focus on network configuration and connectivity when troubleshooting.

