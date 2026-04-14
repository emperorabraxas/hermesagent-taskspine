# Fiat Deposits
Source: https://docs.cdp.coinbase.com/coinbase-app/transfer-apis/deposit-fiat



## Table of Endpoints

| Name                              | Method | Endpoint                                               | Legacy Scope             | CDP API Key Scope |
| :-------------------------------- | :----- | :----------------------------------------------------- | :----------------------- | :---------------- |
| [Deposit Funds](#deposit-funds)   | POST   | `/v2/accounts/:account_id/deposits`                    | `wallet:deposits:create` | `transfer`        |
| [Commit Deposit](#commit-deposit) | POST   | `/v2/accounts/:account_id/deposits/:deposit_id/commit` | `wallet:deposits:create` | `transfer`        |
| [List Deposits](#list-deposits)   | GET    | `/v2/accounts/:account_id/deposits`                    | `wallet:deposits:read`   | `view`            |
| [Show Deposit](#show-deposit)     | GET    | `/v2/accounts/:account_id/deposits/:deposit_id`        | `wallet:deposits:read`   | `view`            |

## Overview

The **Deposit resource** represents a deposit of funds using a payment method (e.g., a bank). Each committed deposit also has an associated transaction.

<Tip>
  You can [start a withdrawal](#deposit-funds) with the flag, `commit: false`, which is useful if you want to display a deposit before executing. Deposits made with `commit` set to `false` will not complete nor receive an associated transaction until a separate [commit](#commit-a-deposit) request is made.
</Tip>

| Parameter                                 | Description                                                                                         |
| :---------------------------------------- | :-------------------------------------------------------------------------------------------------- |
| `id` *string*                             | Resource ID                                                                                         |
| `status` *string, enumerable*             | Status of the deposit. Valid values: `created`, `completed`, `canceled`                             |
| `payment_method` *hash*                   | Associated payment method (e.g., a bank)                                                            |
| `transaction` *hash*                      | Associated transaction (e.g., a bank, fiat account)                                                 |
| `amount` *money hash*                     | Amount                                                                                              |
| `subtotal` *money hash*                   | Amount without fees                                                                                 |
| `fee` *money hash*                        | Fees associated to this deposit                                                                     |
| `created_at` *timestamp*                  |                                                                                                     |
| `updated_at` *timestamp*                  |                                                                                                     |
| `resource` *string, constant **deposit*** |                                                                                                     |
| `resource_path` *string*                  |                                                                                                     |
| `committed` *boolean*                     | Has this deposit been committed?                                                                    |
| `payout_at` *timestamp, optional*         | When a deposit isn't executed instantly, it receives a payout date for the time it will be executed |

#### Example Deposit Resource

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
  "resource": "deposit",
  "resource_path": "/v2/accounts/2bbf394c-193b-5b2a-9155-3b4732659ede/deposits/67e0eaec-07d7-54c4-a72c-2e92826897df",
  "committed": true,
  "fee": {
    "amount": "0.00",
    "currency": "USD"
  },
  "payout_at": "2015-02-18T16:54:00-08:00"
}
```

## Deposit Funds

Deposits user-defined amount of funds to a fiat account.

### HTTP Request

`POST https://api.coinbase.com/v2/accounts/:account_id/deposits`

### Scopes

* `wallet:deposits:create`

### Arguments

| Parameter        | Type    | Required | Description                                                                                                         |
| :--------------- | :------ | :------- | :------------------------------------------------------------------------------------------------------------------ |
| `amount`         | string  | Required | Deposit amount                                                                                                      |
| `currency`       | string  | Required | Currency for the `amount`                                                                                           |
| `payment_method` | string  | Required | ID of payment method to be used for the deposit. List Payment Methods: `GET /payment-methods`                       |
| `commit`         | boolean | Optional | If `false`, this deposit is not immediately completed. Use the `commit` call to complete it. Default value: `false` |

### Examples

#### Request

<CodeGroup>
  ```shell Shell  lines wrap theme={null}
  curl https://api.coinbase.com/v2/accounts/82de7fcd-db72-5085-8ceb-bee19303080b/deposits /
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

  deposit = client.deposit('2bbf394c-193b-5b2a-9155-3b4732659ede',
                           {"amount" => "10",
                            "currency" => "USD",
                            "payment_method" => "83562370-3e5c-51db-87da-752af5ab9559"})
  ```

  ```python Python  lines wrap theme={null}
  import requests

  # For instructions generating JWT, check the "API Key Authentication" section
  JWT_TOKEN = "<your_jwt_token>"

  # Coinbase API base URL
  ENDPOINT_URL = "https://api.coinbase.com/v2/accounts/:account_id/deposits"

  def deposit_funds():
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

  deposit_funds = deposit_funds()
  print(deposit_funds)
  ```

  ```javascript JavaScript  lines wrap theme={null}
  var Client = require('coinbase').Client;

  var client = new Client({'apiKey': 'API KEY',
                           'apiSecret': 'API SECRET'});

  client.getAccount('2bbf394c-193b-5b2a-9155-3b4732659ede', function(err, account) {
    account.deposit({"amount": "10",
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
  {
    "transfer": {
        "user_entered_amount": {
            "value": "20",
            "currency": "USD"
        },
        "amount": {
            "value": "20",
            "currency": "USD"
        },
        "total": {
            "value": "20",
            "currency": "USD"
        },
        "subtotal": {
            "value": "20",
            "currency": "USD"
        },
        "idem": "7ada05f0-4ab9-4e42-8cb9-4501e795315d",
        "committed": false,
        "id": "7ada05f0-4ab9-4e42-8cb9-4501e795315d",
        "instant": true,
        "source": {
            "type": "EXTERNAL_PAYMENT_METHOD",
            "network": "ach",
            "payment_method_id": "",
            "external_payment_method": {
                "payment_method_id": "5a48fe239b15170130598e9c"
            }
        },
        "target": {
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
        "payout_at": "2025-04-09T20:13:48.917581730Z",
        "status": "",
        "user_reference": "",
        "type": "TRANSFER_TYPE_DEPOSIT",
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

}
```

## Commit Deposit

Completes a [deposit](#deposit-funds) that is created in `commit: false` state.

### HTTP Request

`POST https://api.coinbase.com/v2/accounts/:account_id/deposits/:deposit_id/commit`

### Scopes

* `wallet:deposits:create`

### Arguments

*None*

### Examples

#### Request

<CodeGroup>
  ```shell Shell  lines wrap theme={null}
  curl https://api.coinbase.com/v2/accounts/82de7fcd-db72-5085-8ceb-bee19303080b/deposits/a333743d-184a-5b5b-abe8-11612fc44ab5/commit /
    -X POST \
    -H 'Authorization: Bearer abd90df5f27a7b170cd775abf89d632b350b7c1c9d53e08b340cd9832ce52c2c' \
  ```

  ```ruby Ruby  lines wrap theme={null}
  require 'coinbase/wallet'
  client = Coinbase::Wallet::Client.new(api_key: <api key>, api_secret: <api secret>)

  deposit = client.commit_deposit('2bbf394c-193b-5b2a-9155-3b4732659ede',
                                  'a333743d-184a-5b5b-abe8-11612fc44ab5')
  ```

  ```python Python  lines wrap theme={null}
  import requests

  # For instructions generating JWT, check the "API Key Authentication" section
  JWT_TOKEN = "<your_jwt_token>"

  # Coinbase API base URL
  ENDPOINT_URL = "https://api.coinbase.com/v2/accounts/:account_id/deposits/:deposit_id/commit"

  def commit_deposit():
      # Generate headers with JWT for authentication
      headers = {
          "Authorization": f"Bearer {JWT_TOKEN}"
      }

      # Make the API request
      response = requests.post(ENDPOINT_URL, headers=headers)

      return response.json()  # Return the JSON response

  commit_deposit = commit_deposit()
  print(commit_deposit)
  ```

  ```javascript JavaScript  lines wrap theme={null}
  var Client = require('coinbase').Client;

  var client = new Client({'apiKey': 'API KEY',
                           'apiSecret': 'API SECRET'});

  client.getAccount('2bbf394c-193b-5b2a-9155-3b4732659ede', function(err, account) {
    account.getDeposit('a333743d-184a-5b5b-abe8-11612fc44ab5', function(err, tx) {
      tx.commit(function(err, resp) {
        console.log(resp);
      });
    });
  });
  ```
</CodeGroup>

#### Response (200)

```json [expandable] lines wrap theme={null}
{
    "transfer": {
        "user_entered_amount": {
            "value": "20",
            "currency": "USD"
        },
        "amount": {
            "value": "20",
            "currency": "USD"
        },
        "total": {
            "value": "20",
            "currency": "USD"
        },
        "subtotal": {
            "value": "20",
            "currency": "USD"
        },
        "idem": "bd4d2728-9d0c-478e-829e-8f4b4888b108",
        "committed": false,
        "id": "bd4d2728-9d0c-478e-829e-8f4b4888b108",
        "instant": true,
        "source": {
            "type": "EXTERNAL_PAYMENT_METHOD",
            "network": "ach",
            "payment_method_id": "",
            "external_payment_method": {
                "payment_method_id": "5a48fe239b15170130598e9c"
            }
        },
        "target": {
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
        "payout_at": "2025-04-10T18:07:25.938533583Z",
        "status": "",
        "user_reference": "CODE",
        "type": "TRANSFER_TYPE_DEPOSIT",
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

## List Deposits

Lists fiat deposits for an account.

<Warning>
  Deposits are only listed for fiat accounts and wallets. To list deposits associated with a crypto account/wallet, use [List Transactions](#list-transactions).
</Warning>

### HTTP Request

`GET https://api.coinbase.com/v2/accounts/:account_id/deposits`

### Scopes

* `wallet:deposits:read`

### Examples

#### Request

<CodeGroup>
  ```shell Shell  lines wrap theme={null}
  curl https://api.coinbase.com/v2/accounts/2bbf394c-193b-5b2a-9155-3b4732659ede/deposits \
    -H 'Authorization: Bearer abd90df5f27a7b170cd775abf89d632b350b7c1c9d53e08b340cd9832ce52c2c'
  ```

  ```ruby Ruby  lines wrap theme={null}
  require 'coinbase/wallet'
  client = Coinbase::Wallet::Client.new(api_key: <api key>, api_secret: <api secret>)

  deposits = client.list_deposits('2bbf394c-193b-5b2a-9155-3b4732659ede')
  ```

  ```python Python  lines wrap theme={null}
  import requests

  # For instructions generating JWT, check the "API Key Authentication" section
  JWT_TOKEN = "<your_jwt_token>"

  # Coinbase API base URL
  ENDPOINT_URL = "https://api.coinbase.com/v2/accounts/:account_id/deposits"

  def list_deposits():
      # Generate headers with JWT for authentication
      headers = {
          "Authorization": f"Bearer {JWT_TOKEN}"
      }

      # Make the API request
      response = requests.get(ENDPOINT_URL, headers=headers)

      return response.json()  # Return the JSON response

  deposits = list_deposits()
  print(deposits)
  ```

  ```javascript lines wrap theme={null}
  var Client = require('coinbase').Client;

  var client = new Client({'apiKey': 'API KEY',
                           'apiSecret': 'API SECRET'});

  client.getAccount('2bbf394c-193b-5b2a-9155-3b4732659ede', function(err, account) {
    account.getDeposits(function(err, txs) {
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
      "resource": "deposit",
      "resource_path": "/v2/accounts/2bbf394c-193b-5b2a-9155-3b4732659ede/deposits/67e0eaec-07d7-54c4-a72c-2e92826897df",
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

## Show Deposit

Get one deposit by deposit Id.

### HTTP Request

`GET https://api.coinbase.com/v2/accounts/:account_id/deposits/:deposit_id`

### Scopes

* `wallet:deposits:read`

### Examples

#### Request

<CodeGroup>
  ```shell Shell  lines wrap theme={null}
  curl https://api.coinbase.com/v2/accounts/2bbf394c-193b-5b2a-9155-3b4732659ede/deposits/67e0eaec-07d7-54c4-a72c-2e92826897df /
    -H 'Authorization: Bearer abd90df5f27a7b170cd775abf89d632b350b7c1c9d53e08b340cd9832ce52c2c'
  ```

  ```ruby Ruby  lines wrap theme={null}
  require 'coinbase/wallet'
  client = Coinbase::Wallet::Client.new(api_key: <api key>, api_secret: <api secret>)

  deposit = client.list_deposit('2bbf394c-193b-5b2a-9155-3b4732659ede',
                                'dd3183eb-af1d-5f5d-a90d-cbff946435ff')
  ```

  ```python Python  lines wrap theme={null}
  import requests

  # For instructions generating JWT, check the "API Key Authentication" section
  JWT_TOKEN = "<your_jwt_token>"

  # Coinbase API base URL
  ENDPOINT_URL = "https://api.coinbase.com/v2/accounts/:account_id/deposits/:deposit_id"

  def show_deposit():
      # Generate headers with JWT for authentication
      headers = {
          "Authorization": f"Bearer {JWT_TOKEN}"
      }

      # Make the API request
      response = requests.get(ENDPOINT_URL, headers=headers)

      return response.json()  # Return the JSON response

  deposit = show_deposit()
  print(deposit)
  ```

  ```javascript JavaScript  lines wrap theme={null}
  var Client = require('coinbase').Client;

  var client = new Client({'apiKey': 'API KEY',
                           'apiSecret': 'API SECRET'});

  client.getAccount('2bbf394c-193b-5b2a-9155-3b4732659ede', function(err, account) {
    account.getDeposit('dd3183eb-af1d-5f5d-a90d-cbff946435ff', function(err, tx) {
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
    "resource": "deposit",
    "resource_path": "/v2/accounts/2bbf394c-193b-5b2a-9155-3b4732659ede/deposits/67e0eaec-07d7-54c4-a72c-2e92826897df",
    "committed": true,
    "fee": {
      "amount": "0.00",
      "currency": "USD"
    },
    "payout_at": "2015-02-18T16:54:00-08:00"
  }
}
```

