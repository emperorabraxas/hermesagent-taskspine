# Fiat Withdrawals
Source: https://docs.cdp.coinbase.com/coinbase-app/transfer-apis/withdraw-fiat



## Table of Endpoints

| Name                                    | Method | Endpoint                                                     | Legacy Scope                | CDP API Key Scope |
| :-------------------------------------- | :----- | :----------------------------------------------------------- | :-------------------------- | :---------------- |
| [Withdraw Funds](#withdraw-funds)       | POST   | `/v2/accounts/:account_id/withdrawals`                       | `wallet:withdrawals:create` | `transfer`        |
| [Commit Withdrawal](#commit-withdrawal) | POST   | `/v2/accounts/:account_id/withdrawals/:withdrawal_id/commit` | `wallet:withdrawals:create` | `transfer`        |
| [List Withdrawals](#list-withdrawals)   | GET    | `/v2/accounts/:account_id/withdrawals`                       | `wallet:withdrawals:read`   | `view`            |
| [Show Withdrawal](#show-withdrawal)     | GET    | `/v2/accounts/:account_id/withdrawals/:withdrawal_id`        | `wallet:withdrawals:read`   | `view`            |

## Overview

The **Withdrawal resource** represents a withdrawal of funds using a payment method (e.g., a bank). Each committed withdrawal also has an associated transaction.

<Tip>
  You can [start a withdrawal](#withdraw-funds) with the flag, `commit: false`, which is useful if you want to display a withdrawal before executing. Withdrawals made with `commit` set to `false` will not complete nor receive an associated transaction until a separate [commit](#commit-a-withdrawal) request is made.
</Tip>

| Parameter                                    | Description                                                                                            |
| :------------------------------------------- | :----------------------------------------------------------------------------------------------------- |
| `id` *string*                                | Resource ID                                                                                            |
| `status` *string, enumerable*                | Status of the withdrawal. Valid values: `created`, `completed`, `canceled`                             |
| `payment_method` *hash*                      | Associated payment method (e.g., a bank)                                                               |
| `transaction` *hash*                         | Associated transaction (e.g., a bank, fiat account)                                                    |
| `amount` *money hash*                        | Amount                                                                                                 |
| `subtotal` *money hash*                      | Amount without fees                                                                                    |
| `fee` *money hash*                           | Fee associated to this withdrawal                                                                      |
| `created_at` *timestamp*                     |                                                                                                        |
| `updated_at` *timestamp*                     |                                                                                                        |
| `resource` *string, constant **withdrawal*** |                                                                                                        |
| `resource_path` *string*                     |                                                                                                        |
| `committed` *boolean*                        | Has this withdrawal been committed?                                                                    |
| `payout_at` *timestamp, optional*            | When a withdrawal isn't executed instantly, it receives a payout date for the time it will be executed |

#### Example Withdrawal Resource

```json [expandable] lines wrap theme={null}
{
  "id": "67e0eaec-07d7-54c4-a72c-2e92826897df",
  "status": "completed",
  "payment_method": {
    "id": "83562370-3e5c-51db-87da-752af5ab9559",
    "resource": "payment_method",
    "resource_path": "/v2/payment-methods/83562370-3e5c-51db-87da-752af5ab9559"
  },
  "transaction": {
    "id": "441b9494-b3f0-5b98-b9b0-4d82c21c252a",
    "resource": "transaction",
    "resource_path": "/v2/accounts/2bbf394c-193b-5b2a-9155-3b4732659ede/transactions/441b9494-b3f0-5b98-b9b0-4d82c21c252a"
  },
  "amount": {
    "amount": "10.00",
    "currency": "USD"
  },
  "subtotal": {
    "amount": "10.00",
    "currency": "USD"
  },
  "created_at": "2015-01-31T20:49:02Z",
  "updated_at": "2015-02-11T16:54:02-08:00",
  "resource": "withdrawal",
  "resource_path": "/v2/accounts/2bbf394c-193b-5b2a-9155-3b4732659ede/withdrawals/67e0eaec-07d7-54c4-a72c-2e92826897df",
  "committed": true,
  "fee": {
    "amount": "0.00",
    "currency": "USD"
  },
  "payout_at": "2015-02-18T16:54:00-08:00"
}
```

## Withdraw Funds

Withdraws a user-defined amount of funds from a fiat account.

### HTTP Request

`POST https://api.coinbase.com/v2/accounts/:account_id/withdrawals`

### Scopes

* `wallet:withdrawals:create`

### Arguments

| Parameter        | Type    | Required | Description                                                                                                            |
| :--------------- | :------ | :------- | :--------------------------------------------------------------------------------------------------------------------- |
| `amount`         | string  | Required | Withdrawal amount                                                                                                      |
| `currency`       | string  | Required | Currency for the `amount`                                                                                              |
| `payment_method` | string  | Required | ID of payment method used for the withdrawal. List Payment Methods: `GET /payment-methods`                             |
| `commit`         | boolean | Optional | If `false`, this withdrawal is not immediately completed. Use the `commit` call to complete it. Default value: `false` |

### Examples

#### Request

<CodeGroup>
  ```shell Shell  lines wrap theme={null}
  curl https://api.coinbase.com/v2/accounts/82de7fcd-db72-5085-8ceb-bee19303080b/withdrawals /
    -X POST \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer abd90df5f27a7b170cd775abf89d632b350b7c1c9d53e08b340cd9832ce52c2c' \
    -d '{
      "amount": "10",
      "currency": "USD",
      "payment_method": "83562370-3e5c-51db-87da-752af5ab9559"
    }'
  ```

  ```ruby Ruby  lines wrap theme={null}
  require 'coinbase/wallet'
  client = Coinbase::Wallet::Client.new(api_key: <api key>, api_secret: <api secret>)

  withdrawal = client.withdraw('2bbf394c-193b-5b2a-9155-3b4732659ede',
                               {"amount" => "10",
                                "currency" => "USD",
                                "payment_method" => "83562370-3e5c-51db-87da-752af5ab9559"})
  ```

  ```python Python  lines wrap theme={null}
  import requests

  # For instructions generating JWT, check the "API Key Authentication" section
  JWT_TOKEN = "<your_jwt_token>"

  # Coinbase API base URL
  ENDPOINT_URL = "https://api.coinbase.com/v2/accounts/:account_id/withdrawals"

  def withdraw():
      # Generate headers with JWT for authentication
      headers = {
          "Authorization": f"Bearer {JWT_TOKEN}"
      }

      data = {
        "amount": "10",
        "currency": "USD",
        "payment_method": "83562370-3e5c-51db-87da-752af5ab9559"
      }

      # Make the API request
      response = requests.post(ENDPOINT_URL, data=data, headers=headers)

      return response.json()  # Return the JSON response

  withdraw = withdraw()
  print(withdraw)
  ```

  ```javascript JavaScript  lines wrap theme={null}
  var Client = require('coinbase').Client;

  var client = new Client({'apiKey': 'API KEY',
                           'apiSecret': 'API SECRET'});

  client.getAccount('2bbf394c-193b-5b2a-9155-3b4732659ede', function(err, account) {
    account.withdraw({"amount": "10",
                      "currency": "USD",
                      "payment_method": "83562370-3e5c-51db-87da-752af5ab9559"}, function(err, tx) {
      console.log(tx);
    });
  });
  ```
</CodeGroup>

#### Response (200)

```json [expandable] lines wrap theme={null}
{
    "transfer": {
        "user_entered_amount": {
            "value": "9",
            "currency": "USD"
        },
        "amount": {
            "value": "9",
            "currency": "USD"
        },
        "total": {
            "value": "9",
            "currency": "USD"
        },
        "subtotal": {
            "value": "9",
            "currency": "USD"
        },
        "idem": "97c0dcf2-daf7-446c-8dcc-66a9b72b6391",
        "committed": false,
        "id": "97c0dcf2-daf7-446c-8dcc-66a9b72b6391",
        "instant": false,
        "source": {
            "type": "LEDGER_ACCOUNT",
            "network": "internal_retail",
            "payment_method_id": "",
            "ledger_account": {
                "account_id": "6c770048-a3aa-580b-b153-2a6791649ee4",
                "currency": "USD",
                "owner": {
                    "id": "5a48fda3bbf66c03a6509af2",
                    "uuid": "",
                    "user_uuid": "",
                    "type": "RETAIL"
                }
            }
        },
        "target": {
            "type": "EXTERNAL_PAYMENT_METHOD",
            "network": "ach",
            "payment_method_id": "",
            "external_payment_method": {
                "payment_method_id": "5a48fe239b15170130598e9c"
            }
        },
        "payout_at": "2025-04-12T19:29:48.611016197Z",
        "status": "",
        "user_reference": "",
        "type": "TRANSFER_TYPE_WITHDRAWAL",
        "created_at": null,
        "updated_at": null,
        "user_warnings": [],
        "fees": [],
        "total_fee": {
            "title": "Fee Total",
            "description": "Total fee associated with this transaction",
            "amount": {
                "value": "0.00",
                "currency": "USD"
            },
            "type": "COINBASE"
        },
        "cancellation_reason": null,
        "hold_days": 0,
        "nextStep": null,
        "checkout_url": "",
        "requires_completion_step": false
    }
}
```

## Commit Withdrawal

Completes a [withdrawal](#withdraw-funds) that is created in `commit: false` state.

### HTTP Request

`POST https://api.coinbase.com/v2/accounts/:account_id/withdrawals/:withdrawal_id/commit`

### Scopes

* `wallet:withdrawals:create`

### Arguments

*None*

### Examples

#### Request

<CodeGroup>
  ```shell Shell  lines wrap theme={null}
  curl https://api.coinbase.com/v2/accounts/82de7fcd-db72-5085-8ceb-bee19303080b/withdrawals/a333743d-184a-5b5b-abe8-11612fc44ab5/commit /
    -X POST /
    -H 'Authorization: Bearer abd90df5f27a7b170cd775abf89d632b350b7c1c9d53e08b340cd9832ce52c2c'
  ```

  ```ruby Ruby  lines wrap theme={null}
  require 'coinbase/wallet'
  client = Coinbase::Wallet::Client.new(api_key: <api key>, api_secret: <api secret>)

  withdrawal = client.commit_withdrawal('2bbf394c-193b-5b2a-9155-3b4732659ede',
                                        'a333743d-184a-5b5b-abe8-11612fc44ab5')
  ```

  ```python Python  lines wrap theme={null}
  import requests

  # For instructions generating JWT, check the "API Key Authentication" section
  JWT_TOKEN = "<your_jwt_token>"

  # Coinbase API base URL
  ENDPOINT_URL = "https://api.coinbase.com/v2/accounts/:account_id/withdrawals/:withdrawal_id/commit"

  def commit_withdrawal():
      # Generate headers with JWT for authentication
      headers = {
          "Authorization": f"Bearer {JWT_TOKEN}"
      }

      # Make the API request
      response = requests.post(ENDPOINT_URL, headers=headers)

      return response.json()  # Return the JSON response

  commit = commit_withdrawal()
  print(commit)
  ```

  ```javascript JavaScript  lines wrap theme={null}
  var Client = require('coinbase').Client;

  var client = new Client({'apiKey': 'API KEY',
                           'apiSecret': 'API SECRET'});

  client.getAccount('2bbf394c-193b-5b2a-9155-3b4732659ede', function(err, account) {
    account.getWithdrawal('a333743d-184a-5b5b-abe8-11612fc44ab5', function(err, tx) {
      tx.commit(function(err, resp) {
        console.log(resp);
      });
    });
  });
  ```
</CodeGroup>

> Response (200)

```json [expandable] lines wrap theme={null}
{
    "transfer": {
        "user_entered_amount": {
            "value": "9",
            "currency": "USD"
        },
        "amount": {
            "value": "9",
            "currency": "USD"
        },
        "total": {
            "value": "9",
            "currency": "USD"
        },
        "subtotal": {
            "value": "9",
            "currency": "USD"
        },
        "idem": "97c0dcf2-daf7-446c-8dcc-66a9b72b6391",
        "committed": false,
        "id": "97c0dcf2-daf7-446c-8dcc-66a9b72b6391",
        "instant": false,
        "source": {
            "type": "LEDGER_ACCOUNT",
            "network": "internal_retail",
            "payment_method_id": "",
            "ledger_account": {
                "account_id": "6c770048-a3aa-580b-b153-2a6791649ee4",
                "currency": "USD",
                "owner": {
                    "id": "5a48fda3bbf66c03a6509af2",
                    "uuid": "",
                    "user_uuid": "",
                    "type": "RETAIL"
                }
            }
        },
        "target": {
            "type": "EXTERNAL_PAYMENT_METHOD",
            "network": "ach",
            "payment_method_id": "",
            "external_payment_method": {
                "payment_method_id": "5a48fe239b15170130598e9c"
            }
        },
        "payout_at": "2025-04-12T19:29:48.611016197Z",
        "status": "",
        "user_reference": "CODE",
        "type": "TRANSFER_TYPE_WITHDRAWAL",
        "created_at": null,
        "updated_at": null,
        "user_warnings": [],
        "fees": [],
        "total_fee": {
            "title": "Fee Total",
            "description": "Total fee associated with this transaction",
            "amount": {
                "value": "0.00",
                "currency": "USD"
            },
            "type": "COINBASE"
        },
        "cancellation_reason": null,
        "hold_days": 0,
        "nextStep": null,
        "checkout_url": "",
        "requires_completion_step": false
    }
}
```

## List Withdrawals

Lists withdrawals for an account.

### HTTP Request

`GET https://api.coinbase.com/v2/accounts/:account_id/withdrawals`

### Scopes

* `wallet:withdrawals:read`

### Examples

#### Request

<CodeGroup>
  ```shell Shell  lines wrap theme={null}
  curl https://api.coinbase.com/v2/accounts/2bbf394c-193b-5b2a-9155-3b4732659ede/withdrawals /
    -H 'Authorization: Bearer abd90df5f27a7b170cd775abf89d632b350b7c1c9d53e08b340cd9832ce52c2c'
  ```

  ```ruby Ruby  lines wrap theme={null}
  require 'coinbase/wallet'
  client = Coinbase::Wallet::Client.new(api_key: <api key>, api_secret: <api secret>)

  withdrawals = client.list_withdrawals('2bbf394c-193b-5b2a-9155-3b4732659ede')
  ```

  ```python Python  lines wrap theme={null}
  import requests

  # For instructions generating JWT, check the "API Key Authentication" section
  JWT_TOKEN = "<your_jwt_token>"

  # Coinbase API base URL
  ENDPOINT_URL = "https://api.coinbase.com/v2/accounts/:account_id/withdrawals"

  def list_withdrawals():
      # Generate headers with JWT for authentication
      headers = {
          "Authorization": f"Bearer {JWT_TOKEN}"
      }

      # Make the API request
      response = requests.get(ENDPOINT_URL, headers=headers)

      return response.json()  # Return the JSON response

  withdrawals = list_withdrawals()
  print(withdrawals)
  ```

  ```javascript JavaScript  lines wrap theme={null}
  var Client = require('coinbase').Client;

  var client = new Client({'apiKey': 'API KEY',
                           'apiSecret': 'API SECRET'});

  client.getAccount('2bbf394c-193b-5b2a-9155-3b4732659ede', function(err, account) {
    account.getWithdrawals(function(err, txs) {
      console.log(txs);
    });
  });
  ```
</CodeGroup>

#### Response

```json [expandable] lines wrap theme={null}
{
  "pagination": {
    "ending_before": null,
    "starting_after": null,
    "limit": 25,
    "order": "desc",
    "previous_uri": null,
    "next_uri": null
  },
  "data": [
    {
      "id": "67e0eaec-07d7-54c4-a72c-2e92826897df",
      "status": "completed",
      "payment_method": {
        "id": "83562370-3e5c-51db-87da-752af5ab9559",
        "resource": "payment_method",
        "resource_path": "/v2/payment-methods/83562370-3e5c-51db-87da-752af5ab9559"
      },
      "transaction": {
        "id": "441b9494-b3f0-5b98-b9b0-4d82c21c252a",
        "resource": "transaction",
        "resource_path": "/v2/accounts/2bbf394c-193b-5b2a-9155-3b4732659ede/transactions/441b9494-b3f0-5b98-b9b0-4d82c21c252a"
      },
      "amount": {
        "amount": "10.00",
        "currency": "USD"
      },
      "subtotal": {
        "amount": "10.00",
        "currency": "USD"
      },
      "created_at": "2015-01-31T20:49:02Z",
      "updated_at": "2015-02-11T16:54:02-08:00",
      "resource": "withdrawal",
      "resource_path": "/v2/accounts/2bbf394c-193b-5b2a-9155-3b4732659ede/withdrawals/67e0eaec-07d7-54c4-a72c-2e92826897df",
      "committed": true,
      "fee": {
        "amount": "0.00",
        "currency": "USD"
      },
      "payout_at": "2015-02-18T16:54:00-08:00"
    }
  ]
}
```

## Show Withdrawal

Get a single withdrawal.

### HTTP Request

`GET https://api.coinbase.com/v2/accounts/:account_id/withdrawals/:withdrawal_id`

### Scopes

* `wallet:withdrawals:read`

### Examples

#### Request

<CodeGroup>
  ```shell Shell  lines wrap theme={null}
  curl https://api.coinbase.com/v2/accounts/2bbf394c-193b-5b2a-9155-3b4732659ede/withdrawals/67e0eaec-07d7-54c4-a72c-2e92826897df /
    -H 'Authorization: Bearer abd90df5f27a7b170cd775abf89d632b350b7c1c9d53e08b340cd9832ce52c2c'
  ```

  ```ruby Ruby  lines wrap theme={null}
  require 'coinbase/wallet'
  client = Coinbase::Wallet::Client.new(api_key: <api key>, api_secret: <api secret>)

  withdrawal = client.list_withdrawal('2bbf394c-193b-5b2a-9155-3b4732659ede',
                                      'dd3183eb-af1d-5f5d-a90d-cbff946435ff')
  ```

  ```python Python  lines wrap theme={null}
  import requests

  # For instructions generating JWT, check the "API Key Authentication" section
  JWT_TOKEN = "<your_jwt_token>"

  # Coinbase API base URL
  ENDPOINT_URL = "https://api.coinbase.com/v2/accounts/:account_id/withdrawals/:withdrawal_id"

  def show_withdrawal():
      # Generate headers with JWT for authentication
      headers = {
          "Authorization": f"Bearer {JWT_TOKEN}"
      }

      # Make the API request
      response = requests.get(ENDPOINT_URL, headers=headers)

      return response.json()  # Return the JSON response

  withdrawal = show_withdrawal()
  print(withdrawal)
  ```

  ```javascript JavaScript  lines wrap theme={null}
  var Client = require('coinbase').Client;

  var client = new Client({'apiKey': 'API KEY',
                           'apiSecret': 'API SECRET'});

  client.getAccount('2bbf394c-193b-5b2a-9155-3b4732659ede', function(err, account) {
    account.getWithdrawal('dd3183eb-af1d-5f5d-a90d-cbff946435ff', function(err, tx) {
      console.log(tx);
    });
  });
  ```
</CodeGroup>

#### Response

```json [expandable] lines wrap theme={null}
{
  "data": {
    "id": "67e0eaec-07d7-54c4-a72c-2e92826897df",
    "status": "completed",
    "payment_method": {
      "id": "83562370-3e5c-51db-87da-752af5ab9559",
      "resource": "payment_method",
      "resource_path": "/v2/payment-methods/83562370-3e5c-51db-87da-752af5ab9559"
    },
    "transaction": {
      "id": "441b9494-b3f0-5b98-b9b0-4d82c21c252a",
      "resource": "transaction",
      "resource_path": "/v2/accounts/2bbf394c-193b-5b2a-9155-3b4732659ede/transactions/441b9494-b3f0-5b98-b9b0-4d82c21c252a"
    },
    "amount": {
      "amount": "10.00",
      "currency": "USD"
    },
    "subtotal": {
      "amount": "10.00",
      "currency": "USD"
    },
    "created_at": "2015-01-31T20:49:02Z",
    "updated_at": "2015-02-11T16:54:02-08:00",
    "resource": "withdrawal",
    "resource_path": "/v2/accounts/2bbf394c-193b-5b2a-9155-3b4732659ede/withdrawals/67e0eaec-07d7-54c4-a72c-2e92826897df",
    "committed": true,
    "fee": {
      "amount": "0.00",
      "currency": "USD"
    },
    "payout_at": "2015-02-18T16:54:00-08:00"
  }
}
```

