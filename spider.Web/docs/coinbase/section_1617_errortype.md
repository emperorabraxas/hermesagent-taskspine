# ErrorType
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Variables/ErrorType



```ts theme={null}
ErrorType: {
  already_exists: "already_exists";
  bad_gateway: "bad_gateway";
  client_closed_request: "client_closed_request";
  faucet_limit_exceeded: "faucet_limit_exceeded";
  forbidden: "forbidden";
  idempotency_error: "idempotency_error";
  internal_server_error: "internal_server_error";
  invalid_request: "invalid_request";
  invalid_sql_query: "invalid_sql_query";
  invalid_signature: "invalid_signature";
  malformed_transaction: "malformed_transaction";
  not_found: "not_found";
  payment_method_required: "payment_method_required";
  payment_required: "payment_required";
  settlement_failed: "settlement_failed";
  rate_limit_exceeded: "rate_limit_exceeded";
  request_canceled: "request_canceled";
  service_unavailable: "service_unavailable";
  timed_out: "timed_out";
  unauthorized: "unauthorized";
  policy_violation: "policy_violation";
  policy_in_use: "policy_in_use";
  account_limit_exceeded: "account_limit_exceeded";
  network_not_tradable: "network_not_tradable";
  guest_permission_denied: "guest_permission_denied";
  guest_region_forbidden: "guest_region_forbidden";
  guest_transaction_limit: "guest_transaction_limit";
  guest_transaction_count: "guest_transaction_count";
  phone_number_verification_expired: "phone_number_verification_expired";
  document_verification_failed: "document_verification_failed";
  recipient_allowlist_violation: "recipient_allowlist_violation";
  recipient_allowlist_pending: "recipient_allowlist_pending";
  travel_rules_recipient_violation: "travel_rules_recipient_violation";
  source_account_invalid: "source_account_invalid";
  target_account_invalid: "target_account_invalid";
  source_account_not_found: "source_account_not_found";
  target_account_not_found: "target_account_not_found";
  source_asset_not_supported: "source_asset_not_supported";
  target_asset_not_supported: "target_asset_not_supported";
  target_email_invalid: "target_email_invalid";
  target_onchain_address_invalid: "target_onchain_address_invalid";
  transfer_amount_invalid: "transfer_amount_invalid";
  transfer_asset_not_supported: "transfer_asset_not_supported";
  insufficient_balance: "insufficient_balance";
  metadata_too_many_entries: "metadata_too_many_entries";
  metadata_key_too_long: "metadata_key_too_long";
  metadata_value_too_long: "metadata_value_too_long";
  travel_rules_field_missing: "travel_rules_field_missing";
  asset_mismatch: "asset_mismatch";
  mfa_already_enrolled: "mfa_already_enrolled";
  mfa_invalid_code: "mfa_invalid_code";
  mfa_flow_expired: "mfa_flow_expired";
  mfa_required: "mfa_required";
  mfa_not_enrolled: "mfa_not_enrolled";
  order_quote_expired: "order_quote_expired";
  order_already_filled: "order_already_filled";
  order_already_canceled: "order_already_canceled";
  account_not_ready: "account_not_ready";
  insufficient_liquidity: "insufficient_liquidity";
  insufficient_allowance: "insufficient_allowance";
  transaction_simulation_failed: "transaction_simulation_failed";
};
```

## Type declaration

