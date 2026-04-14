# API Errors

The CDP API v2 uses conventional HTTP response codes to indicate the success or failure of an API request.
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
  "errorMessage": "Invalid project ID.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#invalid_request"
}
```

**Example 2:**

```json lines wrap theme={null}
{
  "errorType": "invalid_request",
  "errorMessage": "At least one authentication method must be provided.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#invalid_request"
}
```

**Example 3:**

```json lines wrap theme={null}
{
  "errorType": "invalid_request",
  "errorMessage": "The request contains one or more unsupported options.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#invalid_request"
}
```

<a />

### Malformed transaction

This error occurs when the transaction data provided is not properly formatted or is invalid.

**Steps to resolve:**

1. Verify transaction encoding:
   * **EVM networks**: Check RLP encoding is correct
   * **Solana**: Validate base64 encoding
2. Ensure all required transaction fields are present
3. Validate transaction parameters are within acceptable ranges
4. Check that the transaction type is supported on the target network (see our [Supported Networks](/get-started/supported-networks) page for more details)

**Common causes:**

* Invalid hex encoding for EVM transactions
* Missing required transaction fields
* Incorrect parameter formats
* Unsupported transaction types
* Network-specific transaction format mismatches

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "malformed_transaction",
  "errorMessage": "Malformed unsigned transaction.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#malformed_transaction"
}
```

<a />

### Invalid signature

This error occurs when the signature provided for the given user operation is invalid.

**Steps to resolve:**

1. Verify the signature was generated by the correct owner account
2. Ensure the signature corresponds to the exact user operation hash
3. Check that the signature format matches the expected format
4. Confirm you're using the correct network for the Smart Account

**Common causes:**

* Using wrong owner account to sign
* Signing modified/incorrect user operation data
* Malformed signature encoding
* Network mismatch between signature and broadcast

**Example 1:**

```json lines wrap theme={null}
{
  "errorType": "invalid_signature",
  "errorMessage": "Failed to sign user operation.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#invalid_signature"
}
```

**Example 2:**

```json lines wrap theme={null}
{
  "errorType": "invalid_signature",
  "errorMessage": "Invalid signature.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#invalid_signature"
}
```

<a />

### Policy in use

This error occurs when trying to delete a Policy that is currently in use by at least one project or account.

**Steps to resolve:**

1. Update project or accounts to remove references to the Policy in question.
2. Retry your delete request.

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "policy_in_use",
  "errorMessage": "Policy in use",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#policy_in_use"
}
```

<a />

### Invalid sql query

This error occurs when the SQL query is invalid or not allowed.

**Common causes:**

* Using non-SELECT SQL statements (INSERT, UPDATE, DELETE, etc.)
* Invalid table or column names
* Syntax errors in SQL query
* Query exceeds character limit
* Too many JOIN operations

**Example 1:**

```json lines wrap theme={null}
{
  "errorType": "invalid_sql_query",
  "errorMessage": "INSERTs are not supported",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#invalid_sql_query"
}
```

**Example 2:**

```json lines wrap theme={null}
{
  "errorType": "invalid_sql_query",
  "errorMessage": "SQL syntax error: Invalid table name 'invalid_table'",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#invalid_sql_query"
}
```

**Example 3:**

```json lines wrap theme={null}
{
  "errorType": "invalid_sql_query",
  "errorMessage": "Query exceeds maximum length of 10,000 characters",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#invalid_sql_query"
}
```

<a />

### Unknown

**Example 1:**

```json lines wrap theme={null}
{
  "isValid": false,
  "invalidReason": "insufficient_funds",
  "invalidMessage": "Insufficient funds",
  "payer": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#error-type"
}
```

**Example 2:**

```json lines wrap theme={null}
{
  "success": false,
  "errorReason": "insufficient_funds",
  "errorMessage": "Insufficient funds",
  "payer": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  "transaction": "0x89c91c789e57059b17285e7ba1716a1f5ff4c5dace0ea5a5135f26158d0421b9",
  "network": "base",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#error-type"
}
```

<a />

### Network not tradable

This error occurs when the selected asset cannot be purchased on the selected network in the user's location.

**Steps to resolve:**

1. Verify the asset is tradable on the selected network
2. Check the user's location to ensure it is allowed to purchase the asset on the selected network

**Common causes:**

* Users in NY are not allowed to purchase USDC on any network other than Ethereum

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "network_not_tradable",
  "errorMessage": "The selected asset cannot be purchased on the selected network in the user's location.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#network_not_tradable"
}
```

<a />

### Guest permission denied

This error occurs when the user is not allowed to complete onramp transactions as a guest.

**Steps to resolve:**

1. Redirect the user to create a Coinbase account to buy and send crypto.

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "guest_permission_denied",
  "errorMessage": "The user is not allowed to complete onramp transactions as a guest.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#guest_permission_denied"
}
```

<a />

### Guest region forbidden

This error occurs when guest onramp transactions are not allowed in the user's region.

**Steps to resolve:**

1. Redirect the user to create a Coinbase account to buy and send crypto.

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "guest_region_forbidden",
  "errorMessage": "Guest onramp transactions are not allowed in the user's region.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#guest_region_forbidden"
}
```

<a />

### Guest transaction limit

This error occurs when the user has reached the weekly guest onramp transaction limit.

**Steps to resolve:**

1. Inform the user they have reached their weekly limit and will have to wait until next week.

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "guest_transaction_limit",
  "errorMessage": "This transaction would exceed the user's weekly guest onramp transaction limit.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#guest_transaction_limit"
}
```

<a />

### Guest transaction count

This error occurs when the user has reached the lifetime guest onramp transaction count limit.

**Steps to resolve:**

1. Redirect the user to create a Coinbase account to buy and send crypto.

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "guest_transaction_count",
  "errorMessage": "The user has reached the lifetime guest onramp transaction count limit (15).",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#guest_transaction_count"
}
```

<a />

### Phone number verification expired

This error occurs when the user's phone number verification has expired. Use of guest Onramp requires the user's
phone number to be verified every 60 days.

**Steps to resolve:**

1. Re-verify the user's phone number via OTP.
2. Retry the request with the phoneNumberVerifiedAt field set to new verification timestamp.

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "phone_number_verification_expired",
  "errorMessage": "The user's phone number verification has expired. Please re-verify the user's phone number",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#phone_number_verification_expired"
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
  "errorMessage": "The request is not properly authenticated.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#unauthorized"
}
```

**Example 2:**

```json lines wrap theme={null}
{
  "errorType": "unauthorized",
  "errorMessage": "Wallet authentication error.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#unauthorized"
}
```

**Example 3:**

```json lines wrap theme={null}
{
  "errorType": "unauthorized",
  "errorMessage": "Invalid JWT issuer: not-cdp-api, expected: cdp-api",
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
  "errorMessage": "A valid payment method is required to complete this operation. Please add a payment method to your account at https://portal.cdp.coinbase.com.",
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

**Example 1:**

```json lines wrap theme={null}
{
  "errorType": "forbidden",
  "errorMessage": "Unable to sign transaction for this address.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#forbidden"
}
```

**Example 2:**

```json lines wrap theme={null}
{
  "errorType": "forbidden",
  "errorMessage": "Taker not permitted to perform swap.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#forbidden"
}
```

**Example 3:**

```json lines wrap theme={null}
{
  "errorType": "forbidden",
  "errorMessage": "Unable to request faucet funds for this address.",
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
  "errorMessage": "End user not found",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#not_found"
}
```

**Example 2:**

```json lines wrap theme={null}
{
  "errorType": "not_found",
  "errorMessage": "End user with the given ID not found.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#not_found"
}
```

**Example 3:**

```json lines wrap theme={null}
{
  "errorType": "not_found",
  "errorMessage": "EVM account with the given address not found.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#not_found"
}
```

## HTTP 408

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
  "errorMessage": "Query execution was cut off by the server. Please try again with a more efficient query.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#timed_out"
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

**Example 1:**

```json lines wrap theme={null}
{
  "errorType": "already_exists",
  "errorMessage": "An account with the given address already exists.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#already_exists"
}
```

**Example 2:**

```json lines wrap theme={null}
{
  "errorType": "already_exists",
  "errorMessage": "EVM account with the given name already exists.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#already_exists"
}
```

**Example 3:**

```json lines wrap theme={null}
{
  "errorType": "already_exists",
  "errorMessage": "Another request with the same idempotency key is currently processing.",
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
  "errorMessage": "Max concurrent user operations reached.",
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

**Example 3:**

```json lines wrap theme={null}
{
  "errorType": "rate_limit_exceeded",
  "errorMessage": "Rate limit exceeded.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#rate_limit_exceeded"
}
```

<a />

### Faucet limit exceeded

This error occurs when you've exceeded the faucet request limits.

**Steps to resolve:**

1. Wait for the time window to reset
2. Use funds more efficiently in your testing

For more information on faucet limits, please visit the [EVM Faucet endpoint](/api-reference/v2/rest-api/faucets/request-funds-on-evm-test-networks) or the [Solana Faucet endpoint](/api-reference/v2/rest-api/faucets/request-funds-on-solana-devnet).

**Example error response:**

```json lines wrap theme={null}
{
  "errorType": "faucet_limit_exceeded",
  "errorMessage": "Faucet limit reached for this address. Please try again later.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#faucet_limit_exceeded"
}
```

## HTTP 499

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
  "errorMessage": "The client closed the request before the server could send a response.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#client_closed_request"
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

**Example error response:**

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

## HTTP 504

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
  "errorMessage": "The request timed out because the server did not respond in time.",
  "correlationId": "41deb8d59a9dc9a7-IAD",
  "errorLink": "https://docs.cdp.coinbase.com/api-reference/v2/errors#timed_out"
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