| Name                                      | Type                                  |
| ----------------------------------------- | ------------------------------------- |
| <a /> `already_exists`                    | `"already_exists"`                    |
| <a /> `bad_gateway`                       | `"bad_gateway"`                       |
| <a /> `client_closed_request`             | `"client_closed_request"`             |
| <a /> `faucet_limit_exceeded`             | `"faucet_limit_exceeded"`             |
| <a /> `forbidden`                         | `"forbidden"`                         |
| <a /> `idempotency_error`                 | `"idempotency_error"`                 |
| <a /> `internal_server_error`             | `"internal_server_error"`             |
| <a /> `invalid_request`                   | `"invalid_request"`                   |
| <a /> `invalid_sql_query`                 | `"invalid_sql_query"`                 |
| <a /> `invalid_signature`                 | `"invalid_signature"`                 |
| <a /> `malformed_transaction`             | `"malformed_transaction"`             |
| <a /> `not_found`                         | `"not_found"`                         |
| <a /> `payment_method_required`           | `"payment_method_required"`           |
| <a /> `payment_required`                  | `"payment_required"`                  |
| <a /> `settlement_failed`                 | `"settlement_failed"`                 |
| <a /> `rate_limit_exceeded`               | `"rate_limit_exceeded"`               |
| <a /> `request_canceled`                  | `"request_canceled"`                  |
| <a /> `service_unavailable`               | `"service_unavailable"`               |
| <a /> `timed_out`                         | `"timed_out"`                         |
| <a /> `unauthorized`                      | `"unauthorized"`                      |
| <a /> `policy_violation`                  | `"policy_violation"`                  |
| <a /> `policy_in_use`                     | `"policy_in_use"`                     |
| <a /> `account_limit_exceeded`            | `"account_limit_exceeded"`            |
| <a /> `network_not_tradable`              | `"network_not_tradable"`              |
| <a /> `guest_permission_denied`           | `"guest_permission_denied"`           |
| <a /> `guest_region_forbidden`            | `"guest_region_forbidden"`            |
| <a /> `guest_transaction_limit`           | `"guest_transaction_limit"`           |
| <a /> `guest_transaction_count`           | `"guest_transaction_count"`           |
| <a /> `phone_number_verification_expired` | `"phone_number_verification_expired"` |
| <a /> `document_verification_failed`      | `"document_verification_failed"`      |
| <a /> `recipient_allowlist_violation`     | `"recipient_allowlist_violation"`     |
| <a /> `recipient_allowlist_pending`       | `"recipient_allowlist_pending"`       |
| <a /> `travel_rules_recipient_violation`  | `"travel_rules_recipient_violation"`  |
| <a /> `source_account_invalid`            | `"source_account_invalid"`            |
| <a /> `target_account_invalid`            | `"target_account_invalid"`            |
| <a /> `source_account_not_found`          | `"source_account_not_found"`          |
| <a /> `target_account_not_found`          | `"target_account_not_found"`          |
| <a /> `source_asset_not_supported`        | `"source_asset_not_supported"`        |
| <a /> `target_asset_not_supported`        | `"target_asset_not_supported"`        |
| <a /> `target_email_invalid`              | `"target_email_invalid"`              |
| <a /> `target_onchain_address_invalid`    | `"target_onchain_address_invalid"`    |
| <a /> `transfer_amount_invalid`           | `"transfer_amount_invalid"`           |
| <a /> `transfer_asset_not_supported`      | `"transfer_asset_not_supported"`      |
| <a /> `insufficient_balance`              | `"insufficient_balance"`              |
| <a /> `metadata_too_many_entries`         | `"metadata_too_many_entries"`         |
| <a /> `metadata_key_too_long`             | `"metadata_key_too_long"`             |
| <a /> `metadata_value_too_long`           | `"metadata_value_too_long"`           |
| <a /> `travel_rules_field_missing`        | `"travel_rules_field_missing"`        |
| <a /> `asset_mismatch`                    | `"asset_mismatch"`                    |
| <a /> `mfa_already_enrolled`              | `"mfa_already_enrolled"`              |
| <a /> `mfa_invalid_code`                  | `"mfa_invalid_code"`                  |
| <a /> `mfa_flow_expired`                  | `"mfa_flow_expired"`                  |
| <a /> `mfa_required`                      | `"mfa_required"`                      |
| <a /> `mfa_not_enrolled`                  | `"mfa_not_enrolled"`                  |
| <a /> `order_quote_expired`               | `"order_quote_expired"`               |
| <a /> `order_already_filled`              | `"order_already_filled"`              |
| <a /> `order_already_canceled`            | `"order_already_canceled"`            |
| <a /> `account_not_ready`                 | `"account_not_ready"`                 |
| <a /> `insufficient_liquidity`            | `"insufficient_liquidity"`            |
| <a /> `insufficient_allowance`            | `"insufficient_allowance"`            |
| <a /> `transaction_simulation_failed`     | `"transaction_simulation_failed"`     |

